import random

from utils import getLogger

logger = getLogger(__name__, 'strategy.log')


def next_stop_sequential(pos, load, floors, ctx):
    return (pos + 1) % len(floors)


def next_stop_random(pos, load, floors, ctx):
    return random.randint(0, len(floors) - 1)


def next_stop_real(pos, load, floors, ctx):
    going_up = ctx.setdefault('going_up', True)

    def up():
        above = [r for r in load if r > pos]
        if above:
            return min(above)

    def down():
        bellow = [r for r in load if r < pos]
        if bellow:
            return max(bellow)

    funcs = [down, up]
    target = funcs[going_up]()

    if target is None:
        going_up = not going_up
        target = funcs[going_up]()

    if target is None:
        waiting = [i for i, f in enumerate(floors) if f and i != pos]
        if waiting:
            target = min(waiting, key=lambda x: abs(pos - x))

            going_up = target > pos

    if target is None:
        target = pos

    ctx['going_up'] = going_up
    logger.trace('[%d:%d]%s>%d ' + str(load), 1, pos, '^' if going_up else 'v', target)
    return target


def next_stop(pos, load, floors, ctx):
    """

    :param pos: current position (floor) of the elevator
    :param load: list of ints representing the targets of current passengers
    :param floors: list of ints representing number of people waiting on each floor
    :param ctx: dict for persisting data between repeated calls of this function
    :return: target floor (int), None to stop on current floor
    """

    pass


next_stop = next_stop_real
