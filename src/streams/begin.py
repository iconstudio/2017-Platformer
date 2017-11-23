from module.pico2d import *
from module.functions import *
from module.constants import *

from module import framework
from streams import main

from module.sprite import *

__all__ = [
    "name", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "begin_state"
targ_time = 3
logo_time = targ_time
alpha_max = 2
alpha = alpha_max

# noinspection PyGlobalUndefined,PyGlobalUndefined
def enter():
    global logo, hfont
    logo = sprite_get("sLogo")
    hfont = load_font(path_font + "윤고딕_310.ttf", 32)


def exit():
    global hfont
    del hfont


def update(frame_time):
    global logo_time, targ_time, alpha_max, alpha
    if logo_time <= 0:
        logo_time = 0
        alpha -= frame_time
    else:
        logo_time -= frame_time
    if alpha <= -alpha_max:
        framework.change_state(main)


def draw(frame_time):
    global hfont, alpha_max, alpha
    clear_canvas()
    
    valuea = float(max(0, alpha) / alpha_max)
    draw_sprite(logo, 0, screen_width / 2, screen_height / 2, 1, 1, 0, valuea)
    draw_set_color(255, 255, 255)
    draw_set_alpha(valuea)
    hfont.draw(screen_width / 2, screen_height / 2 - 100, "iconstudio")
    update_canvas()


def handle_events(frame_time):
    bevents = get_events()
    for event in bevents:
        if event.type == SDL_QUIT:
            framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                global logo_time, alpha
                if logo_time <= 0:
                    alpha = 0
                else:
                    logo_time = 0


def pause():
    pass


def resume():
    pass
