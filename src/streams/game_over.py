from module.pico2d import *
from module.functions import *
from module.constants import *

import module.framework as framework
from streams import game
from streams import main

__all__ = [
    "name", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "gameover_state"
alpha: float = 0
rpush: float = 0
tpush: float = 0

# noinspection PyGlobalUndefined
def enter():
    global alpha, tpush
    tpush = 0

def exit():
    pass


def update(frame_time):
    global alpha, rpush, tpush
    if tpush < 3:
        alpha = bezier4(tpush / 3, 0.21, 0.61, 0.35, 1)
        tpush += frame_time * 0.9
    else:
        alpha = 1
        tpush = 3


def draw(frame_time):
    global alpha
    clear_canvas()
    game.draw_clean()
    draw_set_color(0, 0, 0)
    draw_set_alpha(alpha)
    draw_rectangle(0, 0, screen_width, screen_height)
    framework.draw_text("Game Over", screen_width / 2, screen_height / 2, scale = 2)
    update_canvas()


def handle_events(frame_time):
    bevents = get_events()
    for event in bevents:
        if event.type == SDL_QUIT:
            framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_p) or (event.type, event.key) == (
                    SDL_KEYDOWN, SDLK_ESCAPE):
                framework.quit()


def pause():
    pass


def resume():
    pass
