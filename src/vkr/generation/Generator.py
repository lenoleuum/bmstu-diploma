import numpy as np
import random
import datetime

import sys
sys.path.append('..')

from analyze.Redis import redis_get_parsed
from constants.Constants import Constants

class Generator:
    def __init__(self):
        self.states, self.init_prob_vector, self.transition_matrix_vector = dict(), dict(), dict()

        for color in Constants.MainColors:
            self.states[color] = dict()
            self.init_prob_vector[color] = dict()
            self.transition_matrix_vector[color] = dict()
            for lad in Constants.Lads:
                self.states[color][lad] = redis_get_parsed("states_" + color + "_" + lad)
                self.init_prob_vector[color][lad] = redis_get_parsed("init_prob_vector_" + color + "_" + lad)
                self.transition_matrix_vector[color][lad] = redis_get_parsed("transition_prob_matrix_" + color + "_" + lad)

        
    @staticmethod
    def find_nearest_above(my_array, target):
        diff = my_array - target
        mask = np.ma.less(diff, 0)
        
        if np.all(mask):
            return None
        
        masked_diff = np.ma.masked_array(diff, mask)
        return masked_diff.argmin()

    def generate(self, meta:dict, length:int = 100):
        print("[generate]")
        
        color = meta['color']
        lad = meta['lad']

        print(color, lad)

        generated_fragment = [None] * length

        note_prob = random.uniform(0, 1)
        note_index = self.find_nearest_above(self.init_prob_vector[color][lad], note_prob)

        curr_index = 0

        while (curr_index < length):
            note_prob = random.uniform(0, 1)

            note_index = self.find_nearest_above(self.transition_matrix_vector[color][lad][note_index], note_prob)

            generated_fragment[curr_index] = self.states[color][lad][note_index]
            curr_index += 1

        print("DONE")

        return generated_fragment