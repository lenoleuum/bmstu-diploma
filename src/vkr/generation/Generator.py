import numpy as np
import random
import datetime

import sys
sys.path.append('..')

from stats.Redis import redis_get_parsed
from constants.Constants import Constants

class Generator:
    def __init__(self):
        self.states, self.init_prob_vector, self.transition_matrix_vector = dict(), dict(), dict()

        for color in Constants.MainColors:
            self.states[color] = redis_get_parsed("states_" + color)
            self.init_prob_vector[color] = redis_get_parsed("init_prob_vector_" + color)
            self.transition_matrix_vector[color] = redis_get_parsed("transition_prob_matrix_" + color)

        
    @staticmethod
    def find_nearest_above(my_array, target):
        diff = my_array - target
        mask = np.ma.less(diff, 0)
        
        if np.all(mask):
            return None
        
        masked_diff = np.ma.masked_array(diff, mask)
        return masked_diff.argmin()

    def generate(self, color, length:int = 100):
        print("[generate]")

        generated_fragment = [None] * length

        note_prob = random.uniform(0, 1)
        note_index = self.find_nearest_above(self.init_prob_vector[color], note_prob)
        curr_index = 0

        while (curr_index < length):
            note_prob = random.uniform(0, 1)

            note_index = self.find_nearest_above(self.transition_matrix_vector[color][note_index], note_prob)

            generated_fragment[curr_index] = self.states[color][note_index]
            curr_index += 1

        print("DONE")

        return generated_fragment
    