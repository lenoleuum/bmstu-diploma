from music21 import midi, note, chord
import os
from constants.Constants import PATH
from collections import Counter


def walk_directory(res:list, path:str=PATH, files_list:list=[]):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)

        if os.path.isfile(f):
            files_list.append(f)

        if os.path.isdir(f):
            walk_directory(res, f, [])

    if files_list != []:
        res.append(files_list)

def open_midi_file(midi_path:str, remove_drums:bool):
    '''Конвертирует MIDI файл в music21.Stream, предварительно удалив из файла барабанные партии'''
    mf = midi.MidiFile()

    mf.open(midi_path)
    mf.read()
    mf.close()

    if (remove_drums):
        for i in range(len(mf.tracks)):
            mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10] 

    return midi.translate.midiFileToStream(mf)

def extract_notes(midi_part):
    '''Возвращает список со всеми нотами/аккордами в потоке вместе с длительностями'''
    chords, events = [], []

    for nt in midi_part.flat.notes:  
        if isinstance(nt, note.Note):
            events.append([nt.duration.quarterLength, [max(0.0, nt.pitch.ps)]])
        elif isinstance(nt, chord.Chord):
            chords.append([])
            chords[-1].append(nt.duration.quarterLength)
            chords[-1].append([])

            for pitch in nt.pitches:
                chords[-1][-1].append(pitch.ps)

            events.append(chords[-1])

    return events

def extract_tonalities(midi_part):
    '''Возвращает словарь с тональностями в потоке и количеством их использования'''
    dict = {}
    for chorale in midi_part:
        key = chorale.analyze('key').tonicPitchNameWithCase
        dict[key] = dict[key] + 1 if key in dict.keys() else 1

    return dict


def durations_count_appearances(data:list):
    '''Возвращает словарь с вероятнотностью использования каждой переданной в функцию длительности'''
    count_appearance = dict(Counter(data))

    for ngram in count_appearance.keys():
        count_appearance[ngram] = count_appearance[ngram] / len(data)

    return count_appearance


def get_duartions(sound:str, data:list):
    '''Возвращает список с используемыми длительностями для заданного события (аккорд/нота)'''
    durations = []

    for n in data:
        if create_key(n[-1]) == sound:
            if 'Fraction' in str(n[0]):
                dur = str(n[0])[8:][:-1]
                durations.append(float(dur))
            else:
                durations.append(float(n[0]))

    return durations_count_appearances(durations)


def get_bigrams(data:list):
    bigrams = []

    for i in range(len(data) - 1):
        cur = data[i][-1]
        next = data[i + 1][-1]
        bigrams.append([cur, next])

    return bigrams    

def count_appearances(start:str, data:list):
    bigrams_with_current_sound = [create_key(d[1]) for d in data if create_key(d[0]) == start]

    count_appearance = dict(Counter(bigrams_with_current_sound))

    for ngram in count_appearance.keys():
        count_appearance[ngram] = count_appearance[ngram] / len(bigrams_with_current_sound)

    return count_appearance

def get_distinct_sounds(data:list):
    '''Возвращает список с уникальными событиями в потоке (аккорды/ноты)'''
    result = []

    for d in data:
        if not d[-1] in result:
            result.append(d[-1])

    return result

def create_key(data:list):
    '''Переводит список аккордов/нот в ключ словаря'''
    key = ""

    for i in range(len(data)):
        key += str(int(data[i])) 
        if i != len(data) - 1:
            key += " "

    return key