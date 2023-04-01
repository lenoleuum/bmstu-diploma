import numpy as np
import random
import datetime
import music21

import sys
sys.path.append('..')

from music.Tonality import Tonality
from music.TonalityCircle import QuartoQuintCircle
from stats.Redis import redis_get,redis_get_parsed
from stats.Parse import create_key
from constants.Constants import ProbabilityCurTonality, BarsToGenerate, BarsInTonality, TimeSignature, NotesDurations, GammaBb, GammaDies, WorkDir
from utils.ProcessOutput import create_midi_file, play_midi


# обучающий набор данных из redis
DUR = redis_get('all_dur')
ALL_DATA = redis_get('all_new')


def generate_music_fragment(tonality: Tonality, data: dict = ALL_DATA, length: int = 100):
    start_note = np.random.choice(tonality.linked_list_to_list(),
                                  p=list([1 / len(tonality.linked_list_to_list()) for i in
                                          range(len(tonality.linked_list_to_list()))])) + "4" #str(random.randint(1, 7))
    
    start_note = str(convert_note(start_note))

    generated_fragment = [[start_note, predict_duration(start_note)]]
    
    
    for i in range(length):
        note = predict_next_sound(start_note, data)
        dur = predict_duration(note)

        generated_fragment.append([note, dur])

        start_note = generated_fragment[-1][0]

    print(generated_fragment)

    return generated_fragment


def find_nearest_above(my_array, target):
    diff = my_array - target
    mask = np.ma.less(diff, 0)
    # We need to mask the negative differences and zero
    # since we are looking for values above
    if np.all(mask):
        return None # returns None if target is greater than any value
    masked_diff = np.ma.masked_array(diff, mask)
    return masked_diff.argmin()


def generate_music_fragment_1(length: int = 100):
    init_prob_vector = redis_get_parsed("init_prob_vector")
    transition_matrix_vector = redis_get_parsed("transition_prob_matrix")
    states = redis_get_parsed("states")

    #print(states)
    
    '''note_prob = random.uniform(0, 1)
    rhythm_prob = random.uniform(0, 1)
    note_index = find_nearest_above(init_prob_vector, note_prob)
    curr_index = 0

    print("START ", note_index, states[note_index])

    seq = [None] * length

    while (curr_index < length):
        note_prob = random.uniform(0, 1)
        rhythm_prob = random.uniform(0, 1)

        note_index = find_nearest_above(transition_matrix_vector[note_index], note_prob)

        seq[curr_index] = [create_key(states[note_index]), 0.5]
        curr_index += 1'''


    sequence = [None] * length

    # comment in for same start note as training data
    note_prob = random.uniform(0, 1)
    rhythm_prob = random.uniform(0, 1)
    note_index = find_nearest_above(init_prob_vector, note_prob)
    curr_index = 0

    # comment in for seed
    # sequence[0] = parser.states[0]
    # note_index = 0
    # curr_index = 1

    while (curr_index < length):
        note_prob = random.uniform(0, 1)
        rhythm_prob = random.uniform(0, 1)

        note_index = find_nearest_above(transition_matrix_vector[note_index], note_prob)

        sequence[curr_index] = states[note_index]
        curr_index += 1

    return sequence

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

@DeprecationWarning
def get_suitable_tonality_data(tonality: Tonality, data: dict = ALL_DATA):
    data_suitable = dict()

    for n in data.keys():
        if n in tonality.linked_list_to_list():
            data_suitable[n] = data[n]

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


def predict_next_sound(note: str, notes_dict: dict = ALL_DATA):
    '''Случайно выбирает следующее событие (аккорд/нота), основываясь на текущем событии, на основе вероятностей в обучающем наборе'''
    data_notes = notes_dict[note]

    options_note = [key for key in data_notes.keys()]
    probabilities_note = [data_notes[key] for key in data_notes.keys()]

    return np.random.choice(options_note, p=probabilities_note)

def predict_duration(sound:str, dur_dict:dict=DUR):
    '''Случайно выбирает длительность для заданного звука на основе вероятностей в обучающем наборе'''
    data_dur = dur_dict[sound]

    options_dur = [key for key in data_dur.keys()]
    probabilities_dur = [data_dur[key] for key in data_dur.keys()]

    return np.random.choice(options_dur, p=probabilities_dur)



t = Tonality('major', 'C')
#n = generate_music_fragment(t)
#print(n)
filename = WorkDir + "\\" + str(datetime.datetime.now()).split('.')[0].replace(':', '-') + ".mid"
#create_midi_file(n, time_signature='4/4', bpm=100, file=filename)
#play_midi(filename)
n = generate_music_fragment_1()
print(n)
create_midi_file(n, time_signature='3/4', bpm=120, file=filename)

'''r = music21.chord.Chord(['C', 'E-', 'F#', 'A'])
print(r)
k = music21.key.KeySignature(1)
i = music21.interval.Interval(k.transposePitchFromC, music21.pitch.Pitch('C'))
r.transpose(-i)
print(r)'''
