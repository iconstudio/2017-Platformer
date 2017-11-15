from module.pico2d import *
from module.functions import *
from module.constants import *

from module import framework
from module.framework import io
from streams import game

from module.sprite import *

__all__ = [
    "name", "menu_begin", "Menu", "MenuNode", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "main_state"
menusel = None
menudic = {}
menusy = screen_height - 180
mpush = 0

class MenuNode:
    captioon: str = "submenu"
    nnext = None

    def __init__(self, ncaption):
        self.captioon = ncaption

    def set_next(self, node):
        self.nnext = node

    def __next__(self):
        return self.nnext


class Menu:
    caption: str = "menu"
    menu_last = None
    nnext = None
    nbefore = None
    rpush = 0

    subsel = None
    sub_opened: bool = false
    submenu_last: MenuNode = None
    subroot: MenuNode = None

    def __init__(self, ncaption):
        self.caption = ncaption

    def add(self, ncaption):
        newnode = MenuNode(ncaption)
        if self.subroot == None:
            self.subroot = newnode
        if self.submenu_last != None:
            self.submenu_last.set_next(self)
        return newnode

    def __next__(self):
        return self.nnext


def menu_create(ncaption) -> Menu:
    newone = Menu(ncaption)
    if Menu.menu_last != None:
        Menu.menu_last.nnext = newone
        newone.nbefore = Menu.menu_last

    Menu.menu_last = newone
    menudic[ncaption] = newone
    return newone


menu_begin: Menu = None


# noinspection PyGlobalUndefined
def enter():
    io.key_add(SDLK_UP)
    io.key_add(SDLK_LEFT)
    io.key_add(SDLK_DOWN)
    io.key_add(SDLK_x)
    io.key_add(SDLK_z)
    io.key_add(SDLK_RETURN)

    global hfont, hfontlrg
    hfont = load_font(path_font + "윤고딕_310.ttf", 40)
    hfontlrg = load_font(path_font + "윤고딕_320.ttf", 40)

    global menusel, menu_begin, menu_opt, menu_credit, menu_exit
    cm = menusel = menu_begin = menu_create("Start Game")
    cm.subsel = cm.add("Stage 1")
    cm.add("Stage 2")
    cm.add("Stage 3")
    menu_opt = menu_create("Option")
    menu_credit = menu_create("Credit")
    cm = menu_exit = menu_create("Exit Game")
    cm.add("Yes")
    cm.subsel = cm.add("No")
    # cm.nnext = menu_begin


def exit():
    global hfont, hfontlrg
    del hfont, hfontlrg


def update(frame_time):
    global mpush
    if mpush != 0:
        mpush -= mpush / 4 * (frame_time * delta_velocity(5))

    global menusel, menu_begin, menu_opt, menu_credit, menu_exit
    if io.key_check_pressed(SDLK_z):
        if menusel == menu_begin:
            menusel.sub_opened = false
    elif io.key_check_pressed(SDLK_RETURN) or io.key_check_pressed(SDLK_x):
        io.clear()
        if menusel == menu_begin:
            if not menusel.sub_opened:
                menusel.sub_opened = true
            else:
                framework.change_state(game)
        elif menusel == menu_opt:
            pass
        elif menusel == menu_credit:
            pass
        elif menusel == menu_exit:
            framework.quit()
    elif io.key_check_pressed(SDLK_UP):
        if not menusel.sub_opened:
            menusel = menusel.nbefore
            if menusel == None:
                menusel = Menu.menu_last
                mpush = -200
            else:
                mpush = -50
    elif io.key_check_pressed(SDLK_DOWN):
        if not menusel.sub_opened:
            menusel = next(menusel)
            if menusel == None:
                menusel = menu_begin
                mpush = 200
            else:
                mpush = 50


def draw():
    global hfont, hfontlrg, menu_begin, menusy
    clear_canvas()
    ddx = screen_width / 2 + 90
    curr = menu_begin
    ddy = menusy - mpush
    while curr != None:
        if menusel == curr:
            break
        ddy += 50
        curr = next(curr)

    curr = menu_begin
    while curr != None:
        if menusel == curr:
            hfontlrg.draw(ddx, ddy, curr.caption)
        else:
            hfont.draw(ddx, ddy, curr.caption)
        ddy -= 50 - curr.rpush
        curr = next(curr)
    update_canvas()
    pass


def handle_events(frame_time):
    mevents = get_events()
    for event in mevents:
        if event.type == SDL_QUIT:
            framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                framework.quit()
            else:
                io.proceed(event)


def pause():
    pass


def resume():
    pass
