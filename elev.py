
import random
import time

from asciimatics.screen import Screen

SECOND = 1.


floor_count = 8 
floors = [list() for _ in xrange(floor_count)]
elev_count = 2
elev_w = 15

RPS = 4

frame_w, frame_h, frame_x, frame_y = 80, floor_count + 2, 3, 3
frame_x2, frame_y2 = frame_x + frame_w - 1, frame_y + frame_h - 1


class Elevator(object):

    CAPACITY = 12

    IDLE = 3
    LOAD = 1
    SEND = 2
    FETCH = 5

    def __init__(self):
        self.pos = 0
        self.old_pos = 0
        self.load = []
        self.state = Elevator.IDLE
        self.target = random.randint(0, floor_count - 1)

    def __repr__(self):
        return '[{}>{}]'.format(len(self.load), self.target)

    def idle(self):

        # position
        # list of waiting riders
        # other elevators?
        return # (target)
        pass

    def load(self):
        pass

    def send(self):
        pass

    def fetch(self):
        pass


def idle_sequential(e):
    e.target = (e.pos+1)%floor_count

def idle_random(e):
    e.target = random.randint(0,len(floors)-1)

idle = idle_random

def main(s):

    def draw_rect(w, h, x, y, hchar='#', vchar='|'):
        # top
        s.move(x, y)
        s.draw(x + w, y, char=hchar)

        # right
        s.move(x + w - 1, y + 1)
        s.draw(x + w - 1, y + h - 1, char=vchar)

        # bottom
        s.move(x + w - 1, y + h - 1)
        s.draw(x - 1, y + h - 1, char=hchar)

        # left
        s.move(x, y + h - 2)
        s.draw(x, y, char=vchar)

    # draw frame
    draw_rect(frame_w, frame_h, frame_x, frame_y)

    # draw elevator shafts
    for i in xrange(elev_count):
        draw_rect(elev_w, frame_h, frame_x2 - (elev_w - 1) * (i + 1), frame_y)

    def print_elevator(i, n, c='@', color=Screen.COLOUR_WHITE):
        #s.print_at(c, frame_x2 - (elev_w - 1) * (i + 1) + elev_w / 2, frame_y + frame_h - 2 - n, color)
        s.print_at(c, frame_x2 - (elev_w - 1) * (i + 1)+1, frame_y + frame_h - 2 - n, color)

    def move_elevators(elevators):

        for i, e in enumerate(elevators):
            e.old_pos = e.pos

            if e.pos < e.target:
                e.pos = e.old_pos+1
            elif e.pos > e.target:
                e.pos = e.old_pos-1
            else:
                e.pos = e.old_pos

    def generate_riders():
        pool = range(floor_count)
        for _ in xrange(RPS):
            s,t = random.sample(pool, 2)

            floors[s].append(t)

    elevators = [Elevator() for _ in xrange(elev_count)]

    while True:

        current_frame = time.time()

        # update game state

        for e in elevators:
            if e.state == Elevator.IDLE:
                e.load = [r for r in e.load if r != e.pos]
                d = e.CAPACITY - len(e.load)
                e.load += floors[e.pos][:d]
                del floors[e.pos][:d]
                idle(e)

        move_elevators(elevators)

        for e in elevators:
            if e.pos == e.target:
                e.state = Elevator.IDLE
            else:
                e.state = Elevator.FETCH

        generate_riders()

        # update display
        for i, e in enumerate(elevators):
            print_elevator(i, e.old_pos, c=' '*len(str(e)))
            print_elevator(i, e.pos, c=str(e), color=e.state)

        for f in xrange(len(floors)):
            m = str(len(floors[f]))
            s.print_at(m, frame_x+2, frame_y + frame_h - 2 - f)

        s.refresh()

        d = SECOND - (time.time() - current_frame)
        if d > 0:
            time.sleep(d)


Screen.wrapper(main)
