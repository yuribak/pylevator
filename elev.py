import math
import random
import time

from asciimatics.effects import Sprite
from asciimatics.paths import Path
from asciimatics.renderers import StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen

SECOND = 1.

floors = 10
elev_count = 5
elev_w = 5

frame_w, frame_h, frame_x, frame_y = 30, floors + 2, 3, 3
frame_x2, frame_y2 = frame_x + frame_w - 1, frame_y + frame_h - 1


class Elevator(object):
    IDLE = 0b0
    SEND = 0b1
    FETCH = 0b10

    def __init__(self):
        self.pos = 0
        self.load = 0
        self.state = Elevator.IDLE
        self.target = random.randint(0, floors - 1)


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
        s.print_at(c, frame_x2 - (elev_w - 1) * (i + 1) + elev_w / 2, frame_x + frame_h - 2 - n)

    def move_elevators(elevators):

        for i, e in enumerate(elevators):
            if e.pos < e.target:
                pos_d = 1
            elif e.pos > e.target:
                pos_d = -1
            else:
                pos_d = 0

            print_elevator(i, e.pos, c=' ')
            e.pos += pos_d
            print_elevator(i, e.pos)

    elevators = [Elevator() for _ in xrange(elev_count)]

    while True:

        current_frame = time.time()

        move_elevators(elevators)

        s.refresh()

        time.sleep(SECOND - (time.time() - current_frame))


Screen.wrapper(main)
