import random
import time
from functools import total_ordering
from itertools import count

from asciimatics.screen import Screen

from strategy import idle

FRAME_W = 150
ELEV_W = 15

GAME_TIME = 5
GAME_SECOND = .2
RPS = 4


@total_ordering
class Rider(object):
    produced = 0
    delivered = 0
    riding = 0
    time_alive = 0.
    time_riding = 0.

    IDS = count()

    def __init__(self, target):
        Rider.produced += 1
        self.target = target
        self.birth_time = time.time()
        self.load_time = None
        self.death = self.birth_time + 20 * GAME_SECOND

        self.id = Rider.IDS.next()

    def __gt__(self, other):
        return self.target > other.target if isinstance(other, Rider) else self.target > other

    def __eq__(self, other):
        return self.target == other.target if isinstance(other, Rider) else self.target == other

    def __repr__(self):
        return str(self.target)

    def load(self):
        self.load_time = time.time()
        Rider.riding += 1
        pass

    def unload(self):
        Rider.delivered += 1
        Rider.riding -= 1
        t = time.time()
        Rider.time_alive += t - self.birth_time
        Rider.time_riding += t - self.load_time


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

    # load/unload riders

    def re_load(self, floor):
        re_load = []
        for r in self.load:
            if r == self.pos:
                r.unload()
                continue
            re_load.append(r)
        self.load = re_load

        d = self.CAPACITY - len(self.load)
        for r in floor[:d]:
            r.load()
            self.load.append(r)

        del floor[:d]

    def load(self):
        pass

    def send(self):
        pass

    def fetch(self):
        pass


def draw_rect(screen, w, h, x, y, hchar='#', vchar='|'):
    # top
    screen.move(x, y)
    screen.draw(x + w, y, char=hchar)

    # right
    screen.move(x + w - 1, y + 1)
    screen.draw(x + w - 1, y + h - 1, char=vchar)

    # bottom
    screen.move(x + w - 1, y + h - 1)
    screen.draw(x - 1, y + h - 1, char=hchar)

    # left
    screen.move(x, y + h - 2)
    screen.draw(x, y, char=vchar)


class Display(object):
    def __init__(self, screen, floor_count, elev_count):
        self.screen = screen
        self.floor_count = floor_count
        self.elev_count = elev_count

        self.frame_w, self.frame_h, self.frame_x, self.frame_y = FRAME_W, floor_count + 2, 3, 3
        self.frame_x2, self.frame_y2 = self.frame_x + self.frame_w - 1, self.frame_y + self.frame_h - 1

        # draw frame
        draw_rect(self.screen, self.frame_w, self.frame_h, self.frame_x, self.frame_y)

        # draw elevator shafts
        for i in xrange(elev_count):
            draw_rect(self.screen, ELEV_W, self.frame_h, self.frame_x2 - (ELEV_W - 1) * (i + 1), self.frame_y)

    def print_elevator(self, i, n, c='@', color=Screen.COLOUR_WHITE):
        # self.s.print_at(c, frame_x2 - (elev_w - 1) * (i + 1) + elev_w / 2, frame_y + frame_h - 2 - n, color)
        self.screen.print_at(c, self.frame_x2 - (ELEV_W - 1) * (i + 1) + 1, self.frame_y + self.frame_h - 2 - n, color)

    def update_display(self, elevators, floors):

        # elevator positions
        for i, e in enumerate(elevators):
            self.print_elevator(i, e.old_pos, c=' ' * (len(str(e)) + 2))
            self.print_elevator(i, e.pos, c=str(e), color=e.state)

        # rider counds
        for f in xrange(len(floors)):
            m = str(len(floors[f]))
            self.screen.print_at('    ', self.frame_x + 2, self.frame_y + self.frame_h - 2 - f)
            self.screen.print_at(m, self.frame_x + 2, self.frame_y + self.frame_h - 2 - f)

        self.screen.refresh()


class Game(object):
    def __init__(self, screen, floor_count, elev_count):

        self.display = Display(screen, floor_count, elev_count)

        self.floors = [list() for _ in xrange(floor_count)]
        self.elevators = [Elevator(random.randint(0, floor_count - 1)) for _ in xrange(elev_count)]

    def move_elevators(self):

        for i, e in enumerate(self.elevators):
            e.old_pos = e.pos

            if e.pos < e.target:
                e.pos += 1
            elif e.pos > e.target:
                e.pos -= 1
            else:
                e.pos = e.old_pos

    def generate_riders(self):
        pool = range(len(self.floors))
        for _ in xrange(RPS):
            s, t = random.sample(pool, 2)

            self.floors[s].append(Rider(t))

    def update_state(self):
        # IDLE
        for e in self.elevators:
            if e.state == Elevator.IDLE:
                e.re_load(self.floors[e.pos])
                t = idle(e, self.floors)
                e.target =  t if t is not None else e.pos

        self.move_elevators()

        for e in self.elevators:
            if e.pos == e.target:
                e.state = Elevator.IDLE
            else:
                if e.load:
                    e.state = Elevator.SEND
                else:
                    e.state = Elevator.FETCH

        self.generate_riders()

    def update(self):

        self.update_state()
        self.display.update_display(self.elevators, self.floors)


def main(s):
    floor_count = 20
    elev_count = 4

    g = Game(s, floor_count, elev_count)

    start_time = time.time()

    while time.time() < start_time + GAME_TIME:

        current_frame = time.time()

        g.update()

        d = GAME_SECOND - (time.time() - current_frame)
        if d > 0:
            time.sleep(d)


try:
    Screen.wrapper(main)
except KeyboardInterrupt:
    pass

print 'Riders:', Rider.produced
print 'Delivered', Rider.delivered
print 'Average alive time:', Rider.time_alive / Rider.produced
print 'Average ride time:', Rider.time_riding / Rider.delivered
