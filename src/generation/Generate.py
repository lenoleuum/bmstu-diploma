import numpy as np
import random
import datetime

import sys
sys.path.append('..')

from music.Tonality import Tonality
from music.TonalityCircle import QuartoQuintCircle
from stats.Redis import redis_get
from constants.Constants import ProbabilityCurTonality, BarsToGenerate, BarsInTonality, TimeSignature, NotesDurations, GammaBb, GammaDies, WorkDir
from utils.ProcessOutput import create_midi_file, play_midi

DATA = redis_get('notes')
DUR = redis_get('all_dur')
ALL_DATA = redis_get('all_new')

def generate_music_fragment(tonality: Tonality, data: dict = ALL_DATA, length: int = 100):
    start_note = np.random.choice(tonality.linked_list_to_list(),
                                  p=list([1 / len(tonality.linked_list_to_list()) for i in
                                          range(len(tonality.linked_list_to_list()))])) + "4"#str(random.randint(1, 7))
    
    start_note = str(convert_note(start_note))

    print("START ", start_note)

    #start_note = random.choice(list(data.keys()))

    generated_fragment = [[start_note, predict_duration(start_note)]]
    
    for i in range(length):
        note = predict_next_sound(start_note, data)
        dur = predict_duration(note)
        generated_fragment.append([note, dur])
        start_note = generated_fragment[-1][0]

    print(generated_fragment)

    return generated_fragment

@DeprecationWarning
def find_combinations(bar_length, beats_durations, res, lastindex=0, lst=[]):
    if bar_length == 0:
        res.append(lst)
    else:
        for i in range(lastindex, len(beats_durations)):
            if beats_durations[i] <= bar_length:
                find_combinations(bar_length - beats_durations[i], beats_durations, res, i, lst + [beats_durations[i]])

@DeprecationWarning
def get_bar_content(bar_duration: float, beat_duration: float):
    lst = []
    for d in NotesDurations:
        if d <= beat_duration:
            lst.append(d)

    combinations = []
    find_combinations(bar_duration, lst, combinations)
    for_delete = []

    print(combinations)

    for i in range(len(combinations)):
        if combinations[i].count(0.0625) > 8:
            for_delete.append(combinations[i])

    for i in for_delete:
        combinations.remove(i)

    indexes = [i for i in range(len(combinations))]

    print(combinations)

    # todo: вероятность получить комбинацию с 16 нотой должна быть оч маленькая
    # у меня почти везде получаются 16-е (если текущие длительности), надо тоже тут вероятность подкрутить
    # точнее выходят самые маленькие ноты по длительности - надо пофиксить
    res = combinations[np.random.choice(indexes)]
    random.shuffle(res)

    return res

def get_suitable_tonality_data(tonality: Tonality, data: dict = DATA):
    data_suitable = dict()

    for n in data.keys():
        if n in tonality.linked_list_to_list():
            data_suitable[n] = DATA[n]

    return data_suitable

def convert_note(note):
        key = note[:-1]
        octave = note[-1]
        midi_number = -1

        if not octave.isdigit():
            key = note
            octave = '4'

        try:
            if 'b' in key:
                pos = GammaBb.index(key)
            else:
                pos = GammaDies.index(key)
        except:
            return None

        midi_number += pos + 12 * (int(octave) + 1) + 1

        return midi_number


def predict_next_sound(note: str, notes_dict: dict = DATA):
    data_notes = notes_dict[note]

    options_note = [key for key in data_notes.keys()]
    probabilities_note = [data_notes[key] for key in data_notes.keys()]

    return np.random.choice(options_note, p=probabilities_note)

def predict_duration(sound:str, dur_dict:dict=DUR):
    data_dur = dur_dict[sound]

    options_dur = [key for key in data_dur.keys()]
    probabilities_dur = [data_dur[key] for key in data_dur.keys()]

    return np.random.choice(options_dur, p=probabilities_dur)

t = Tonality('major', 'C')
n = generate_music_fragment(t)
filename = WorkDir + "\\" + str(datetime.datetime.now()).split('.')[0].replace(':', '-') + ".mid"
create_midi_file(n, time_signature='3/4', bpm=120, file=filename)
#play_midi(filename)