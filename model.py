from functools import total_ordering
from itertools import count


@total_ordering
class Rider(object):
    IDS = count()

    def __init__(self, target):
        self.target = target
        self.id = Rider.IDS.next()

    def __gt__(self, other):
        return self.target > other.target if isinstance(other, Rider) else self.target > other

    def __eq__(self, other):
        return self.target == other.target if isinstance(other, Rider) else self.target == other

    def __repr__(self):
        return str(self.target)


class Elevator(object):
    CAPACITY = 12

    IDLE = 3
    LOAD = 1
    SEND = 2
    FETCH = 5

    IDS = count()

    def __init__(self, pos):
        self.pos = pos
        self.old_pos = 0
        self.load = []
        self.state = Elevator.IDLE
        self.target = 0
        self.ctx = {}
        self.id = Elevator.IDS.next()

    def __repr__(self):
        return '[{}>{}]'.format(len(self.load), self.target)
