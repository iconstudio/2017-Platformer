from module.pico2d import *
from module.constants import *

import module.framework as framework
from module.keycode import *

from module.audio import *

import math
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

selected = 0
# 0: Music, 1: Sfx, -1: None
choice_state = -1


def ease_out_sine(arg0):
    """
    :param arg0: 0 ~ 1
    :return: 0 ~ 1
    """
    if arg0 is 0:
        return 0
    elif arg0 is 1:
        return 1

    return math.sin(arg0 * math.pi / 2)


def rewrite_option():
    option = {
        "volume_sfx": audio_get_volume_sfx_global(),
        "volume_mus": audio_get_volume_music_global(),
        "effect": True
    }

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
        alpha = ease_out_sine(time / 2)
        time += frame_time
    else:
        alpha = 1
    time += frame_time


def draw(frame_time):
    global alpha, hfont, choice_state, selected

    hw, hh = screen_width / 2, screen_height / 2
    clear_canvas()
    draw_set_alpha(min(1, alpha * 2))
    draw_set_color(255, 255, 255)
    draw_set_halign(1)
    draw_set_valign(1)
    framework.draw_text("Option", hw, screen_height - 32, font = 2, scale = 2)

    dcol_sfx = (255, 255, 255)
    dcol_mus = (0, 0, 0)
    draw_set_alpha(alpha)
    dx1, dy1, dx2, dy2 = hw - 225, hh - 20, hw - 75, hh + 20
    draw_value = audio_get_volume_sfx_global()

    if selected == 1:
        dx1 += 300
        dx2 += 300
        draw_value = audio_get_volume_music_global()
    else:
        dcol_sfx = (0, 0, 0)
        dcol_mus = (255, 255, 255)
    draw_rectangle(dx1, dy1, dx2, dy2)

    draw_set_color(*dcol_sfx)
    hfont.draw(hw - 150, hh, "Sound")
    draw_set_color(*dcol_mus)
    hfont.draw(hw + 150, hh, "Music")

    if choice_state != -1:
        draw_set_color(255, 255, 255)
        draw_rectangle(hw - 150, hh + 60, hw + 150, hh + 100)
        draw_set_color(0, 0, 0)
        draw_rectangle(hw - 148, hh + 62, hw + 148, hh + 98)
        draw_set_color(255, 255, 255)
        draw_rectangle_sized(hw - 150, hh + 60, (draw_value / 10) * 300, 40)
        hfont.draw(hw, hh + 40, str(draw_value))

    update_canvas()


def handle_events(frame_time):
    global time, choice_state, selected

    bevents = get_events()
    for event in bevents:
        if event.type == SDL_QUIT:
            framework.quit()
            rewrite_option()
        elif time > 1:
            if event.type == SDL_KEYDOWN:
                if choice_state == -1:
                    if event.key in (ord('z'), SDLK_ESCAPE):
                        framework.pop_state()
                        audio_play("sndMenuSelect")
                        rewrite_option()
                    elif event.key in (SDLK_LEFT, SDLK_RIGHT):
                        selected = 1 - selected
                        audio_play("sndMenuEnter")
                    elif event.key in (ord('x'), SDLK_RETURN):
                        choice_state = selected
                        audio_play("sndMenuEnter")
                else:
                    volsfx = audio_get_volume_sfx_global()
                    volmus = audio_get_volume_music_global()
                    if event.key in (ord('z'), SDLK_ESCAPE):
                        choice_state = -1
                        audio_play("sndMenuSelect")
                    elif event.key is SDLK_LEFT:
                        if selected == 0:  # Sound effect Volume
                            audio_set_volume_sfx_global(volsfx - 1)
                        elif selected == 1:  # Music Volume
                            audio_set_volume_music_global(volmus - 1)
                    elif event.key is SDLK_RIGHT:
                        if selected == 0:  # Sound effect Volume
                            audio_set_volume_sfx_global(volsfx + 1)
                        elif selected == 1:  # Music Volume
                            audio_set_volume_music_global(volmus + 1)


def pause():
    pass


def resume():
    pass
