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

time: float = 0
alpha: float = 0
hfont = None
option = {
    "volume_sfx": 8,
    "volume_mus": 5,
    "effect": True
}


def ease_out_elastic(arg0):
    """
    :param arg0: 0 ~ 1
    :return: 0 ~ 1
    """
    if arg0 is 0:
        return 0
    elif arg0 is 1:
        return 1

    p = 0.3
    s = p / 4

    return 2 ** (-10 * arg0 * math.sin((arg0 - s) * (2 * math.pi) / p) + 1)


def rewrite_option():
    global option
    with open(path_data + "option.json", 'w', encoding = "utf-8") as make_file:
        json.dump(option, make_file, ensure_ascii = False, indent = "\t")


# noinspection PyGlobalUndefined
def enter():
    global time, hfont
    time = 0
    hfont = load_font(path_font + "Contl___.ttf", 40)


def exit():
    global hfont
    del hfont

    framework.unpause()


def update(frame_time):
    global time, alpha

    if time < 2:
        alpha = ease_out_elastic(time / 2)
        time += frame_time
    else:
        alpha = 1
    time += frame_time


def draw(frame_time):
    global alpha, hfont

    clear_canvas()
    draw_set_alpha(alpha * 2)
    draw_set_color(255, 255, 255)
    draw_set_halign(1)
    draw_set_valign(1)
    framework.draw_text("Option", screen_width / 2, screen_height - 32, font = 2, scale = 2)

    draw_set_alpha(alpha)
    hfont.draw()
    framework.draw_text("Option", screen_width / 2, screen_height - 32, font = 2, scale = 2)

    update_canvas()


def handle_events(frame_time):
    bevents = get_events()
    for event in bevents:
        if event.type == SDL_QUIT:
            framework.quit()
        elif time > 1:
            if event.type == SDL_KEYDOWN:
                if event.key in (SDLK_z, SDLK_ESCAPE):
                    framework.pop_state()
                    audio_play("sndMenuSelect")


def pause():
    pass


def resume():
    pass
