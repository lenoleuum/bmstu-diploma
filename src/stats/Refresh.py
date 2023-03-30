from .Parse import walk_directory, open_midi_file, extract_notes, extract_tonalities, create_key, get_duartions, count_appearances, get_distinct_sounds, get_bigrams, count_appearances_without_prob
from .Redis import redis_set, redis_get, redis_get_parsed
import uuid
import json
import collections
from .Parser import Parser

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
    count_dict = dict()
    sounds_dict_1 = dict()
    #sounds_dict, durations_dict = collections.OrderedDict(), dict()
    for n in distinct_sounds:
        key = create_key(n)
        sounds_dict[key] = count_appearances(key, bigrams_all)
        durations_dict[key] = get_duartions(key, events)
        count_dict[key] = count_appearances_without_prob(key, events)
        sounds_dict_1[key] = count_appearances(key, bigrams_all, False)

    #redis_set('all_new', sounds_dict)
    #redis_set('all_dur', durations_dict)

    print('DONE')

    #print(sounds_dict_1)

    p = Parser(distinct_sounds, count_dict, sounds_dict_1)
    p.create_initial_probability_vector()
    p.create_transition_probability_matrix()

    redis_set('states', distinct_sounds, False)
    redis_set('init_prob_vector', p.initial_probability_vector, False)
    redis_set('transition_prob_matrix', p.transition_probability_matrix, False)

    #redis_set('all', dict_all) - старые все события
    #redis_set('notes', notes_dict) - старые ноты
    #redis_set('durations', notes_durations_dict) - старые длительности для all

def clear_stats():
    Track.truncate_table()
    Stats.truncate_table()


d = collections.OrderedDict()
d['a'] = 'value_a'
d['b'] = 'value_b'
d['c'] = 'value_c'
d['c']['value_c'] = 'CCC'
print(d)