from pico2d import *
from functions import *

import framework

__all__ = [
              "Menu", "MenuNode"
          ] + framework.__all__

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================

name = "main_state"
logo_time = 0


def enter():
    global bg
    open_canvas(screen_width, screen_height, true)
    hide_cursor()
    hide_lattice()
    bg = load_image(path_image + "bg_black.png")
    pass


def exit():
    if logo_time > 10:
        global bg
        del bg
        close_canvas()
    pass


def update():
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0
        import game
        framework.push_state(game)
    logo_time += 0.01
    delay(0.01)
    pass


def draw():
    global bg
    clear_canvas()
    bg.draw(screen_width / 2, screen_height / 2)
    update_canvas()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                framework.quit()


def pause():
    pass


def resume():
    pass


# ==================================================================================================
#                                    사용자 정의 객체 / 함수
# ==================================================================================================

class MenuNode:
    captioon:str = "menu"
    nnext = None

    @staticmethod
    def __init__(self, ncaption, node):
        self.captioon = ncaption
        self.nnext = node


class Menu:
    root:MenuNode = None
    

