from module.pico2d import *

import module.framework as framework
import streams.main as main

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "begin_state"
logo_time = 0


# noinspection PyGlobalUndefined,PyGlobalUndefined
def enter():
    global logo, hfont
    logo = load_image(path_image + "logo.png")
    hfont = load_font(path_font + "윤고딕_310.ttf", 32)


def exit():
    if logo_time > 10:
        global logo, hfont
        del logo, hfont


def update():
    global logo_time
    if logo_time > 180.0:
        logo_time = 0
        framework.change_state(main)
    logo_time += 1

    delay(0.01)


def draw():
    global logo
    clear_canvas()
    logo.draw(screen_width / 2, screen_height / 2)
    draw_set_color(255, 255, 255)
    hfont.draw(screen_width / 2 - 200, screen_height / 2 - 100, "iconstudio")
    update_canvas()


def handle_events():
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
