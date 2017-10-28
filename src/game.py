from pico2d import *
from functions import *
from sprite import *

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

ID_SOLID: str = "Solid"
ID_PARTICLE: str = "Particle"
ID_DOODAD: str = "Doodad"
ID_DMG_PLAYER: str = "HurtPlayer"
ID_DMG_ENEMY: str = "HurtEnemy"
ID_ITEM: str = "Items"
instance_list_spec[ID_SOLID] = []
instance_list_spec[ID_PARTICLE] = []
instance_list_spec[ID_DOODAD] = []
instance_list_spec[ID_DMG_PLAYER] = []
instance_list_spec[ID_DMG_ENEMY] = []
instance_list_spec[ID_ITEM] = []

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================

name = "game_state"


def enter():
    GameExecutor()


def exit():
    '''
    while (true):
        try:
            data_tuple = sprite_list.popitem()
            olddb: Sprite = data_tuple[1]
            del olddb
        except KeyError as e:
            break
        else:
            del olddb
    '''


def update():
    if len(instance_list) > 0:
        for inst in instance_list:
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
        if event.type == SDL_QUIT:
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

# ==================================================================================================
#                                               지형
# ==================================================================================================

# Object : Terrain Container
class TerrainContainer:
    mess = []

    def signin(self, type_t):
        self.mess.append(type_t)

    def clear(self):
        self.mess.clear()


tcontainer = TerrainContainer()


# Object : Terrain Manager
class TerrainManager:
    fits = []
    type_theme = 0

    def __init__(self, theme: int = 0, numberw: int = 1, numberh: int = 1):
        self.type_theme = theme
        for i in range(0, numberw, 1):
            for j in range(0, numberh, 1):
                newone = TerrainAllocator(self.type_theme, i * screen_width, j * screen_height)
                self.fits.append(newone)

    def allocate(self, data: str, position: int = 0):
        try:
            self.fits[position].allocate(data, self.type_theme)
        except IndexError:
            pass

    def generate(self):
        for alloc in self.fits:
            alloc.generate()

    def __del__(self):
        try:
            for alloc in self.fits:
                del alloc
        except IndexError:
            return
        except KeyError:
            return
            # finally:
            # del self.fits


# Object : A Allocating block of Terrain
class TerrainAllocator:
    data: str = ""  # Determines what to generate
    type_theme: int = 0
    type_path: int = 0  # Determines how to do.
    tile_w: int = 20
    tile_h: int = 20
    x, y, w, h, hsz, vsz = 0, 0, 0, 0, 0, 0

    def __init__(self, nt: int, nx: int, ny: int, nw: int = screen_width, nh: int = screen_height):
        self.assignment(nt, nx, ny, nw, nh)

    def assignment(self, nt: int, nx: int, ny: int, nw: int = screen_width, nh: int = screen_height):
        # The position of a map
        self.x, self.y = nx, ny
        # The size of a map
        self.w, self.h = nw, nh
        # The number of grid
        self.hsz, self.vsz = int(nw / self.tile_w), int(nh / self.tile_h)
        self.type_theme = nt

    def generate(self):
        newx = self.x
        newy = self.y + self.h - self.tile_h
        for i in range(0, len(self.data)):
            current = self.data[i]
            if current == "0" or current == " " or current == "\n":
                continue
            if current == "@":
                newy -= self.tile_h
                continue
            # newx = (i - math.floor(i / self.hsz)) * self.tile_w
            # newy = math.floor(i / self.hsz) * self.tile_h
            NEWBLOCK: GObject = tcontainer.mess[int(current) - 1](100, newx, newy)
            newx += self.tile_w
            if newx >= self.w:
                newx = self.x
                newy -= self.tile_h

    def allocate(self, data: str, newtype: int = 0):
        self.data = data
        self.type_theme = newtype


# ==================================================================================================
#                                               게임
# ==================================================================================================


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
        self.x = nx
        self.y = ny

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
        if self.sprite_index != None:
            draw_sprite(self.sprite_index, self.image_index, self.x, self.y, 1, 1, 0.0, self.image_alpha)

    def event_step(self):  # The basic machanism of objects.
        if not self.step_enable:
            return

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


class oBrick(Solid):
    name = "Brick of Mine"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_index = sprite_get("CastleBrick")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3)


# Object : Specials
# Player
class Player(GObject):
    name = "Player"


# Parent of Enemies
class EnemyParent(GObject):
    name = "NPC"


# Damage caused by Player
class PlayerDamage(GObject):
    name = "DamageP"
    identify = ID_DMG_PLAYER
    gravity_default = 0


# Damage caused by Enemy
class EnemyDamage(GObject):
    name = "DamageE"
    identify = ID_DMG_ENEMY
    gravity_default = 0


# Parent of Items
class ItemParent(GObject):
    name = "Item"
    identify = ID_ITEM
    gravity_default = 0


# Parent of Terrain Doodads
class DoodadParent(GObject):
    name = "Doodad"
    identify = ID_DOODAD
    gravity_default = 0


# Object : Functions
def instance_create(Ty, depth=int(0), x=int(0), y=int(0)) -> object:
    temp = Ty(depth, x, y)
    temp.x, temp.y = x, y
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


class GameExecutor:
    def __init__(self):
        # TODO: Definite more objects.
        # Definitions of Special Objects ( Need a canvas )
        sprite_load(
            [path_theme + "brick_castle_0.png", path_theme + "brick_castle_1.png", path_theme + "brick_castle_2.png",
             path_theme + "brick_castle_3.png"], "CastleBrick", 0, 0)

        tcontainer.signin(oBrick)

        first_scene = TerrainManager(1, 1)
        first_scene.allocate("1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     @ \
                                     @ \
                                     @ \
                                     @ \
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     ", 0)

        first_scene.generate()
