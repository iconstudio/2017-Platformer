from module.pico2d import *
from module.functions import *
from module.constants import *

import math
from module.framework import Camera

from module.sprite import *

__all__ = [
    "oStatusContainer",
    "instance_last", "instance_list_spec", "instance_draw_list", "instance_update", "instance_list",
    "container_player", "GObject", "Solid",
    "ID_OTHERS", "ID_SOLID", "ID_DMG_PLAYER", "ID_DMG_ENEMY", "ID_ENEMY", "ID_ITEM", "ID_PARTICLE", "ID_DOODAD",
    "ID_EFFECT"
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

player_lives = 3

ID_OTHERS: str = "Objects"
ID_SOLID: str = "Solid"
ID_PARTICLE: str = "Particle"
ID_DOODAD: str = "Doodad"
ID_DMG_PLAYER: str = "HurtPlayer"
ID_DMG_ENEMY: str = "HurtEnemy"
ID_ENEMY: str = "Enemy"
ID_ITEM: str = "Items"
ID_EFFECT: str = "Effect"
instance_list_spec[ID_OTHERS] = []
instance_list_spec[ID_SOLID] = []
instance_list_spec[ID_PARTICLE] = []
instance_list_spec[ID_DOODAD] = []
instance_list_spec[ID_DMG_PLAYER] = []
instance_list_spec[ID_DMG_ENEMY] = []
instance_list_spec[ID_ENEMY] = []
instance_list_spec[ID_ITEM] = []
instance_list_spec[ID_EFFECT] = []

container_player = None


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
    image_alpha: float = 1.0
    image_index = float(0)
    image_speed = float(0)
    visible: bool = true
    depth: int = 0
    image_xscale: float = 1

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
        if self.step_enable:
            self.step_enable = false
            self.destroy()

    def sprite_set(self, spr: Sprite or str):
        if type(spr) == str:
            self.sprite_index = sprite_get(spr)
        else:
            self.sprite_index = spr
        self.image_index = 0

    def destroy(self):
        self.step_enable = false
        global instance_list, instance_list_spec, instance_update, instance_draw_list
        instance_update = true

        instance_list.remove(self)
        (instance_list_spec[self.identify]).remove(self)
        instance_draw_list.remove(self)
        del self

    # Below methods are common-functions for all object that inherits graviton.
    def instance_collide(self, b):
        sx, sy, sw, sh = self.get_bbox()
        ox, oy, ow, oh = b.get_bbox()

        if sx >= ox + ow: return False
        if sx + sw <= ox: return False
        if sy + sh <= oy: return False
        if sy >= oy + oh: return False
        return True

    def get_bbox(self):
        data = self.sprite_index
        return int(self.x - data.xoffset), int(self.y - data.yoffset), data.width, data.height

    def draw_bbox(self):
        draw_rectangle(*self.get_bbox())

    # Check the place fits to self
    def place_free(self, vx = 0, vy = 0, olist = None) -> bool:
        clist = olist
        if clist is None:
            global instance_list_spec
            clist = instance_list_spec["Solid"]  # 고체 개체 목록 불러오기

        length = len(clist)
        if length > 0:
            # print("Checking Place for one")
            self.x += vx
            self.y += vy
            for inst in clist:
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
        clist = instance_list_spec["Solid"]
        length = len(clist)
        xprog = 0
        cx = 0
        if length > 0:
            while xprog <= tdist:
                if not self.place_free(cx + sign(cx) * 2, 0):
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
        tdist = math.ceil(dist)
        if dist < 0:
            tdist = 1000000
        if dist == 0:
            return false

        global instance_list_spec
        clist = instance_list_spec["Solid"]
        length = len(clist)
        yprog = 0
        cy = 0
        if length > 0:
            templist = []
            for inst in clist:
                if bool(inst.y - inst.sprite_index.yoffset <= int(
                                        self.y - self.sprite_index.yoffset + self.sprite_index.height)) != up:
                    templist.append(inst)

            while yprog <= tdist:
                if not self.place_free(0, cy + sign(cy) * 2, templist):
                    self.y += cy
                    return true
                if up:
                    cy += 1
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
                if abs(self.yVel) <= 3:
                    self.onAir = false
                    self.yVel = 0
                else:
                    self.yVel *= -0.4
            else:
                if self.yVel <= 0:
                    self.onAir = false
                    self.yVel = 0
                else:
                    self.yVel *= -0.6
        else:
            self.onAir = false
        self.y = math.ceil(self.y)

    def draw_self(self):  # Simply draws its sprite on its position.
        data = self.sprite_index
        if not data.__eq__(None):
            dx, dy = self.x - data.xoffset, self.y - data.yoffset
            if dx <= Camera.x + Camera.width and Camera.x <= dx + data.width and Camera.y <= dy + data.height and dy <= Camera.y + Camera.height:
                draw_sprite(self.sprite_index, self.image_index, self.x - Camera.x, self.y - Camera.y,
                            self.image_xscale, 1, 0.0,
                            self.image_alpha)

    def event_step(self, frame_time):  # The basic mechanisms of objects.
        if not self.step_enable:
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

        if self.xVel != 0:
            xdist = delta_velocity(self.xVel) * frame_time
            xc = xdist + sign(xdist)
            if self.place_free(xc, 0):
                self.x += xdist
            else:
                self.phy_collide(xdist)

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
        self.draw_self()
        # self.draw_bbox()


# Object : Solid Objects
class Solid(GObject):
    # reset some inherited variables
    name = "Solid"
    identify = ID_SOLID

    image_speed = 0
    depth = 1000
    step_enable = false
    gravity_default = 0
    xFric, yFric = 0, 0
