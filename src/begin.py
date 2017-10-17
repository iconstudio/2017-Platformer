from pico2d import *
from .module import functions

import framework
import main

name = "begin_state"

def enter():
    global image
    open_canvas()
    image = load_image("kpu_credit.png")

def exit():
    if logo_time > 10:
        global image
        del image
        close_canvas()

def update():
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0
        framework.push_state(main)
    delay(0.01)
    logo_time += 0.01
    pass

def draw():
    global image
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    pass

def pause():
    pass

def resume():
    pass
