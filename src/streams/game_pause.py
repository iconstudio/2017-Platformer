from module.pico2d import *
from module.constants import *

import module.framework as framework
from streams import game

__all__ = [
    "name", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "pause_state"

# noinspection PyGlobalUndefined
def enter():
    global logo
    logo = load_image(path_image + "logo.png", 80, 80)


def exit():
    global logo
    del logo

def update(frame_time):
    pass


def draw():
    global logo
    clear_canvas()
    game.draw_clean()
    logo.draw(screen_width / 2, screen_height / 2)
    update_canvas()


def handle_events(frame_time):
    bevents = get_events()
    for event in bevents:
        if event.type == SDL_QUIT:
            framework.pop_state()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_p) or (event.type, event.key) == (
            SDL_KEYDOWN, SDLK_ESCAPE):
                framework.pop_state()


def pause():
    pass


def resume():
    pass
