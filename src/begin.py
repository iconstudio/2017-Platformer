from pico2d import *
from functions import *

import framework
import main

name = "begin_state"
logo_time = 0

def enter():
    global bg, logo
    open_canvas(screen_width, screen_height, true)
    hide_cursor()
    hide_lattice()
    bg = load_image("..\\res\\img\\bg_black.png")
    logo = load_image("..\\res\\img\\logo.png")

def exit():
    if logo_time > 10:
        global bg, logo
        del bg, logo
        close_canvas()

def update():
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0
        framework.push_state(main)
    logo_time += 0.01
    delay(0.01)

def draw():
    global bg, logo
    clear_canvas()
    bg.draw(screen_width / 2, screen_height / 2)
    logo.draw(screen_width / 2, screen_height / 2)
    update_canvas()

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
