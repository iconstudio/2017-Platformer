from pico2d import *
from functions import *
from constants import *

import math
from camera import *

from sprite import *
from audio import *

__all__ = [
    "oStatusContainer", "instance_place", "instance_list_remove_something", "instance_list_clear",
    "instance_clear_all", "instance_place_single",
    "instance_last", "instance_list_spec", "instance_draw_list", "instance_update", "instance_list",
    "get_instance_list", "draw_list_sort",
    "container_player", "GObject", "Solid", "oItemParent", "oDoodadParent",
    "oEffectParent",
    "ID_OVERALL", "ID_DRAW", "ID_OTHERS", "ID_SOLID", "ID_TILE", "ID_ENEMY", "ID_ITEM",
    "ID_PARTICLE", "ID_DOODAD", "ID_EFFECT", "ID_UI", "ID_DOODAD_DECO", "ID_TRAP"
]

# Global : Variables
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
instance_update: bool = true  # 개체 갱신 여부

# Special constants.
ID_OVERALL: str = "All"
ID_DRAW: str = "Draw"
#
ID_OTHERS: str = "Objects"

ID_PARTICLE: str = "Particle"
ID_DOODAD: str = "Doodad"
ID_DOODAD_DECO: str = "DoodadDecoration"
ID_TRAP: str = "Trap"

ID_TILE: str = "Tile"
ID_SOLID: str = "Solid"

ID_ENEMY: str = "Enemy"
ID_ITEM: str = "Items"
ID_EFFECT: str = "Effect"
ID_UI: str = "UI"
instance_list_spec[ID_OTHERS] = []
instance_list_spec[ID_PARTICLE] = []
instance_list_spec[ID_DOODAD] = []
instance_list_spec[ID_DOODAD_DECO] = []
instance_list_spec[ID_TRAP] = []
instance_list_spec[ID_TILE] = []
instance_list_spec[ID_SOLID] = []
instance_list_spec[ID_ENEMY] = []
instance_list_spec[ID_ITEM] = []
instance_list_spec[ID_EFFECT] = []
instance_list_spec[ID_UI] = []

container_player = None


def get_instance_list(identific: str) -> list:
    global instance_list, instance_draw_list, instance_list_spec
    if identific is ID_OVERALL:
        return instance_list
    elif identific is ID_DRAW:
        return instance_draw_list
    else:
        try:
            return instance_list_spec[identific]
        except KeyError:
            print("Not available key of list")
            return []


def instance_list_remove_something(identific: str, content):
    where = get_instance_list(identific)
    try:
        where.remove(content)
    except KeyError:
        pass
    except ValueError:
        pass


def instance_list_clear(identific: str):
    global instance_list, instance_draw_list, instance_list_spec
    if identific is ID_OVERALL:
        instance_list.clear()
        instance_list = []
    elif identific is ID_DRAW:
        instance_draw_list.clear()
        instance_draw_list = []
    else:
        try:
            instance_list_spec[identific].clear()
            instance_list_spec[identific] = []
        except KeyError:
            print("Not available key of list")


def instance_clear_all():
    global instance_list, instance_draw_list, instance_list_spec
    for inst in instance_list:
        inst.destroy()

    instance_list_clear(ID_OVERALL)
    instance_list_clear(ID_DRAW)
    instance_list_clear(ID_DOODAD)
    instance_list_clear(ID_EFFECT)
    instance_list_clear(ID_OTHERS)
    instance_list_clear(ID_ENEMY)


def draw_list_sort():
    global instance_list, instance_draw_list
    instance_draw_list = sorted(instance_list, key = lambda gobject: -gobject.depth)


# Object : A container of Status
class oStatusContainer:
    NONE = 0
    IDLE = 1
    WALK = 8
    PATROL = 10
    RUNNING = 15
    TRACKING = 20
    ATTACKING = 40
    ATTACKING_END = 45
    LADDERING = 50
    CHANNELING = 60
    STUNNED = 80
    DEAD = 98
    DISAPPEAR = 99


# Object : Game Object
class GObject(object):
    # Basis properties of object
    name: str = "None"
    identify: str = ID_OTHERS
    next: object = None

    # Advanced properties of object
    oStatus = oStatusContainer.IDLE
    stunned: int = 0

    # Properties of sprite
    sprite_index: Sprite = None
    image_index = float(0)
    image_speed = float(0)
    image_xscale: float = 1.0
    image_alpha: float = 1.0
    visible: bool = true
    depth: int = 0

    # for optimization
    step_enable: bool = true

    # Physics (real-scale: Km per hours)
    x, y = 0, 0
    xVel, yVel = 0, 0
    xVelMin, xVelMax = -45, 45
    yVelMin, yVelMax = -80, 100
    xFric, yFric = 0.6, 0
    gravity_default: float = delta_gravity()
    gravity: float = 0
    onAir: bool = false

    def __init__(self, ndepth = int(0), nx = int(0), ny = int(0)):
        if ndepth is not None:
            self.depth = ndepth
        self.x = nx
        self.y = ny
        global instance_list, instance_update, instance_list_spec, instance_draw_list
        instance_list.append(self)
        instance_draw_list.append(self)
        instance_update = true
        if self.identify != "":
            instance_list_spec[self.identify].append(self)

    def __str__(self):
        return self.name

    def __del__(self):

        # self.destroy()
        pass

    def sprite_set(self, spr: Sprite or str):
        if type(spr) == str:
            self.sprite_index = sprite_get(spr)
        else:
            self.sprite_index = spr
        self.image_index = 0

    def destroy(self):
        self.step_enable = false
        self.depth = 1000000
        self.x = -10000
        self.image_xscale = 0
        self.xVel, self.yVel = 0, 0
        global instance_list, instance_list_spec, instance_update, instance_draw_list
        instance_update = true

        self.visible = false
        instance_list.remove(self)
        (instance_list_spec[self.identify]).remove(self)
        instance_draw_list.remove(self)
        del self

    # Below methods are common-functions for all object that inherits graviton.
    def instance_collide(self, othero) -> bool:
        if othero is not Camera and not self.visible:
            return false

        sx, sy, sw, sh = self.get_bbox()
        ox, oy, ow, oh = othero.get_bbox()

        try:
            throughBot = othero.isPlatform  # 밑에서 위로 통과할 수 있다면
        except AttributeError:
            throughBot = false

        if not throughBot or (throughBot and sy >= oy):
            if sx >= ox + ow: return false  # Right
            if sx + sw <= ox: return false  # Left
            if sy + sh <= oy: return false  # Top
            if sy >= oy + oh: return false  # Bottom
        elif throughBot:
            return false
        return true

    def get_bbox(self) -> tuple:
        data = self.sprite_index
        return int(self.x - data.xoffset), int(self.y - data.yoffset), data.width, data.height

    def draw_bbox(self):
        draw_set_alpha(1)
        draw_set_color(255, 0, 0)
        draw_rectangle_outline(*self.get_bbox(), Camera.x, Camera.y)

    # Check the place fits to self
    def place_free(self, vx = 0, vy = 0, olist = None) -> bool:
        clist = olist
        if clist is None:
            global instance_list_spec
            clist = instance_list_spec[ID_SOLID]  # 고체 개체 목록 불러오기

        toUp = false
        if vy > 0:
            toUp = true
        length = len(clist)
        if length > 0:
            # print("Checking Place for one")
            self.x += vx
            self.y += vy
            for inst in clist:
                if self is inst or (toUp and inst.isPlatform):
                    continue
                if self.instance_collide(inst):
                    self.x -= vx
                    self.y -= vy
                    return false
            self.x -= vx
            self.y -= vy
            return true
        else:
            return true

    def move_contact_x(self, dist: float or int = 1, right: bool = false) -> bool:
        tdist = dist
        if dist < 0:
            tdist = 1000000
        if dist == 0:
            return false

        global instance_list_spec
        clist = instance_list_spec[ID_SOLID]
        length = len(clist)
        xprog = 0
        cx = 0
        if length > 0:
            while xprog <= tdist:
                if not self.place_free(cx + sign(cx) * 2):
                    self.x += cx
                    return true
                if right:
                    cx += 1
                else:
                    cx -= 1
                xprog += 1
            return false
        else:
            return false

    def phy_collide(self, how: float or int):
        if self.xVel != 0:
            self.move_contact_x(abs(how), how > 0)
            if self.oStatus >= oStatusContainer.STUNNED:
                self.xVel *= -0.4
            else:
                self.xVel = 0
        self.x = math.floor(self.x)

    def move_contact_y(self, dist: float or int = 1, up: bool = false) -> bool:
        tdist = math.floor(dist)
        if dist < 0:
            tdist = 1000000
        if dist == 0:
            return false

        global instance_list_spec
        clist = instance_list_spec[ID_SOLID]
        length = len(clist)
        yprog = 0
        cy = 0
        if length > 0:
            templist = []
            for inst in clist:
                if bool(inst.y - inst.sprite_index.yoffset <= int(
                        self.y - self.sprite_index.yoffset + self.sprite_index.height)) != up and \
                        ((not up and inst.isPlatform) or not up):
                    templist.append(inst)

            while yprog <= tdist:
                if not self.place_free(0, cy + sign(cy) * 2, templist):
                    self.y += cy
                    return true
                if up:
                    cy -= 1
                else:
                    cy -= 1
                yprog += 1
            return false
        else:
            return false

    def phy_thud(self, how: float or int):
        if self.yVel != 0:
            if self.yVel > 0:
                self.move_contact_y(abs(how) + 1, true)
            elif self.yVel < 0:
                self.move_contact_y(abs(how) + 1)
            if self.oStatus >= oStatusContainer.STUNNED:
                if abs(how) <= 3:
                    self.yVel = 0
                    if self.onAir:
                        audio_play("sndBounce")
                        self.onAir = false
                else:
                    self.yVel *= -0.4
                    audio_play("sndBounce")
            else:
                if self.yVel <= 0:
                    self.yVel = 0
                    self.y = math.floor(self.y)
                    if self.onAir:
                        self.onAir = false
                        self.y += 0.1
                        audio_play("sndLand")
                else:
                    self.yVel *= -0.3
                    audio_play("sndBounceLit")
        else:
            self.onAir = false
        self.y = math.floor(self.y + 0.5)

    def draw_self(self) -> None:  # Simply draws its sprite on its position.
        data = self.sprite_index
        if data is not None:
            draw_sprite(self.sprite_index, self.image_index, self.x - Camera.x, self.y - Camera.y,
                        self.image_xscale, 1, 0.0,
                        self.image_alpha)

    def event_step(self, frame_time) -> None:  # The basic mechanisms of objects.
        if self.name == "Player":
            self.visible = true
        elif self.instance_collide(Camera):
            self.visible = true
        else:
            self.visible = false
        if not self.visible:
            return

        try:
            count = self.sprite_index.number
        except AttributeError:
            raise RuntimeError(self.name + " 는 스프라이트를 갖고있지 않습니다!")
        if count > 1:
            if self.image_speed > 0:
                self.image_index += self.image_speed * count * frame_time * 2.5
                if self.image_index >= count:
                    self.image_index -= count

        if not self.step_enable:
            return

        if self.xVel != 0:
            xdist = delta_velocity(self.xVel) * frame_time
            xc = xdist + sign(xdist)
            if self.place_free(xc):
                self.x += xdist
            else:
                self.phy_collide(xdist)

        if self.yVel != 0 and self.yFric != 0:
            if abs(self.yVel) > self.yFric:
                self.yVel -= self.yFric * self.yVel
            else:
                self.xVel = 0
        ydist = delta_velocity(self.yVel) * frame_time
        if ydist > 0:  # Going up higher
            yc = ydist + 1
        else:  # Going down
            yc = ydist - 1
        if self.place_free(0, yc):
            self.y += ydist  # let it moves first.
            self.gravity = self.gravity_default
            self.yVel -= self.gravity * frame_time
            self.onAir = true
        else:
            self.gravity = 0
            if self.xVel != 0:  # horizontal friction works only when it is on the ground
                if abs(self.xVel) > self.xFric:
                    self.xVel -= self.xFric * self.xVel
                else:
                    self.xVel = 0
            self.phy_thud(ydist)

        self.xVel = clamp(self.xVelMin, self.xVel, self.xVelMax)
        self.yVel = clamp(self.yVelMin, self.yVel, self.yVelMax)

    def event_draw(self):  # This will be working for drawing.
        if self.visible:
            self.draw_self()
        # self.draw_bbox()


# Object : Solid Objects
class Solid(GObject):
    # reset some inherited variables
    name = "Solid"
    identify = ID_TILE  # It is not real collidable

    # 아래에서 통과가능한지의 여부
    isPlatform: bool = false

    image_speed = 0
    depth = 10000
    step_enable = false
    gravity_default = 0
    xFric, yFric = 0, 0

    tile_left: int = 0
    tile_right: int = 0
    tile_up: int = 0
    tile_down: int = 0

    def tile_correction(self):
        pass


# Parent of Items
class oItemParent(GObject):
    name = "Item"
    identify = ID_ITEM
    depth = 400
    image_speed = 0
    rot = 0

    def __init__(self, nd, nx, ny):
        super().__init__(nd, nx, ny)
        self.starty = ny

    def event_step(self, frame_time):
        super().event_step(frame_time)
        if self.gravity_default == 0:
            self.y = self.starty + 12 + math.sin(self.rot * math.pi / 180) * 3
            self.rot = (self.rot + 1) % 360


# Parent of Terrain Doodads
class oDoodadParent(GObject):
    name = "Doodad"
    parent: Solid = None
    identify = ID_DOODAD
    gravity_default = 0
    step_enable = false
    depth = -100

    tile_up: bool = false
    tile_down: bool = false

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)

    def parent_set(self, id):
        self.parent = id

    def parent_get(self):
        return self.parent

    def tile_correction(self):
        pass


# Parent of Effect
class oEffectParent(GObject):
    name = "Fx Effect"
    identify = ID_EFFECT
    image_speed = 0.5
    depth = -400


def instance_place(Ty, fx, fy) -> (list, int):
    try:
        ibj = Ty.identify
    except AttributeError:
        raise RuntimeError("Cannot find variable 'identify' in %s" % (str(Ty)))

    __returns = []
    if ibj == "":
        clist = get_instance_list(ID_OVERALL)
    else:
        clist = get_instance_list(ibj)
    length = len(clist)
    if length > 0:
        for inst in clist:
            if isinstance(inst, Ty) and point_in_rectangle(fx, fy, *inst.get_bbox()):
                __returns.append(inst)

    return __returns, len(__returns)


def instance_place_single(Ty, fx, fy):
    try:
        ibj = Ty.identify
    except AttributeError:
        raise RuntimeError("Cannot find variable 'identify' in %s" % (str(Ty)))

    if ibj == "":
        clist = get_instance_list(ID_OVERALL)
    else:
        clist = get_instance_list(ibj)
    length = len(clist)
    if length > 0:
        for inst in clist:
            if isinstance(inst, Ty) and point_in_rectangle(fx, fy, *inst.get_bbox()):
                return inst

    return None
