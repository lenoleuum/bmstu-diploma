from .Parse import walk_directory, open_midi_file, extract_notes, extract_tonalities, create_key, get_duartions_all, get_bigrams_all_new, get_distinct_sounds_new, get_bigrams_all, count_appearances_all, get_distinct_sounds
from .Redis import redis_set
import uuid
import json

import sys
sys.path.append("..")

from constants.Constants import PATH
from models.Stats import Stats
from models.Track import Track
import datetime

def save_db(track_name:str, time_signature:str, tonalities:list, events:list):
    id_track = generate_id()
    track = Track(id=id_track, track_name=track_name, time_signature=str(time_signature), 
                  tonalities=json.dumps(tonalities), events=str(events))
    track.save(force_insert=True)

    stats = Stats(track_id=id_track, timestamp=datetime.datetime.now())
    stats.save(force_insert=True)

def generate_id():
    return uuid.uuid4()


def refresh_stats(path:str=PATH):
    #clear_stats()

    data = list()
    walk_directory(data, path)

    tonalities_all = []
    events_all = []
    events_all_new = []

    for dir in data:
        for file in dir:
            try:
                print(file)

                base_midi = open_midi_file(file, True)
                ts = base_midi.getTimeSignatures()[0]
                time_signature = str(ts).split(' ')[1].split('>')[0]
            
                events, events_new = extract_notes(base_midi)
                events_all_new += events_new
                events_all += events

                tonalities = extract_tonalities(base_midi)
                tonalities_all += tonalities
                
                #save_db(file.split('\\')[-1], time_signature, tonalities, events_new)
            except:
                continue

    '''bigram_notes = get_bigrams(notes_all)

    notes_dict = dict()
    for note in get_notes_codes():
        notes_dict[note] = predict_next_state(note, bigram_notes)

    notes_durations_dict = dict()
    for note in get_notes_codes():
        notes_durations_dict[note] = get_note_duartions(note, notes_all)'''

    bigrams_all = get_bigrams_all(events_all)
    distinct_sounds = get_distinct_sounds(events_all)

    '''sounds_dict = dict()
    durations_dict = dict()
    for n in distinct_sounds:
        key = create_key(n)
        sounds_dict[key] = count_appearances_all(key, bigrams_all)
        #durations_dict[key] = get_duartions_all(key, events_all)
        get_duartions_all(key, events_all)'''
    

    bigrams_all_new = get_bigrams_all_new(events_all_new)
    distinct_sounds_new = get_distinct_sounds_new(events_all_new)

    sounds_dict = dict()
    durations_dict = dict()
    for n in distinct_sounds_new:
        key = create_key(n)
        sounds_dict[key] = count_appearances_all(key, bigrams_all_new)
        durations_dict[key] = get_duartions_all(key, events_all_new)

    #redis_set('all_new', sounds_dict)
    #redis_set('all_dur', durations_dict)

    print('DONE')

    #redis_set('all', dict_all)
    #redis_set('notes', notes_dict)
    #redis_set('durations', notes_durations_dict)

    
# todo: объединить всю статистику в одну

def clear_stats():
    Track.truncate_table()
    Stats.truncate_table()


def get_bigrams(data:list):
    bigrams = []

    for i in range(len(data) - 1):
        cur = data[i][0]
        next = data[i + 1][0]
        bigrams.append(str(int(cur)) + ' ' + str(int(next)))

    return bigrams
    