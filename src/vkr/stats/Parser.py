import numpy as np
import collections
from music21 import midi, note, chord
import os
from constants.Constants import Constants
import mido

from .Redis import redis_set

class Parser:
    def __init__(self, path:str):
        self.path = path

        self.states = []
        self.states_appearances_dict = collections.OrderedDict()
        self.states_transition_dict = collections.OrderedDict()

        self.initial_probability_vector = None
        self.transition_probability_matrix = None


    def walk_directory(self, res:list, path:str, files_list:list=[]):
        for filename in os.listdir(path):
            f = os.path.join(path, filename)

            if os.path.isfile(f):
                files_list.append(f)

            if os.path.isdir(f):
                self.walk_directory(res, f, [])

        if files_list != []:
            res.append(files_list)

    def open_midi_file(self, midi_path:str, remove_drums:bool):
        mf = midi.MidiFile()

        mf.open(midi_path)
        mf.read()
        mf.close()

        if (remove_drums):
            for i in range(len(mf.tracks)):
                mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10] 

        return midi.translate.midiFileToStream(mf)

    def parse(self):
        print("[parse]")

        data = []
        self.walk_directory(data, self.path)
        
        for dir in data:
            cur_color = dir[0].split("\\")[-3]
            cur_lad = dir[0].split("\\")[-2]
            print("parsing", cur_color.upper(), cur_lad)

            for file in dir:
                print(file)
                midi_part = self.open_midi_file(file, True)

                sound_object_to_insert = None 
                prev_sound_object = None 
                first_sound_object = None

                try:
                    for nt in midi_part.flat.notes:  
                        prev_sound_object = sound_object_to_insert

                        if isinstance(nt, note.Note):
                            dur = nt.duration.quarterLength
                            
                            if 'Fraction' in str(dur):
                                dur = float(str(dur)[8:][:-1])
                            else:
                                dur = float(dur)
                            
                            sound_object_to_insert = (max(0.0, int(nt.pitch.ps)), dur)
                        elif isinstance(nt, chord.Chord):
                            c = []

                            for pitch in nt.pitches:
                                c.append(int(pitch.ps))

                            dur = nt.duration.quarterLength
                            
                            if 'Fraction' in str(dur):
                                dur = float(str(dur)[8:][:-1])
                            else:
                                dur = float(dur)

                            sound_object_to_insert = (tuple(sorted(c)), dur)

                        if first_sound_object is None:
                            first_sound_object = sound_object_to_insert

                        self.handle_insertion(prev_sound_object, sound_object_to_insert)

                    self.handle_insertion(sound_object_to_insert, ('R', "quarter"))
                    self.handle_insertion(('R', "quarter"), first_sound_object)
                except:
                    continue

            self.build_training_data()
            self.save_training_data(key_states="states_" + cur_color + "_" + cur_lad, 
                                    key_init_vector="init_prob_vector_" + cur_color + "_" + cur_lad,
                                    key_prob_matrix="transition_prob_matrix_" + cur_color + "_" + cur_lad)

        print('DONE')


    def build_training_data(self):
        self.build_initial_probability_vector()
        self.build_transition_probability_matrix()

    def build_initial_probability_vector(self):
        self.initial_probability_vector = np.array(list(init_prob for init_prob in self.states_appearances_dict.values()))
        self.initial_probability_vector = self.initial_probability_vector/self.initial_probability_vector.sum(keepdims=True)
        self.initial_probability_vector = np.cumsum(self.initial_probability_vector)

    def build_transition_probability_matrix(self):
        list_dimension = len(self.states)
        self.transition_probability_matrix = np.zeros((list_dimension,list_dimension), dtype=float)

        for i, sound_object in enumerate(self.states):
            for j, transition_sound_object in enumerate(self.states):
                if transition_sound_object in self.states_transition_dict[sound_object]:
                    self.transition_probability_matrix[i][j] = self.states_transition_dict[sound_object][transition_sound_object]

        self.transition_probability_matrix = self.transition_probability_matrix/self.transition_probability_matrix.sum(axis=1,keepdims=True)
        self.transition_probability_matrix = np.cumsum(self.transition_probability_matrix,axis=1)


    def handle_insertion(self, prev_sound_object, sound_object_to_insert):
        if sound_object_to_insert is not None and sound_object_to_insert[0] is not None:
            if prev_sound_object is not None and prev_sound_object[0] is not None:
                self.insert(self.states_transition_dict, prev_sound_object, sound_object_to_insert)
            if sound_object_to_insert not in self.states and sound_object_to_insert != ('R', "quarter"):
                self.states.append(sound_object_to_insert)

            if sound_object_to_insert in self.states_appearances_dict:
                self.states_appearances_dict[sound_object_to_insert] = self.states_appearances_dict[sound_object_to_insert] + 1
            else:
                self.states_appearances_dict[sound_object_to_insert] = 1

    def insert(self, dict, value1, value2):
        if value1 in dict:
            if value2 in dict[value1]:
                dict[value1][value2] = dict[value1][value2] + 1
            else:
                dict[value1][value2] = 1
        else:
            dict[value1] = {}
            dict[value1][value2] = 1

    def save_training_data(self, key_states:str="states", key_init_vector:str="init_prob_vector", key_prob_matrix:str="transition_prob_matrix"):
        redis_set(key_states, self.states, False)
        redis_set(key_init_vector, self.initial_probability_vector, False)
        redis_set(key_prob_matrix, self.transition_probability_matrix, False)

'''
 def get_bpm_time_signature(self, path:str):
        file = mido.MidiFile(path)

        for track in file.tracks:
            for msg in track:
                if msg.type == "set_tempo":
                    print(msg)

                if msg.type == "time_signature":
                    print(msg)
                    '''
   


#p = Parser(Constants.ColorsPath)
#p.parse()