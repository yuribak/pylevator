from asciimatics.screen import Screen
import time

def f(s):

    s.print_at('weeee',2,2, Screen.COLOUR_GREEN, Screen.A_BOLD)
    s.move(2,3)
    s.draw(8,3, char='#')
    s.refresh()
    time.sleep(5)

def draw_frame(s):
    w, h, x, y = 40, 25, 2, 2
    hchar = '#'
    vchar = '|'

    # top
    s.move(x-1,y-1)
    s.draw(x+w+1, y-1, char=hchar)

    # right
    s.move(x+w, y)
    s.draw(x+w, y+h, char=vchar)

    # bottom
    s.move(x+w, y+h)
    s.draw(x-2, y+h, char=hchar)

    # left
    s.move(x-1, y+h-1)
    s.draw(x-1, y-1, char=vchar)

    s.refresh()

    time.sleep(5)




Screen.wrapper(draw_frame)
