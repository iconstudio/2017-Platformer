from pico2d import *
from functions import *

import framework
import game

name = "main_state"

def enter():
    open_canvas(screen_width, screen_height, true)
    pass

def exit():
    close_canvas()
    pass

def update():
    delay(0.01)
    pass

def draw():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                framework.quit()

def pause():
    pass

def resume():
    pass