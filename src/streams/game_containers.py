from pico2d import *
from functions import *
from constants import *

from sprite import *
from terrain import *

__all__ = [
    "instance_last", "instance_list_spec", "instance_draw_list", "instance_update", "instance_list",
    "container_player", "instance_create", "place_free", "io",
    "GObject", "Solid", "oBrick", "oPlayer",
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

container_player = None


# ==================================================================================================
#                                               게임
# ==================================================================================================


# Object : Game Object
class GObject(object):
    name: str = "None"
    identify: str = ""
    next: object = None

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
    gravity_default: float = 0.4
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
        global instance_list, instance_list_spec, instance_draw_list, instance_update
        instance_update = true

        if self.identify != "":
            instance_list_spec[self.identify].append(self)

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

    def move_contact_y(self, dist=1, up: bool = false) -> bool:
        if dist < 0:
            dist = 1000000

        global instance_list_spec
        clist = instance_list_spec["Solid"]
        length = len(clist)
        yprog = 0
        if length > 0:
            bbox_x = int(self.x - self.sprite_index.xoffset)
            bbox_y = int(self.y - self.sprite_index.yoffset)
            if up:
                bbox_y += 1
            else:
                bbox_y -= 1
            brect = SDL_Rect(bbox_x, bbox_y, self.sprite_index.width, self.sprite_index.height)
            temprect = SDL_Rect()
            templist = []
            for inst in clist:
                if bool(inst.y + inst.sprite_index.yoffset <= brect.y + brect.h) != up:
                    templist.append(inst)

            while yprog <= dist:
                for inst in templist:
                    tempspr: Sprite = inst.sprite_index
                    otho_left = int(inst.x - tempspr.xoffset)
                    otho_top = int(inst.y - tempspr.yoffset)
                    temprect.x, temprect.y, temprect.w, temprect.h = otho_left, otho_top, tempspr.width, tempspr.height
                    if rect_in_rectangle_opt(brect, temprect):
                        return true
                if up:
                    brect.y += 1
                    yprog += 1
                else:
                    brect.y -= 1
                    yprog += 1
            return false
        else:
            return false

    def thud(self):
        # if self.yVel != 0:
        self.move_contact_y(abs(self.yVel))
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


# ==================================================================================================
#                                    사용자 정의 객체 / 함수
# ==================================================================================================



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


# Definitions of Special Objects
class oBrick(Solid):
    name = "Brick of Mine"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_index = sprite_get("sCastleBrick")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3)


# Object : IO procedure
class oIOProc:
    class iochecker(GObject):
        gravity = 0
        life = 2
        owner = None

        def __init__(self, nowner):
            super().__init__(-100000, -10000, -10000)
            self.owner = nowner

        def event_step(self):
            self.life -= 1
            if self.life <= 0:
                self.owner.check_pressed = false
                del self

    class ionode:
        code = None
        check: bool = false
        check_pressed: bool = false

    key_list = {}

    def key_add(self, key: SDL_Keycode):
        newnode = self.ionode()
        self.key_list[key] = newnode
        return newnode

    def proceed(self, kevent):
        try:
            node = self.key_list[kevent.key]

            if kevent.type == SDL_KEYDOWN:
                node.check = true
                node.check_pressed = true
                self.iochecker(node)
                #print(true)
            elif kevent.type == SDL_KEYUP:
                node.check = false
                node.check_pressed = false
                #print(false)
        except KeyError:
            return

io = oIOProc()


# Player
class oPlayer(GObject):
    name = "Player"

    def __cmd__handle_mvl(self):
        self.xVel = -3

    def __cmd__handle_mvr(self):
        self.xVel = 3

    def __cmd__handle_jmp(self):
        if not self.onAir:
            self.yVel = 6

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_index = sprite_get("Player")
        self.image_speed = 0

        global container_player
        container_player = self


# Parent of Enemies
class oEnemyParent(GObject):
    name = "NPC"

    oStatus = oStatusContainer.IDLE


# Damage caused by Player
class oPlayerDamage(GObject):
    name = "DamageP"
    identify = ID_DMG_PLAYER
    gravity_default = 0
    life = 60


# Damage caused by Enemy
class oEnemyDamage(GObject):
    name = "DamageE"
    identify = ID_DMG_ENEMY
    gravity_default = 0
    life = 60


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
