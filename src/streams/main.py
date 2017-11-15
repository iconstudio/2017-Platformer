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


class MainMenu:
    maxdepth = 0
    menu_hsize = 50
    menucnt = []  # The number of menu nodes
    menusel = []  # Current selection
    menuold = []  # Previous selection
    menuscl = []
    menupos = []  # The initiative y position of a menu node

    def menu_clear(self, index: int, default_selected: int = 9):
        if (index > self.maxdepth):
            self.maxdepth = index
        self.menucnt[index] = 0
        self.menusel[index] = default_selected
        self.menuold[index] = default_selected
        self.menuscl[index] = 0
        self.menupos[index] = self.menu_hsize * default_selected

    def update(self, frame_time):
        for i in range(self.maxdepth):
            self.menupos[i] += (-self.menu_hsize * self.menusel[i] - self.menupos[i]) / 5 * (
                frame_time * delta_velocity(10))
            self.menuscl[i] -= self.menuscl[i] / 5 * (frame_time * delta_velocity(10))

    def draw(self, frame_time):
        """

for (j = 0; j <= maxdepth; j += 1) {
 dy = menupos[j] - 10;
 dalpha = 1 - abs(menurot / 90 - j);
 for (i = 0; i < menucnt[j]; i += 1) {
  if (i = menusel[j])
   draw_set_alpha(aalpha);
  else
   draw_set_alpha(dalpha * aalpha);
  if (i = menusel[j])
   dscl = 4 - menuscl[j] * 2;
  else if (i = menuold[j])
   dscl = 2 + menuscl[j] * 2;
  else
   dscl = 2;
  draw_set_color(make_color_hsv(0, 0, 255 * menucol[j, i]));
  sw = menu_text(8 + rpush[2], dy, menucap[j, i], dscl / 6, menurot - j * 90);
  ldy = dy;
  dy += 5 * dscl + 1.5;
  if (menuinf[j, i] != "") {
   if (i = menusel[j]) {
    draw_set_alpha(aalpha * infoscl[j]);
    menu_text(8 + rpush[2], dy - 0.875 * infoscl[j], "- " + menuinf[j, i], infoscl[j] * 1.75 / 6, menurot - j * 90);
    dy += 10.5 * infoscl[j] + 1;
   } else if (i = menuold[j]) {
    draw_set_alpha(aalpha * infosco[j]);
    menu_text(8 + rpush[2], dy - 0.875 * infosco[j], "- " + menuinf[j, i], infosco[j] * 1.75 / 6, menurot - j * 90);
    dy += 10.5 * infosco[j] + 1.5;
   }
  }
  if (menuvar[j, i] != "0") {
   draw_set_alpha(dalpha * aalpha);
   draw_set_color(make_color_hsv(0, 0, 176 * menucol[j, i]));;
   d3d_transform_set_rotation_y(90);
   d3d_transform_add_translation(-sw, 0, -sw);
   d3d_transform_add_rotation_y(menurot - j * 90);
   d3d_transform_add_translation(sw, 0, sw);
   draw_text_transformed(8 + (string_width(menucap[j, i]) + 3) * dscl / 6 + rpush[2], ldy, string(variable_global_get(menuvar[j, i])), dscl / 6, dscl / 6, 0);
   d3d_transform_set_identity();
   draw_set_color(make_color_hsv(0, 0, 255 * menucol[j, i]));
  }
 }
}
        """
        pass


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
        mpush -= mpush / 4 * (frame_time * delta_velocity(10))

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
                mpush = 200
            else:
                mpush = -50
    elif io.key_check_pressed(SDLK_DOWN):
        if not menusel.sub_opened:
            menusel = next(menusel)
            if menusel == None:
                menusel = menu_begin
                mpush = -200
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
