from module.pico2d import *
from module.constants import *

import module.framework as framework

from module.audio import *

import json

__all__ = [
    "name", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "option_state"

option = {
    "volume_sfx": 8,
    "volume_mus": 5,
    "effect": True
}


def rewrite_option():
    global option
    with open(path_data + "option.json", 'w', encoding = "utf-8") as make_file:
        json.dump(option, make_file, ensure_ascii = False, indent = "\t")


# noinspection PyGlobalUndefined
def enter():
    pass


def exit():
    framework.unpause()


def update(frame_time):
    pass


def draw(frame_time):
    clear_canvas()
    draw_set_alpha(1)
    draw_set_color(255, 255, 255)
    draw_set_halign(1)
    draw_set_valign(1)
    framework.draw_text("Paused", screen_width / 2, 32, scale = 2)
    update_canvas()


def handle_events(frame_time):
    bevents = get_events()
    for event in bevents:
        if event.type == SDL_QUIT:
            framework.quit()
        else:
            if event.type == SDL_KEYDOWN:
                if event.key in (SDLK_RETURN, SDLK_ESCAPE):
                    framework.pop_state()
                    audio_play("sndMenuSelect")


def pause():
    pass


def resume():
    pass
