import sys
sys.path.append("..")

from constants.Constants import GammaDies, GammaBb, Major, Minor, MajorLad, MinorLad


class Node:
    def __init__(self, data: str):
        self.data = data
        self.next = None

class Gamma:
    def __init__(self, gamma_seq: list=GammaDies):
        self.head = None
        self.tail = None
        self.gamma = gamma_seq

    def is_empty(self):
        return self.head is None

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