from module.pico2d import *
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
logo_time = 0


# noinspection PyGlobalUndefined,PyGlobalUndefined
def enter():
    global logo, hfont
    logo = load_image(path_image + "logo.png", 80, 80)
    hfont = load_font(path_font + "윤고딕_310.ttf", 32)


def exit():
    if logo_time > fps_target * 3:
        global logo, hfont
        del logo, hfont


def update(game_frame):
    global logo_time
    if logo_time > fps_target * 3:
        logo_time = 0
        framework.change_state(main)
    logo_time += 1

    delay(0.01)


def draw():
    global logo
    clear_canvas()
    logo.draw(screen_width / 2, screen_height / 2)
    draw_set_color(255, 255, 255)
    hfont.draw(screen_width / 2 - 60, screen_height / 2 - 100, "iconstudio")
    update_canvas()


def handle_events(frame_time):
    bevents = get_events()
    for event in bevents:
        if event.type == SDL_QUIT:
            framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                framework.quit()


def pause():
    pass


def resume():
    pass
