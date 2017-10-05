
import os
from pico2d import *

# Global Constants
false = False
true = True
running = true


class null:
    def __bool__(self):
        return false

    def __abs__(self):
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

# Event
def handle_events():
    global running
    global x
    anevents = get_events()
    for event in anevents:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                x += 20
            elif event.key == SDLK_LEFT:
                x -= 20
            elif event.key == SDLK_ESCAPE:
                running = False

# MAIN
grass = load_image('grass.png')
character = load_image('run_animation.png')

x = 0
frame = 0
while running:
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 0, 100, 100, x, 90)
    update_canvas()
    frame = (frame + 1) % 8

    delay(0.05)
    handle_events()

close_canvas()
