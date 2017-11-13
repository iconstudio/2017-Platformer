from module.pico2d import *
from module.functions import *
from module.constants import *

import math
from module.framework import io
from module.framework import Camera

from module.sprite import *
from module.terrain import *

import math
import sys

__all__ = [
    "instance_last", "instance_list_spec", "instance_draw_list", "instance_update", "instance_list",
    "container_player", "instance_create", "instance_draw_update",
    "GObject", "Solid", "oBrick", "oPlayer", "oSoldier", "oSnake", "oCobra",
    "ID_SOLID", "ID_DMG_PLAYER", "ID_DMG_ENEMY", "ID_ITEM", "ID_PARTICLE", "ID_DOODAD"
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
instance_update: bool = true   # 개체 갱신 여부

player_lives = 3

ID_OTHERS: str = "Objects"
ID_SOLID: str = "Solid"
ID_PARTICLE: str = "Particle"
ID_DOODAD: str = "Doodad"
ID_DMG_PLAYER: str = "HurtPlayer"
ID_DMG_ENEMY: str = "HurtEnemy"
ID_ENEMY: str = "Enemy"
ID_ITEM: str = "Items"
instance_list_spec[ID_OTHERS] = []
instance_list_spec[ID_SOLID] = []
instance_list_spec[ID_PARTICLE] = []
instance_list_spec[ID_DOODAD] = []
instance_list_spec[ID_DMG_PLAYER] = []
instance_list_spec[ID_DMG_ENEMY] = []
instance_list_spec[ID_ENEMY] = []
instance_list_spec[ID_ITEM] = []

container_player = None


def instance_draw_update():
    global instance_list, instance_draw_list, instance_update
    if instance_update or len(instance_draw_list) <= 0:
        del instance_draw_list
        instance_update = false
        instance_draw_list = sorted(instance_list, key=lambda gobject: -gobject.depth)


# TODO: Definite more objects.
# Declaring of Special Objects ( Need a canvas )

# ==================================================================================================
#                                               게임
# ==================================================================================================
# Object : A container of Status
class oStatusContainer:
    NONE = 0
    IDLE = 1
    WALK = 8
    RUNNING = 10
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

        del instance_list[list_seek(instance_list, self)]
        del instance_list_spec[self.identify][list_seek(instance_list_spec[self.identify], self)]
        del instance_draw_list[list_seek(instance_draw_list, self)]
        del (self)

    # Below methods are common-functions for all object that inherits graviton.
    def get_bbox(self):
        data = self.sprite_index
        return self.x - data.xoffset, self.y - data.yoffset, self.x - data.xoffset + data.width, self.y - data.yoffset + data.height

    # Check the place fits to self
    def place_free(self, vx, vy, olist = None) -> bool:
        clist = olist
        if clist is None:
            global instance_list_spec
            clist = instance_list_spec["Solid"]  # 고체 개체 목록 불러오기

        length = len(clist)
        if length > 0:
            # print("Checking Place for one")
            bbox_left = int(self.x - self.sprite_index.xoffset + vx)
            bbox_top = int(self.y - self.sprite_index.yoffset + vy)
            brect = SDL_Rect(bbox_left, bbox_top, self.sprite_index.width, self.sprite_index.height + 3)
            temprect = SDL_Rect()

            for inst in clist:
                tempspr: Sprite = inst.sprite_index
                otho_left = int(inst.x - tempspr.xoffset)
                otho_top = int(inst.y - tempspr.yoffset)
                temprect.x, temprect.y, temprect.w, temprect.h = otho_left, otho_top, tempspr.width, tempspr.height
                if rect_in_rectangle_opt(brect, temprect):
                    del temprect
                    return false
            del temprect
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

    def collide(self, how: float or int):
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
                if not self.place_free(0, cy + sign(cy), templist):
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

    def thud(self, how: float or int):
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
                self.onAir = false
                self.yVel = 0
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
                self.collide(xdist)

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
            self.thud(ydist)

        self.xVel = clamp(self.xVelMin, self.xVel, self.xVelMax)
        self.yVel = clamp(self.yVelMin, self.yVel, self.yVelMax)

    def event_draw(self):  # This will be working for drawing.
        self.draw_self()


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


# ==================================================================================================
#                                    사용자 정의 객체 / 함수
# ==================================================================================================
# Object : Functions
def instance_create(Ty, depth = int(0), x = int(0), y = int(0)) -> object:
    temp = Ty(depth, x, y)
    global instance_last
    instance_last = temp
    return temp


def instance_place(Ty, fx, fy) -> (list, int):
    try:
        ibj = Ty.identify
    except AttributeError:
        print("Cannot find variable 'identify' in %s" % (str(Ty)))
        sys.exit(-1)

    __returns = []
    global instance_list, instance_list_spec
    if ibj == "":
        clist = instance_list
    else:
        clist = instance_list_spec[ibj]
    length = len(clist)
    if length > 0:
        for inst in clist:
            tempspr: Sprite = inst.sprite_index
            otho_left = int(inst.x - tempspr.xoffset)
            otho_top = int(inst.y - tempspr.yoffset)
            if point_in_rectangle(fx, fy, otho_left, otho_top, otho_left + tempspr.width, otho_top + tempspr.height):
                __returns.append(inst)

    return __returns, len(__returns)


# Definitions of Special Objects
# Brick
class oBrick(Solid):
    name = "Brick of Mine"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sCastleBrick")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3)


# Player
class oPlayer(GObject):
    name = "Player"
    depth = 0
    image_speed = 0
    # anitem what to hold on
    held: object = None

    # real-scale: 54 km per hour
    xVelMin, xVelMax = -54, 54

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_index = sprite_get("Player")

        global container_player
        container_player = self
        self.hfont = load_font(path_font + "윤고딕_310.ttf", 20)

    def event_step(self, frame_time):
        super().event_step(frame_time)
        if self.oStatus < oStatusContainer.CHANNELING:  # Player can control its character.
            Camera.x, Camera.y = self.x - Camera.width / 2, self.y - Camera.height / 2
            # Stomp enemies under the character
            whothere, howmany = instance_place(oEnemyParent, self.x, self.y - 9)
            if howmany > 0 and self.yVel < 0 and self.onAir:
                for enemy in whothere:
                    if enemy.oStatus < oStatusContainer.STUNNED:
                        if enemy.name not in ("ManEater", "Lavaman",):
                            if self.yVel < -20:
                                self.yVel *= -0.6
                            else:
                                self.yVel = 30
                            enemy.hp -= 1
                            if enemy.hp <= 0:
                                enemy.status_change(oStatusContainer.DEAD)
                            else:
                                enemy.status_change(oStatusContainer.STUNNED)
                                enemy.stunned = delta_velocity(5)

            mx = 0
            if io.key_check(SDLK_LEFT): mx -= 1
            if io.key_check(SDLK_RIGHT): mx += 1

            if mx != 0:
                self.xFric = 0
                if not self.onAir:
                    self.xVel += mx * 5
                else:
                    self.xVel += mx * 2
                self.image_xscale = mx
            else:
                self.xFric = 0.6

            if io.key_check_pressed(SDLK_UP):
                if not self.onAir:
                    self.yVel = 90

            if not self.onAir:
                if self.xVel != 0:
                    self.image_speed = 0.8
                    self.sprite_index = sprite_get("PlayerRun")
                else:
                    self.sprite_set("Player")
            else:
                self.sprite_set("PlayerJump")
        else:  # It would be eventual, and uncontrollable
            if self.oStatus == oStatusContainer.DEAD:
                self.sprite_set("PlayerDead")

    def event_draw(self):
        super().event_draw()
        self.hfont.draw(self.x - 40 - Camera.x, self.y + 50 - Camera.y, 'Time: %1.0f' % get_time())


# Parent of Enemies
class oEnemyParent(GObject):
    """
            모든 적 객체의 부모 객체
    """
    name = "NPC"
    identify = ID_ENEMY
    # sprite_index = sprite_get("Snake")
    depth = 100

    hp, maxhp = 1, 1
    mp, maxmp = 0, 0
    oStatus = oStatusContainer.IDLE
    image_speed = 0
    collide_with_player: bool = false
    attack_delay = 0

    def handle_none(self, *args):
        pass

    def handle_be_idle(self, *args):
        pass

    def handle_be_walk(self, *args):
        pass

    def handle_be_stunned(self, *args):
        pass

    def handle_be_dead(self, *args):
        pass

    def handle_idle(self, *args):
        pass

    def handle_walk(self, *args):
        pass

    def handle_dead(self, *args):
        pass

    def handle_stunned(self, frame_time):
        if self.stunned <= 0:
            if self.hp > 0:
                self.status_change(oStatusContainer.IDLE)
            else:
                self.status_change(oStatusContainer.DEAD)
        self.stunned -= delta_velocity() * frame_time

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.table = {
            oStatusContainer.IDLE: (self.handle_idle, self.handle_be_idle),
            oStatusContainer.WALK: (self.handle_walk, self.handle_be_walk),
            oStatusContainer.STUNNED: (self.handle_stunned, self.handle_be_stunned),
            oStatusContainer.DEAD: (self.handle_dead, self.handle_be_dead)
        }

    def status_change(self, what):
        if self.oStatus != what:
            (self.table[what])[1]()
        self.oStatus = what

    def event_step(self, frame_time):
        super().event_step(frame_time)

        (self.table[self.oStatus])[0](frame_time)


class oSoldier(oEnemyParent):
    hp, maxhp = 4, 4
    name = "Soldier"
    xVelMin, xVelMax = -45, 45

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("SoldierIdle")
        self.runspr = sprite_get("SoldierRun")
        self.image_speed = 0

    def handle_be_idle(self):
        self.sprite_set("SoldierIdle")

    def handle_be_stunned(self):
        self.sprite_set("SoldierDead")

    def handle_be_dead(self):
        self.sprite_set("SoldierDead")

    def handle_idle(self, *args):
        pass

    def handle_dead(self, *args):
        pass

    def handle_stunned(self, frame_time):
        super().handle_stunned(frame_time)


class oSnake(oEnemyParent):
    hp, maxhp = 1, 1
    name = "Snake"
    count = 0

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("SnakeIdle")
        self.runspr = sprite_get("SnakeRun")
        self.image_speed = 0

    def handle_be_idle(self):
        self.sprite_set("SnakeIdle")

    def handle_be_walk(self, *args):
        self.sprite_index = self.runspr
        self.image_speed = 0.65

    def handle_idle(self, *args):
        self.count += delta_velocity()
        if self.count >= delta_velocity(irandom_range(8, 12)) and irandom(99) == 0:
            self.status_change(oStatusContainer.WALK)
            self.count = 0

    def handle_walk(self, *args):
        checkl, checkr = self.place_free(-10, -10), self.place_free(10, -10)
        if checkl and checkr:
            self.status_change(oStatusContainer.WALK)
            return

        distance = delta_velocity(15) * args[0]
        self.count += delta_velocity()
        if self.image_xscale == 1:
            if self.place_free(distance + 10, 0) and not self.place_free(distance + 10, -10):
                self.xVel = 15
            else:
                self.image_xscale = -1
                self.xVel = -15
        else:
            if self.place_free(distance - 10, 0) and not self.place_free(distance - 10, -10):
                self.xVel = -15
            else:
                self.image_xscale = 1
                self.xVel = 15

        if self.count >= delta_velocity(20):
            if irandom(99) == 0:
                self.xVel = 0
                self.status_change(oStatusContainer.IDLE)
                self.count = 0

    def handle_dead(self, *args):
        self.destroy()


class oCobra(oSnake):
    name = "Cobra"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("CobraIdle")
        self.runspr = sprite_get("CobraRun")
        self.image_speed = 0

    def handle_be_idle(self):
        self.sprite_set("CobraIdle")


# Damage caused by Player
class oPlayerDamage(GObject):
    name = "DamageP"
    identify = ID_DMG_PLAYER
    gravity_default = 0
    life = fps_target


# Damage caused by Enemy
class oEnemyDamage(GObject):
    name = "DamageE"
    identify = ID_DMG_ENEMY
    gravity_default = 0
    life = fps_target


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
