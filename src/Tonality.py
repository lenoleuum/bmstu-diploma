import Constants as const


class Node:
    def __init__(self, data: str):
        self.data = data
        self.next = None


class Gamma:
    def __init__(self, gamma_seq: list=const.GammaDies):
        self.head = None
        self.tail = None
        self.gamma = gamma_seq

    def is_empty(self):
        return self.head is None;

    def insert_end(self, data: str):
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head
        else:
            cur = self.head

            while cur.next is not self.head:
                cur = cur.next

            cur.next = new_node
            new_node.next = self.head

    def create_gamma(self):
        #gamma = const.Gamma
        for note in self.gamma:
            self.insert_end(note)

    def print_gamma(self):
        cur = self.head
        print(cur.data, cur.next.data)

        while cur.next != self.head:
            cur = cur.next
            print(cur.data, cur.next.data)

    def find_note(self, note: str):
        cur = self.head
        while cur.next != self.head:
            if cur.data == note:
                return cur
            cur = cur.next

        if cur.data == note:
            return cur

        return None

# todo: нормальный конвертер из связного списка в массив
class Tonality:
    def __init__(self, lad: str, tonica: str):
        self.lad = lad
        self.tonica = tonica

        # todo: разобраться с бемолями
        if 'b' in self.tonica:
            self.gamma = Gamma(const.GammaBb)
            self.gamma_seq = const.GammaBb
        else:
            self.gamma = Gamma()
            self.gamma_seq = const.GammaDies

        self.generate_gamma()

    def generate_gamma(self):
        gamma = Gamma(self.gamma_seq)
        gamma.create_gamma()

        lad_list = None

        if self.lad == const.Major:
            lad_list = const.MajorLad
        elif self.lad == const.Minor:
            lad_list = const.MinorLad

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
