import Constants as const
from Tonality import Tonality


class Node:
    def __init__(self, data: str):
        self.data = data
        self.next = None
        self.prev = None
        self.parallel = None


class TonalityCircle:
    def __init__(self, seq: list):
        self.head = None
        self.tail = None
        self.seq = seq

    def is_empty(self):
        return self.head is None

    def insert_end(self, data: str):
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            # self.tail = new_node
            new_node.next = self.head
            # new_node.prev = self.tail
        else:
            cur = self.head

            while cur.next is not self.head:
                cur = cur.next

            cur.next = new_node
            new_node.prev = cur
            new_node.next = self.head

            self.head.prev = self.tail

    def insert_node_end(self, new_node: Node):
        if self.is_empty():
            self.head = new_node
            # self.tail = new_node
            new_node.next = self.head
            # new_node.prev = self.tail
            # print(new_node.data, new_node.prev.data, new_node.next.data)
        else:
            cur = self.head

            while cur.next is not self.head:
                cur = cur.next

            cur.next = new_node
            new_node.prev = cur
            new_node.next = self.head

            self.head.prev = self.tail

            # print(new_node.data, new_node.prev.data, new_node.next.data)

    def create_tonality_circle(self):
        tonality_seq = self.seq

        for tonality in tonality_seq:
            node = Node(tonality)
            self.insert_node_end(node)

        self.tail = node
        self.head.prev = node

    def print_tonality_circle(self):
        cur = self.head
        print(cur.data)

        while cur.next != self.head:
            cur = cur.next
            print(cur.data)

    def find_tonality(self, tonality: Tonality):
        cur = self.head
        while cur.next != self.head:
            if cur.data == tonality.tonica:
                return cur
            cur = cur.next

        if cur.data == tonality.tonica:
            return cur

        return None


class QuartoQuintCircle:
    def __init__(self):
        self.major = None
        self.minor = None

    def create_circle(self):
        self.major = TonalityCircle(const.TonalitySequenceMajor)
        self.major.create_tonality_circle()

        self.minor = TonalityCircle(const.TonalitySequenceMinor)
        self.minor.create_tonality_circle()

        cur_major = self.major.head
        cur_minor = self.minor.head

        # cur_major.prev = self.major.tail
        # cur_minor.prev = self.minor.tail

        while cur_major.next != self.major.head:
            cur_major.parallel = cur_minor

            cur_major = cur_major.next
            cur_minor = cur_minor.next

        cur_major.parallel = cur_minor

        cur_major = self.major.head
        cur_minor = self.minor.head

        while cur_minor.next != self.minor.head:
            cur_minor.parallel = cur_major

            cur_major = cur_major.next
            cur_minor = cur_minor.next

        cur_minor.parallel = cur_major

    def get_tonality_by_offset(self, tonality: Tonality, offset: int):
        if offset > 0:
            if tonality.lad == const.Major:
                cur = self.major.find_tonality(tonality)

                for i in range(offset):
                    cur = cur.next

                return cur
            else:
                cur = self.minor.find_tonality(tonality)

                for i in range(offset):
                    cur = cur.next

                return cur
        else:
            if tonality.lad == const.Major:
                cur = self.major.find_tonality(tonality)

                for i in range(abs(offset)):
                    cur = cur.prev

                return cur
            else:
                cur = self.minor.find_tonality(tonality)

                for i in range(abs(offset)):
                    cur = cur.prev

                return cur

    def get_relatives(self, tonality: Tonality):
        if tonality.lad == const.Major:
            pos = self.major.find_tonality(tonality)

            t0 = Tonality(const.Major, pos.data)  # текущая тональность
            t1 = Tonality(const.Minor, pos.parallel.data)  # параллельная тональность (минор)
            t2 = Tonality(const.Major, pos.next.data)  # параллельная тональность правого соседа (минор)
            t3 = Tonality(const.Minor, pos.next.parallel.data)  # правый сосед (тоже мажор)
            t4 = Tonality(const.Major, pos.prev.data)  # левый сосед (тоже мажор)
            t5 = Tonality(const.Minor, pos.prev.parallel.data)  # параллельная тональность левого соседа (минор)

            t = self.get_tonality_by_offset(tonality, -5)
            t6 = Tonality(const.Major, t.data)
            t7 = Tonality(const.Minor, t.parallel.data)

            return list([t0, t1, t2, t3, t4, t5, t6, t7])

        else:
            pos = self.minor.find_tonality(tonality)

            t0 = Tonality(const.Minor, pos.data)  # текущая тональность
            t1 = Tonality(const.Major, pos.parallel.data)  # параллельная тональность (мажор)
            t2 = Tonality(const.Minor, pos.next.data)  # правый сосед (тоже минор)
            t3 = Tonality(const.Major, pos.next.parallel.data)  # параллельная тональность правого соседа (мажор)
            t4 = Tonality(const.Minor, pos.prev.data)  # левый сосед (тоже минор)
            t5 = Tonality(const.Major, pos.prev.parallel.data)  # параллельная тональность левого соседа (мажор)

            t = self.get_tonality_by_offset(tonality, -5)
            t6 = Tonality(const.Minor, t.data)
            t7 = Tonality(const.Major, t.parallel.data)

            return list([t0, t1, t2, t3, t4, t5, t6, t7])