from .Gamma import Gamma

import sys
sys.path.append("..")

from constants.Constants import GammaDies, GammaBb, Major, Minor, MajorLad, MinorLad


# todo: нормальный конвертер из связного списка в массив
class Tonality:
    def __init__(self, lad: str, tonica: str):
        self.lad = lad
        self.tonica = tonica

        # todo: разобраться с бемолями
        if 'b' in self.tonica:
            self.gamma = Gamma(GammaBb)
            self.gamma_seq = GammaBb
        else:
            self.gamma = Gamma()
            self.gamma_seq = GammaDies

        self.generate_gamma()

    def generate_gamma(self):
        gamma = Gamma(self.gamma_seq)
        gamma.create_gamma()

        lad_list = None

        if self.lad == Major:
            lad_list = MajorLad
        elif self.lad == Minor:
            lad_list = MinorLad

        g = Gamma(self.gamma_seq)
        g.create_gamma()
        cur = g.find_note(self.tonica)

        self.gamma.insert_end(self.tonica)

        for i in lad_list:
            if i == 1:
                cur = cur.next.next
            else:
                cur = cur.next

            self.gamma.insert_end(cur.data)

    def linked_list_to_list(self):
        res = []
        cur = self.gamma.head
        while cur.next is not self.gamma.head:
            res.append(cur.data)
            cur = cur.next

        return res
