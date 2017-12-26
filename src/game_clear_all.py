from pico2d import *
from functions import *
from constants import *

import framework

from sprite import *
from audio import *

import game

__all__ = [
    "name", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "gamecomplete_state"
alpha: float = 0
dmode = 0
tpush: float = 0


# noinspection PyGlobalUndefined
def enter():
    global alpha, dmode, tpush
    alpha = 0
    dmode = 0
    tpush = 0

    audio_play("musCredit")


def exit():
    pass


def update(frame_time):
    global alpha, dmode, tpush
    if dmode == 0:
        if tpush < 4:
            alpha = bezier4(tpush / 4, 0.21, 0.61, 0.35, 1)
            tpush += frame_time
        else:
            alpha = 1
            tpush = 5
            dmode = 1


def draw(frame_time):
    game.draw_clean(frame_time)
    global alpha
    clear_canvas()
    draw_set_alpha(alpha)
    draw_set_color(0, 0, 0)
    draw_rectangle(0, 0, screen_width, screen_height)

    credit = sprite_get("sCredit")
    draw_sprite(credit, 0, 320, 240, 1, 1, 0, alpha)
    update_canvas()


def handle_events(frame_time):
    global tpush

    bevents = get_events()
    for event in bevents:
        if event.type == SDL_QUIT or (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            framework.quit()
        elif tpush > 1.2:
            if (event.type, event.key) == (SDL_KEYDOWN, ord('x')):
                framework.quit()


def pause():
    pass


def resume():
    pass
