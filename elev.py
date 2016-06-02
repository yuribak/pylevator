import random
from time import sleep

from asciimatics.screen import Screen

from model import Elevator, Rider
from strategy import next_stop
from utils import Timer

FRAME_W = 150
ELEV_W = 11


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
    def __init__(self, screen, floor_count, elev_count, game):
        self.screen = screen
        self.floor_count = floor_count
        self.elev_count = elev_count
        self.game = game

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
            m = len(floors[f])
            self.screen.print_at(' ' * 20, self.frame_x + 2, self.frame_y + self.frame_h - 2 - f)

            label = '{:<10}{:<3}({})'.format('*' * min(m, 10), '...' if m > 10 else '', m)
            self.screen.print_at(label, self.frame_x + 2, self.frame_y + self.frame_h - 2 - f)

        # stats:
        self.screen.print_at(' ' * self.frame_w, self.frame_x, self.frame_y - 1)
        self.screen.print_at(
            'Time: {:<6.1f}, Produced: {:<6}, Delivered: {:<6} ({:<2.0f}%), Died: {:<6} ({:2.0f}%)'.format(
                Timer.timer(self.game).time(),
                self.game.produced,
                self.game.delivered,
                100.0 * self.game.delivered / self.game.produced,
                self.game.died,
                100.0 * self.game.died / self.game.produced,
            ),
            self.frame_x,
            self.frame_y - 1
        )

        self.screen.refresh()


class Game(object):
    def __init__(self, screen, floor_count, elev_count, life_expectancy, rps):

        self.life_expectancy = life_expectancy
        self.rps = rps

        self.display = Display(screen, floor_count, elev_count, self)

        self.floors = [list() for _ in xrange(floor_count)]
        self.elevators = [Elevator(random.randint(0, floor_count - 1)) for _ in xrange(elev_count)]

        self.timer = Timer.timer(self)

        self.delivered = 0
        self.produced = 0
        self.died = 0

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
        for _ in xrange(self.rps):
            s, t = random.sample(pool, 2)
            self.floors[s].append(Rider(t))
            self.floors[s][-1].init_time = self.timer.time()
            self.produced += 1

    def update_state(self):
        self.handle_stopped()
        self.kill_riders()
        self.move_elevators()
        self.update_elevator_state()
        self.generate_riders()

    def handle_stopped(self):
        for e in self.elevators:
            if e.state == Elevator.IDLE:
                # reload
                d = len(e.load)
                e.load = [r for r in e.load if r.target != e.pos]
                d -= len(e.load)
                self.delivered += d

                d = e.CAPACITY - len(e.load)
                e.load += self.floors[e.pos][:d]
                del self.floors[e.pos][:d]

                # compute next stop
                t = next_stop(e.pos, [r.target for r in e.load], map(len, self.floors), e.ctx)
                e.target = t if t is not None else e.pos
                assert 0 <= e.target < len(self.floors)

    def kill_riders(self):
        now = self.timer.time()
        for floor in self.floors:
            d = len(floor)
            floor[:] = [r for r in floor if now - r.init_time < self.life_expectancy]
            d -= len(floor)
            self.died += d

    def update_elevator_state(self):
        for e in self.elevators:
            if e.pos == e.target:
                e.state = Elevator.IDLE
            else:
                if e.load:
                    e.state = Elevator.SEND
                else:
                    e.state = Elevator.FETCH

    def update(self):

        self.update_state()
        self.display.update_display(self.elevators, self.floors)


def elev(
        life_expectancy,
        floor_count,
        elev_count,
        fast_mode,
        game_time,
        game_second,
        rps
):
    def main(s):

        g = Game(s, floor_count, elev_count, life_expectancy, rps)

        t = Timer.timer(g)

        while t.time() < game_time:

            current_frame = t.time()

            g.update()

            d = game_second - (t.time() - current_frame)
            if d > 0:
                if fast_mode:
                    t.skip(d)
                else:
                    sleep(d)

    try:
        Screen.wrapper(main)
    except KeyboardInterrupt:
        pass


elev(
    life_expectancy=4,
    floor_count=40,
    elev_count=12,
    fast_mode=False,
    game_time=100,
    game_second=.2,
    rps=4
)
