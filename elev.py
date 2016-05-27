
import random
import time

from asciimatics.screen import Screen

SECOND = 1.


floor_count = 10
floors = [list() for _ in xrange(floor_count)]
elev_count = 4
elev_w = 5

RPS = 3

frame_w, frame_h, frame_x, frame_y = 30, floor_count + 2, 3, 3
frame_x2, frame_y2 = frame_x + frame_w - 1, frame_y + frame_h - 1


class Elevator(object):
    IDLE = 0b0
    SEND = 0b1
    FETCH = 0b10

    def __init__(self):
        self.pos = 0
        self.new_pos = 0
        self.load = 0
        self.state = Elevator.IDLE
        self.target = random.randint(0, floor_count - 1)

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

    def print_elevator(i, n, c='@'):
        s.print_at(c, frame_x2 - (elev_w - 1) * (i + 1) + elev_w / 2, frame_y + frame_h - 2 - n)

    def move_elevators(elevators):

        for i, e in enumerate(elevators):
            e.pos = e.new_pos

            if e.pos < e.target:
                e.new_pos = e.pos+1
            elif e.pos > e.target:
                e.new_pos = e.pos-1
            else:
                e.new_pos = e.pos

    def generate_riders():
        pool = range(floor_count)
        for _ in xrange(RPS):
            s,t = random.sample(pool, 2)
            floors[s].append(t)

    elevators = [Elevator() for _ in xrange(elev_count)]

    while True:

        current_frame = time.time()

        # update game state
        move_elevators(elevators)
        generate_riders()

        # update display
        for i, e in enumerate(elevators):
            print_elevator(i, e.pos, c=' ')
            print_elevator(i, e.new_pos)

        for f in xrange(len(floors)):
            m = str(len(floors[f]))
            s.print_at(m, frame_x+2, frame_y + frame_h - 2 - f)

        s.refresh()

        d = SECOND - (time.time() - current_frame)
        if d > 0:
            time.sleep(d)



Screen.wrapper(main)
