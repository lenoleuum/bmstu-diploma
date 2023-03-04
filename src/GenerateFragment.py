import os
from collections import Counter

import numpy as np
import Constants as const
from TonalityCircle import QuartoQuintCircle
from Tonality import Tonality

from MyMidiFile import MidiFile

# todo: везде добавить типы todo: что делаем с time? и с сhannel/track? (можно ввести ограничение только на один
#  канал/трек aka мы играем только на фоно => один канал)

bigrams = []


def get_bigrams(data: list = bigrams):
    for filename in os.listdir(const.MidiFilesPath):
        f = os.path.join(const.MidiFilesPath, filename)

        if os.path.isfile(f):
            m = MidiFile(f)
            data += m.parse()


def handle_generation(start_note: str, tonality_gamma: list, data: list = bigrams):
    data_suitable = []

    for n in data:
        if n.split(' ')[0][:-1] in tonality_gamma or n.split(' ')[1][:-1] in tonality_gamma:
            data_suitable.append(n)

    notes = []

    for n in range(30):
        notes.append(predict_next_state(start_note, data))
        start_note = notes[-1]

    return notes


# todo: у меня фрагмент улетает сильно по тональностям, это надо поправить i guess

# tonality = list(tonica, lad, gamma)
def generate_music_fragment(tonality: Tonality, data: list = bigrams, length: int = 100):
    start_note = np.random.choice(tonality.linked_list_to_list(),
                                  p=list([1 / len(tonality.linked_list_to_list()) for i in range(len(tonality.linked_list_to_list()))])) + '4'
    generated_fragment = []
    tonality_cur = tonality

    quint_circle = QuartoQuintCircle()
    quint_circle.create_circle()

    tonality_options = quint_circle.get_relatives(tonality_cur)
    suitable_data = get_suitable_tonality_data(tonality_cur)
    tonality_probabilities = list(
        [0.5] + [(1 - 0.5) / (len(tonality_options) - 1) for i in range(len(tonality_options) - 1)])
    print(tonality_probabilities)

    for n in range(length):
        if n > 20 and n % 10 == 0 and np.random.choice([True, False], p=[0.8, 0.2]):
            tonality_cur = np.random.choice(tonality_options, p=tonality_probabilities)
            suitable_data = get_suitable_tonality_data(tonality_cur)

        print("CUR TONALITY - " + tonality_cur.tonica + tonality_cur.lad)
        generated_fragment.append((predict_next_state(start_note, suitable_data)))
        start_note = generated_fragment[-1]

    return generated_fragment


def get_suitable_tonality_data(tonality: Tonality, data: list = bigrams):
    data_suitable = []

    for n in data:
        if n.split(' ')[0][:-1] in tonality.linked_list_to_list() or n.split(' ')[1][:-1] in tonality.linked_list_to_list():
            data_suitable.append(n)

    return data_suitable


def predict_next_state(note: str, data: list = bigrams):
    # ищем пары нот, начинающиеся с переданной ноты
    bigrams_with_current_chord = [d for d in data if d.split(' ')[0] == note]

    # считаем частоту появления каждой найденной пары
    count_appearance = dict(Counter(bigrams_with_current_chord))

    # переводим частоту в вероятность
    for ngram in count_appearance.keys():
        count_appearance[ngram] = count_appearance[ngram] / len(bigrams_with_current_chord)

    # создаем список с возможными переходами
    options = [key.split(' ')[1] for key in count_appearance.keys()]

    # todo: проверка на null для options (если некуда перейти) - хотя по идее такого быть не должно (не хотелось бы
    #  точнее)

    # из словаря count_appearance делаем список с вероятностями (для numpy)
    probabilities = list(count_appearance.values())

    # рандомно выбираем ноту из options (куда перейти) на основе probabilities
    return np.random.choice(options, p=probabilities)


def generate_sequence(start_note: str = None, data: list = bigrams, length: int = 30):
    notes = []

    for n in range(length):
        notes.append(predict_next_state(start_note, data))
        start_note = notes[-1]

    return notes


# todo: биграмы по хорошему в redis засунуть + желательно сразу вероятности i guess, чтоб лишний раз не парсить +
#  посчитать это все заранее как-то
get_bigrams()

#t = Tonality('major', 'C')
#generate_music_fragment(t)