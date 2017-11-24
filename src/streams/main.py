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

manager = None
menusy = screen_height - 180


class MenuEnumerator:
    menunod = []  # A List of menu nodes
    menucnt = 0  # The number of menu nodes
    menusel = 0  # Current selection (index)
    menuold = 0  # Previous selection (index)
    menuscl = []  # A inverted scale of a currently selected menu node (Not acquire to all nodes in an index)
    menupos = 0  # The initiative y position of a menu node


class MainMenu:
    menu_hsize = 50
    depthlist = []
    currdepth = 0

    def menu_init(self, default_selected: int = 0):
        newone = MenuEnumerator()
        self.depthlist.append(newone)
        newone.menusel = default_selected
        newone.menuold = default_selected
        newone.menupos = self.menu_hsize * default_selected

    def menu_add(self, caption: str):
        menum = self.depthlist[self.currdepth]
        menum.menunod.append(caption)
        menum.menuscl.append(0)
        menum.menucnt += 1
        return menum.menucnt - 1

    def update(self, frame_time):
        menum = self.depthlist[self.currdepth]
        vel = frame_time * delta_velocity(10)
        for i in range(menum.menucnt):
            menum.menupos += (self.menu_hsize * menum.menusel - menum.menupos) / 5 * vel
            if menum.menusel == i:
                if menum.menuscl[i] != 0:
                    menum.menuscl[i] -= menum.menuscl[i] / 5 * vel
            elif menum.menuscl[i] != 1:
                menum.menuscl[i] += (1 - menum.menuscl[i]) / 5 * vel

    def draw(self, frame_time):
        menum = self.depthlist[self.currdepth]
        ddx = screen_width / 2 + 160
        ddy = menusy + menum.menupos + 10

        global hfont, hfontlrg
        for j in range(menum.menucnt):
            dhfont = hfont
            if j == menum.menusel:
                dscl = 1 - menum.menuscl[j] / 5
                dhfont = hfontlrg
                draw_set_color(32, 32, 32)
                draw_rectangle(0, ddy - 25, screen_width, ddy + 15)
            elif j == menum.menuold:
                dscl = 1.2 - menum.menuscl[j] / 5
            else:
                dscl = 1
            draw_set_color(255, 255, 255)
            dhfont.draw(ddx, ddy, menum.menunod[j], dscl)
            ddy -= self.menu_hsize * dscl


# noinspection PyGlobalUndefined
def enter():
    global manager

    io.key_add(SDLK_UP)
    io.key_add(SDLK_LEFT)
    io.key_add(SDLK_DOWN)
    io.key_add(ord('z'))
    io.key_add(ord('x'))
    io.key_add(SDLK_RETURN)

    if manager is None:
        global hfontsml, hfont, hfontlrg
        hfontsml = load_font(path_font + "Contl___.ttf", 36)
        hfont = load_font(path_font + "Contl___.ttf", 40)  # "윤고딕_310.ttf"
        hfontlrg = load_font(path_font + "Contl___.ttf", 44)

        draw_set_alpha(1)
        global mainmenu, mn_begin, mn_opt, mn_credit, mn_end
        manager = mainmenu = MainMenu()
        mainmenu.menu_init(0)
        mn_begin = mainmenu.menu_add("begin game")
        mn_opt = mainmenu.menu_add("option")
        mn_credit = mainmenu.menu_add("credit")
        mn_end = mainmenu.menu_add("end game")


def exit():
    global hfontsml, hfont, hfontlrg
    del hfontsml, hfont, hfontlrg

    global manager
    if manager is not None:
        del manager
        manager = None


def update(frame_time):
    global mainmenu
    mainmenu.update(frame_time)
    menum = mainmenu.depthlist[mainmenu.currdepth]

    if io.key_check_pressed(ord('z')):
        io.clear()
    elif io.key_check_pressed(SDLK_RETURN) or io.key_check_pressed(ord('x')):
        io.clear()

        if mn_begin == menum.menusel:
            framework.change_state(game)
        elif mn_opt == menum.menusel:
            pass
        elif mn_credit == menum.menusel:
            pass
        elif mn_end == menum.menusel:
            framework.quit()
    elif io.key_check_pressed(SDLK_UP):
        if menum.menusel <= 0:
            menum.menusel = menum.menucnt - 1
        else:
            menum.menusel -= 1
    elif io.key_check_pressed(SDLK_DOWN):
        if menum.menusel >= menum.menucnt - 1:
            menum.menusel = 0
        else:
            menum.menusel += 1


def draw(frame_time):
    clear_canvas()
    global mainmenu
    mainmenu.draw(frame_time)
    update_canvas()


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
