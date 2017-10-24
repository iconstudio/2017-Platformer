from pico2d import *
from functions import *

import framework

__all__ = [
              "name", "hwnd", "instance_last", "instance_list_spec", "instance_draw_list", "instance_update",
              "sprite_list",
              "Sprite", "GObject", "Solid"
          ] + framework.__all__

# Global : Variables 2
instance_last = None  # 마지막 개체
instance_list: list = []  # 개체는 순서가 있다.
"""
            <List> instance_list_spec:

                목적: 객체를 종류 별로 담기 위한 리스트
                용법:
                    instance_list_spec[객체 이름] = []
                    instance_list_spec[객체 이름].append(객체 ID)

                비고: 객체 이름 외에도 "Solid", "Particle" 등의 구별자 사용.
"""
instance_list_spec: dict = {}  # 객체 종류 별 목록
instance_draw_list: list = []  # 개체 그리기 목록
instance_update: bool = false  # 개체 갱신 여부
sprite_list: dict = {}  # 스프라이트는 이름으로 구분된다.

ID_SOLID: str = "Solid"
ID_PARTICLE: str = "Particle"
ID_DOODAD: str = "Doodad"
ID_DMG_PLAYER: str = "HurtPlayer"
ID_DMG_ENEMY: str = "HurtEnemy"
instance_list_spec[ID_SOLID] = []
instance_list_spec[ID_PARTICLE] = []
instance_list_spec[ID_DOODAD] = []
instance_list_spec[ID_DMG_PLAYER] = []
instance_list_spec[ID_DMG_ENEMY] = []

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================

name = "game_state"


def enter():
    global hwnd
    hwnd = open_canvas(screen_width, screen_height, true)
    SDL_SetWindowTitle(hwnd, ctypes.c_char_p("Vampire Exodus".encode("UTF-8")))
    SDL_SetWindowSize(hwnd, screen_width * screen_scale, screen_height * screen_scale)
    # SDL_SetWindowFullscreen(self.hwnd, ctypes.c_uint32(1))
    hide_cursor()
    hide_lattice()

    # TODO: Definite more objects.
    # Definitions of Special Objects ( Need a canvas )
    global bg
    bg = sprite_load(path_image + "bg_black.png", "black")
    sprite_load(
        [path_theme + "brick_castle_0.png", path_theme + "brick_castle_1.png", path_theme + "brick_castle_2.png",
         path_theme + "brick_castle_3.png"], "CastleBrick", 4)

    for i in range(0, 20, 1):
        instance_create(oBrick, 40 - i * 20, 800)

        # tempo = instance_create(GObject, 0, 100, 400)
        # tempo.sprite_index = sprite_get("CastleBrick")
        # tempo.gravity_default = 0.3


def exit():
    close_canvas()
    try:
        while (true):
            data_tuple = sprite_list.popitem()
            if data_tuple.index(0):
                break
    except KeyError as e:
        pass

    pass


def update():
    if len(instance_list) > 0:
        for inst in instance_list:
            if inst.step_enable:
                inst.event_step()
    else:
        raise RuntimeError("No instance")
    delay(0.01)


def draw():
    clear_canvas()
    instance_draw_update()
    if len(instance_draw_list) > 0:
        for inst in instance_draw_list:
            inst.event_draw()
    else:
        raise RuntimeError("No instance")
    update_canvas()


def instance_draw_update():
    global instance_draw_list, instance_update
    if instance_update:
        del instance_draw_list
        instance_update = false
        instance_draw_list = []
        for inst in instance_list:
            instance_draw_list.append(inst)


def handle_events():
    event_queue = get_events()
    for event in event_queue:
        if (event.type == SDL_QUIT):
            framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            framework.quit()


def pause():
    pass


def resume():
    pass


# ==================================================================================================
#                                    사용자 정의 객체 / 함수
# ==================================================================================================

# Object : Sprites
class Sprite(object):
    number: int = 0
    width, height = 0, 0
    isSummed: bool = false

    def __init__(self, filepath, number):
        """
            이미지 불러오기, 이미지 분할, 리스트화 작업
            :param filepath: 
            :param number: 
        """
        if type(filepath) == list:
            self.isSummed = true
            self.number = len(filepath)

            try:
                if self.number > 0:
                    self.__data__ = []
                    for specpath in filepath:
                        img = load_image(specpath)
                        self.__data__.append(img)
                    self.width = int(self.__data__[0].w)
                    self.height = int(self.__data__[0].h)
            except IndexError:
                raise RuntimeError("스프라이트 목록아 비어있습니다!")
        else:  # load only an image, so dosent need spliting one image.
            self.__data__ = load_image(filepath)
            self.number = number  # the number of sprite in an image
            # size of each index
            self.width = int(self.__data__.w / number)
            self.height = int(self.__data__.h)

        try:
            tempTy = type(number)
            if tempTy != int and tempTy != float:
                raise RuntimeError("스프라이트 불러오기 시 인자가 숫자가 아닙니다.")
        except ZeroDivisionError:
            raise RuntimeError("스프라이트의 갯수는 0개가 될 수 없습니다.")

    def draw(self, index, x, y, xscale=float(1), yscale=float(1), rot=float(0.0)) -> None:
        if not self.isSummed:
            if rot != 0.0:  # pico2d does not support scaling + rotating draw.
                self.__data__.rotate_draw(rot, x, y, int(self.width * xscale), int(self.height * yscale))
            else:
                self.__data__.clip_draw(int(index * self.width), 0, self.width, self.height, x, y,
                                        int(self.width * xscale), int(self.height * yscale))
        else:
            if rot != 0.0:  # pico2d does not support scaling + rotating draw.
                self.__data__[int(index)].rotate_draw(rot, x, y, int(self.width * xscale), int(self.height * yscale))
            else:
                self.__data__[int(index)].clip_draw(0, 0, self.width, self.height, x, y, int(self.width * xscale),
                                                    int(self.height * yscale))

    def get_handle(self):
        return self.__data__


# Object : Game Object
class GObject(object):
    name = "None"
    identify = ""
    next = None

    # Properties of sprite
    sprite_index: Sprite = None
    image_alpha: float = 1.0
    image_index = float(0)
    image_speed = float(0)
    visible: bool = true
    depth: int = 0

    # for optimization
    step_enable: bool = true

    x, y = 0, 0
    xVel, yVel = 0, 0
    xFric, yFric = 0.4, 1
    gravity_default = 0.4
    gravity: float = 0
    onAir: bool = false

    def __init__(self, ndepth=int(0), nx=int(0), ny=int(0)):
        self.depth = ndepth
        self.x, self.y = nx, ny

        global instance_list, instance_update, instance_list_spec
        instance_list.append(self)
        instance_update = true
        if self.identify != "":
            instance_list_spec[self.identify].append(self)

    def __str__(self):
        return self.name

    def __del__(self):
        global instance_last, instance_list, instance_list_spec, instance_draw_list, instance_update

    # Below methods are common-functions for all object that inherites graviton.
    def collide(self):
        self.xVel = 0

    def thud(self):
        self.yVel = 0
        self.onAir = false

    def draw_self(self):  # Simply draws its sprite on its position.
        if (self.sprite_index != None):
            if self.sprite_index.isSummed:
                get = self.sprite_index.get_handle()[int(self.image_index)]
                get.opacify(self.image_alpha)
            else:
                get = self.sprite_index.get_handle()
                get.opacify(self.image_alpha)
            draw_sprite(self.sprite_index, self.image_index, self.x, self.y)

    def event_step(self):  # The basic machanism of objects.
        if self.xVel != 0:
            xc = self.x + self.xVel + sign(self.xVel)
            if place_free(xc, self.y):
                self.x += self.xVel
            else:
                self.collide()

        if self.yVel > 0:  # Going up higher
            yc = self.y + self.yVel + 1
        else:  # Going down
            yc = self.y + self.yVel - 1

        if place_free(self.x, yc):
            self.y += self.yVel  # let it moves first.
            self.gravity = self.gravity_default
            self.yVel -= self.gravity
            self.onAir = true
        else:
            self.gravity = 0
            if self.xVel != 0:  # horizontal friction works only when it is on the ground
                self.xVel *= self.xFric
            self.thud()

    def event_draw(self):  # This will be working for drawing.
        self.draw_self()


# Object : Solid Objects
class Solid(GObject):
    # reset some inherited variables
    name = "Solid"
    identify = ID_SOLID

    step_enable = false
    gravity_default = 0
    xFric, yFric = 0, 0

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)


class oBrick(Solid):
    name = "Brick of Mine"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_index = sprite_get("CastleBrick")
        self.image_index = self.sprite_index.number #irandom_range(0, 3)


# Object : Functions
def instance_create(Ty, depth=int(0), x=int(0), y=int(0)) -> object:
    temp = Ty(depth, x, y)
    global instance_last
    instance_last = temp
    return temp


def place_free(dx, dy) -> bool:
    global instance_list_spec
    clist = instance_list_spec["Solid"]  # 고체 개체 목록 불러오기
    length = len(clist)
    if length > 0:
        for inst in clist:
            tempspr: Sprite = inst.sprite_index
            if point_in_rectangle(dx, dy, inst.x - tempspr.width / 2, inst.y - tempspr.height / 2,
                                  inst.x + tempspr.width / 2, inst.y + tempspr.height / 2):
                return true
        return false
    else:
        return false


def sprite_load(filepaths, name=str("default"), number=int(1), xoffset=None, yoffset=None) -> Sprite:
    global sprite_list
    new = Sprite(filepaths, number)
    sprite_list[name] = new
    return new


def sprite_get(name: str) -> Sprite:
    global sprite_list
    return sprite_list[name]


def draw_sprite(spr: Sprite, index=int(0) or float(0), x=int(0), y=int(0), xscale=float(1), yscale=float(1),
                rot=float(0.0)) -> None:
    spr.draw(index, x, y, xscale, yscale, rot)
