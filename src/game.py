from pico2d import *

import framework
import game_pause
from functions import *
from sprite import *

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
    """
    while (true):
        try:
            data_tuple = sprite_list.popitem()
            olddb: Sprite = data_tuple[1]
            del olddb
        except KeyError as e:
            break
        else:
            del olddb
    """


def update():
    if len(instance_list) > 0:
        for inst in instance_list:
            inst.event_step()
    else:
        raise RuntimeError("No instance")
    delay(0.01)


def draw_clean():
    instance_draw_update()
    if len(instance_draw_list) > 0:
        for inst in instance_draw_list:
            inst.event_draw()
    else:
        raise RuntimeError("No instance")


def draw():
    clear_canvas()
    draw_clean()
    update_canvas()


def instance_draw_update():
    global instance_list, instance_draw_list, instance_update
    if instance_update:
        del instance_draw_list
        instance_update = false
        instance_draw_list = []
        instance_draw_list = sorted(instance_list, key=lambda gobject: gobject.depth)
        # for inst in instance_list:
        #    instance_draw_list.append(inst)


def handle_events():
    event_queue = get_events()
    for event in event_queue:
        if event.type == SDL_QUIT:
            framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            framework.push_state(game_pause)
        elif event.type == SDL_KEYDOWN:
            io.procede(event)


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
        global instance_update
        instance_update = true
        instance_draw_update()

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
            if current == '0' or current == ' ' or current == '\n':
                continue
            if current == ';':
                newx = self.x
                newy -= self.tile_h
                continue
            # newx = (i - math.floor(i / self.hsz)) * self.tile_w
            # newy = math.floor(i / self.hsz) * self.tile_h
            # noinspection PyUnusedLocal
            if current.isnumeric():
                tcontainer.mess[int(current) - 1](100, newx, newy)
            else:
                if current == '@':
                    oPlayer(-10, newx + 10, newy + 10)
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
    # Check the place fits to self
    def place_free(self, vx, vy) -> bool:
        global instance_list_spec
        clist = instance_list_spec["Solid"]  # 고체 개체 목록 불러오기
        length = len(clist)
        if length > 0:
            # print("Checking Place for one")
            bbox_left = int(self.x - self.sprite_index.xoffset + vx)
            bbox_top = int(self.y - self.sprite_index.yoffset + vy)
            brect = SDL_Rect(bbox_left, bbox_top, self.sprite_index.width, self.sprite_index.height)
            temprect = SDL_Rect()

            for inst in clist:
                tempspr: Sprite = inst.sprite_index
                otho_left = int(inst.x - tempspr.xoffset)
                otho_top = int(inst.y - tempspr.yoffset)
                temprect.x, temprect.y, temprect.w, temprect.h = otho_left, otho_top, tempspr.width, tempspr.height
                if rect_in_rectangle_opt(brect, temprect):
                    return false
            return true
        else:
            return true

    def collide(self):
        self.xVel = 0

    def thud(self):
        self.yVel = 0
        self.onAir = false

    def draw_self(self):  # Simply draws its sprite on its position.
        if not self.sprite_index.__eq__(None):
            draw_sprite(self.sprite_index, self.image_index, self.x, self.y, 1, 1, 0.0, self.image_alpha)

    def event_step(self):  # The basic machanism of objects.
        if not self.step_enable:
            return

        if self.xVel != 0:
            xc = self.xVel + sign(self.xVel)
            if self.place_free(xc, 0):
                self.x += self.xVel
            else:
                self.collide()

        if self.yVel > 0:  # Going up higher
            yc = self.yVel + 1
        else:  # Going down
            yc = self.yVel - 1

        if self.place_free(0, yc):
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

    image_speed = 0
    step_enable = false
    gravity_default = 0
    xFric, yFric = 0, 0


# Definitions of Special Objects
class oBrick(Solid):
    name = "Brick of Mine"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_index = sprite_get("sCastleBrick")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3)


# Player
class oPlayer(GObject):
    name = "Player"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_index = sprite_get("Player")
        self.image_speed = 0


# Parent of Enemies
class oEnemyParent(GObject):
    name = "NPC"

    oStatus = oStatusContainer.IDLE


# Damage caused by Player
class oPlayerDamage(GObject):
    name = "DamageP"
    identify = ID_DMG_PLAYER
    gravity_default = 0


# Damage caused by Enemy
class oEnemyDamage(GObject):
    name = "DamageE"
    identify = ID_DMG_ENEMY
    gravity_default = 0


# Parent of Items
class oItemParent(GObject):
    name = "Item"
    identify = ID_ITEM
    gravity_default = 0


# Parent of Terrain Doodads
class oDoodadParent(GObject):
    name = "Doodad"
    identify = ID_DOODAD
    gravity_default = 0


# Object : Functions
def instance_create(Ty, depth=int(0), x=int(0), y=int(0)) -> object:
    temp = Ty(depth, x, y)
    global instance_last
    instance_last = temp
    return temp


def place_free(dx, dy) -> bool:
    # return true
    global instance_list_spec
    clist = instance_list_spec["Solid"]  # 고체 개체 목록 불러오기
    length = len(clist)
    if length > 0:
        # print("Checking Place")
        for inst in clist:
            tempspr: Sprite = inst.sprite_index
            if point_in_rectangle(dx, dy, inst.x - tempspr.width / 2, inst.y - tempspr.height / 2,
                                  inst.x + tempspr.width / 2, inst.y + tempspr.height / 2):
                return false
        return true
    else:
        return true


class GameExecutor:
    def __init__(self):
        # TODO: Definite more objects.
        # Declaring of Special Objects ( Need a canvas )
        sprite_load(
            [path_theme + "brick_castle_0.png", path_theme + "brick_castle_1.png", path_theme + "brick_castle_2.png",
             path_theme + "brick_castle_3.png"], "sCastleBrick", 0, 0)
        sprite_load(path_entity + "vampire.png", "Player", 0, 0)

        tcontainer.signin(oBrick)

        Camera.set_pos(0, 0)
        first_scene = TerrainManager(1, 1)
        first_scene.allocate("1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     ;;;;@;;; \
                                     0000 0000 0000 0000 0000 0000 0000 0000\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     ", 0)

        first_scene.generate()
