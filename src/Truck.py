
class Truck(object):
    def __init__(self, po, size, live, time):
        self.po = po
        self.size = size
        self.live = live
        self.time = time

    def incrementTime(self):
        self.time += 1

    def __lt__(self, other):
        return self.size < other.size and self.time <= other.time
