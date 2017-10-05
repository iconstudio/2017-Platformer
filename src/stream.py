
import os
from pico2d import *

false = False
true = True

class null:
    def __bool__(self):
        return false

    def __abs__(self):
        return 0

    def __sizeof__(self):
        return 0

class gravitons:
    name = "None"

    depth = 0
    x, y = 0, 0

    gravity_current = 0
    gravity = 0

    sprite = null

    def __init__(self, ndepth = 0, nx = 0, ny = 0):
        self.depth = ndepth
        self.x, self.y = nx, ny

    def __str__(self):
        return self.name

open_canvas()
show_cursor()

while (true):
    pass


#grass = load_image('grass.png')
#character = load_image('run_animation.png')

close_canvas()
