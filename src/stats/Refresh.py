from .Parse import walk_directory, open_midi_file, extract_notes, extract_tonalities, create_key, get_duartions, count_appearances, get_distinct_sounds, get_bigrams
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

    tonalities, events = [], []

    for dir in data:
        for file in dir:
            try:
                print(file)

                base_midi = open_midi_file(file, True)

                ts = base_midi.getTimeSignatures()[0]
                time_signature = str(ts).split(' ')[1].split('>')[0]
            
                events += extract_notes(base_midi)

                tonalities += extract_tonalities(base_midi)
                
                #save_db(file.split('\\')[-1], time_signature, tonalities, events)
            except:
                continue

    bigrams_all = get_bigrams(events)
    distinct_sounds = get_distinct_sounds(events)

    sounds_dict, durations_dict = dict(), dict()
    for n in distinct_sounds:
        key = create_key(n)
        sounds_dict[key] = count_appearances(key, bigrams_all)
        durations_dict[key] = get_duartions(key, events)

    #redis_set('all_new', sounds_dict)
    #redis_set('all_dur', durations_dict)

    print('DONE')

    #redis_set('all', dict_all) - старые все события
    #redis_set('notes', notes_dict) - старые ноты
    #redis_set('durations', notes_durations_dict) - старые длительности для all


def clear_stats():
    Track.truncate_table()
    Stats.truncate_table()