import numpy as np

from .Parse import create_key

class Parser:
    def __init__(self, _states_set: list, _states_dict: dict, _states_transition_dict: dict):
        self.states = _states_set
        self.states_appearances_dict = _states_dict
        self.states_transition_dict = _states_transition_dict

        # training data
        self.initial_probability_vector = None
        self.transition_probability_matrix = None


    def build_training_data(self):
        # начальное распределение вероятностей
        self.build_initial_probability_vector()
        # матрица переходных вероятностей
        self.build_transition_probability_matrix()


    def build_initial_probability_vector(self):
        self.initial_probability_vector = np.array(list(init_prob for init_prob in self.states_appearances_dict.values()))

        self.initial_probability_vector = self.initial_probability_vector/self.initial_probability_vector.sum(keepdims=True)

        # multinomial dist
        self.initial_probability_vector = np.cumsum(self.initial_probability_vector)

    def build_transition_probability_matrix(self):
        list_dimension = len(self.states)

        self.transition_probability_matrix = np.zeros((list_dimension,list_dimension), dtype=float)

        for i, sound_object in enumerate(self.states):
            for j, transition_sound_object in enumerate(self.states):
                if create_key(transition_sound_object) in self.states_transition_dict[create_key(sound_object)]:
                    self.transition_probability_matrix[i][j] = self.states_transition_dict[create_key(sound_object)][create_key(transition_sound_object)]

        self.transition_probability_matrix = self.transition_probability_matrix/self.transition_probability_matrix.sum(axis=1,keepdims=True)
        
        # multinomial dist
        self.transition_probability_matrix = np.cumsum(self.transition_probability_matrix,axis=1)

    def parse(self):
        print()


    def handle_insertion(self, prev_sound_object, sound_object_to_insert):
        if sound_object_to_insert is not None and sound_object_to_insert[0] is not None:
            if prev_sound_object is not None and prev_sound_object[0] is not None:
                self.insert(self.transition_probability_dict, prev_sound_object, sound_object_to_insert)
            if sound_object_to_insert not in self.states:
                self.states.append(sound_object_to_insert)

            if sound_object_to_insert in self.initial_transition_dict:
                self.initial_transition_dict[sound_object_to_insert] = self.initial_transition_dict[sound_object_to_insert] + 1
            else:
                self.initial_transition_dict[sound_object_to_insert] = 1

    def insert(self, dict, value1, value2):
        if value1 in dict:
            if value2 in dict[value1]:
                dict[value1][value2] = dict[value1][value2] + 1
            else:
                dict[value1][value2] = 1