import random
from utils import getLogger

logger = getLogger(__name__, 'idle.log')


def idle_sequential(e, floors):
    e.target = (e.pos + 1) % len(floors)


def idle_random(e, floors):
    e.target = random.randint(0, len(floors) - 1)


def idle_real(e, floors):
    going_up = e.ctx.setdefault('going_up', True)

    def up():
        above = [r for r in e.load if r > e.pos]
        if above:
            return min(above).target

    def down():
        bellow = [r for r in e.load if r < e.pos]
        if bellow:
            return max(bellow).target

    funcs = [down, up]
    target = funcs[going_up]()

    if target is None:
        going_up = not going_up
        target = funcs[going_up]()

    if target is None:
        waiting = [f for f in range(len(floors)) if floors[f] and f != e.pos]
        if waiting:
            going_up = e.target > e.pos
            target = min(waiting, key=lambda x: abs(e.pos - x))

    if target is None:
        target = e.pos

    e.ctx['going_up'] = going_up
    logger.trace('[%d:%d]%s>%d '+str(e.load), e.id, e.pos, '^' if going_up else 'v', target)
    return target


idle = idle_real
