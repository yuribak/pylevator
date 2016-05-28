import random


def idle_sequential(e, floors):
    e.target = (e.pos + 1) % len(floors)


def idle_random(e, floors):
    e.target = random.randint(0, len(floors) - 1)


def idle_real(e, floors):
    going_up = e.ctx.setdefault('going_up', True)
    target = None
    if going_up:
        up = [r for r in e.load if r > e.pos]
        if up:
            target = min(up).target
        else:
            going_up = False
    if not going_up:
        down = [r for r in e.load if r < e.pos]
        if down:
            target = max(down).target
        else:
            going_up = True
    if target is not None:
        e.target = target
        e.ctx['going_up'] = going_up
    else:
        waiting = [f for f in range(len(floors)) if floors[f]]
        if waiting:
            e.target = min(waiting, key=lambda x: abs(e.pos - x))
            e.ctx['going_up'] = e.target > e.pos


idle = idle_real
