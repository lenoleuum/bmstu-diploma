import numpy as np
import random
import datetime

import sys
sys.path.append('..')

from stats.Redis import redis_get_parsed
from constants.Constants import WorkDir

class Generator:
    def __init__(self):
        self.states = redis_get_parsed('states')
        self.init_prob_vector = redis_get_parsed("init_prob_vector")
        self.transition_matrix_vector = redis_get_parsed("transition_prob_matrix")

        
    @staticmethod
    def find_nearest_above(my_array, target):
        diff = my_array - target
        mask = np.ma.less(diff, 0)
        # We need to mask the negative differences and zero
        # since we are looking for values above
        if np.all(mask):
            return None # returns None if target is greater than any value
        
        masked_diff = np.ma.masked_array(diff, mask)
        return masked_diff.argmin()

    def generate(self, length:int = 100):
        generated_fragment = [None] * length

        note_prob = random.uniform(0, 1)
        note_index = self.find_nearest_above(self.init_prob_vector, note_prob)
        curr_index = 0

        while (curr_index < length):
            note_prob = random.uniform(0, 1)

            note_index = self.find_nearest_above(self.transition_matrix_vector[note_index], note_prob)

            generated_fragment[curr_index] = self.states[note_index]
            curr_index += 1

        return generated_fragment