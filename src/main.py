from pico2d import *
from .module import functions

import framework
import game

name = "main_state"

'''
        수정 사항:
            1. pico2d.py 의 open_canvas 함수 수정 (창 핸들 반환)
'''

# Global : Constants
false = False
true = True
scr_defw:int = 640
scr_defh:int = 360
scr_scale:int = 1

# Global : Variables
running:bool = true                                 # 전역 진행 변수

sprite_list:dict = {}                               # 스프라이트는 이름으로 구분된다.
instance_last:bool= None                            # 마지막 개체
instance_list:list = []                             # 개체는 순서가 있다.
'''
        <List> instance_list_spec:

            목적: 객체를 종류 별로 담기 위한 리스트
            용법:
                instance_list_spec[객체 이름] = []
                instance_list_spec[객체 이름].append(객체 ID)

            비고: 객체 이름 외에도 "Solid", "Particle" 등의 구별자 사용.
'''
instance_list_spec:dict = {}                         # 객체 종류 별 목록
instance_draw_list:list = []                         # 개체 그리기 목록
instance_update:bool = false                         # 개체 갱신 여부
#event_queue = []                                    # 이벤트 목록

ID_SOLID:str= "Solid"
ID_PARTICLE:str = "Particle"
ID_DOODAD:str = "Doodad"
ID_DMG_PLAYER:str = "HurtPlayer"
ID_DMG_ENEMY:str = "HurtEnemy"
instance_list_spec[ID_SOLID] = []
instance_list_spec[ID_PARTICLE] = []
instance_list_spec[ID_DOODAD] = []
instance_list_spec[ID_DMG_PLAYER] = []
instance_list_spec[ID_DMG_ENEMY] = []

# Object : Game
class __Game:
    hwnd = None
    width = scr_defw
    height = scr_defh
    dgan = 0.05

    class __Camera:
        x:float = 0
        y:float = 0
        width, height = scr_defw, scr_defh

        def set_pos(self, x:float = None, y:float = None):
            if x != None:
                self.x = x
            if y != None:
                self.y = y

        def add_pos(self, x:float = None, y:float = None):
            if x != None:
                self.x += x
            if y != None:
                self.y += y
    camera = __Camera()

    def __init__(self, nw = int(scr_defw), nh = int(scr_defh)):
        self.width = nw
        self.height = nh

    def __del__(self):
        close_canvas()

    def begin(self):
        self.hwnd = open_canvas(self.width, self.height, true)
        SDL_SetWindowTitle(self.hwnd, ("Vampire Exodus").encode("UTF-8"))
        SDL_SetWindowSize(self.hwnd, scr_defw * scr_scale, scr_defh * scr_scale)

        #x, y = ctypes.c_int(), ctypes.c_int()
        #SDL_GetWindowPosition(self.hwnd, ctypes.byref(x), ctypes.byref(y))
        #x, y = x.value, y.value
        #vscl = scr_scale * 2
        #dx, dy = int(x - scr_defw * scr_scale / vscl), int(y - scr_defh * scr_scale / vscl)

        #SDL_SetWindowPosition(self.hwnd, c_int(dx), c_int(dy))
        #SDL_SetWindowFullscreen(self.hwnd, ctypes.c_uint32(1))


        hide_cursor()
        hide_lattice()

    # Proceed instance
    def instance_draw_update(self):
        global instance_draw_list, instance_update
        if instance_update:
            del instance_draw_list
            instance_update = false
            instance_draw_list = []
            for inst in instance_list:
                instance_draw_list.append(inst)

    # Event : Global
    def event_global(self):
        global event_queue, running

        for event in event_queue:
            if (event.type == SDL_QUIT):
                running = False
            elif (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
                running = False

        return running

    # Main Procedure
    def process(self):
        while running:
            global event_queue
            clear_canvas()

            event_queue = get_events()
            if not self.event_global():
                break

            if len(instance_list) > 0:
                for inst in instance_list:
                    if inst.step_enable:
                        inst.event_step()

                self.instance_draw_update()
                for inst in instance_draw_list:
                    if inst.visible:
                        inst.event_draw()
                update_canvas()

            delay(self.dgan)

# Object : Sprites
class __Sprite(object):
    number = 0

    def __init__(self, filepath, number):
        self.__data__ = load_image(filepath)

        # the number of sprite in a image
        self.number = number
        # size of each index
        try:
            self.width = int(self.__data__.w / number)
            self.height = int(self.__data__.h / number)

            tempTy = type(number)
            if tempTy != int and tempTy != float:
                raise RuntimeError("스프라이트 불러오기 시 인자가 숫자가 아닙니다.")
        except ZeroDivisionError:
            raise RuntimeError("스프라이트의 갯수는 0개가 될 수 없습니다.")

    def draw(self, index, x, y, xscale = float(1), yscale = float(1), rot = float(0.0)):
        if rot != 0.0: # pico2d does not support scaling + rotating draw.
            self.__data__.rotate_draw(rot, x * scr_scale, y * scr_scale, int(self.width * xscale) * scr_scale,  int(self.height * yscale) * scr_scale)
        else:
            self.__data__.clip_draw(int(index * self.width), 0, self.width, self.height, x * scr_scale, y * scr_scale, int(self.width * xscale) * scr_scale, int(self.height * yscale) * scr_scale)

def place_free(dx, dy):
    clist = instance_list_spec["Solid"] # 고체 개체 목록 불러오기
    length = len(clist)
    if length > 0:
        for inst in clist:
            tempspr:__Sprite = inst.sprite_index
            if functions.point_in_rectangle(dx, dy, inst.x - tempspr.width / 2, inst.y - tempspr.height / 2, inst.x + tempspr.width / 2, inst.y + tempspr.height / 2):
                return true;

        return true
    else:
        return false

# Object : Gravitons
class __Graviton(object):
    name = "None"
    identify = ""
    next = None

    # Properties of sprite
    sprite_index = None
    image_index = float(0)
    image_speed = float(0)
    visible = true
    depth = 0

    # for optimization
    step_enable = true

    x, y = 0, 0
    xVel, yVel = 0, 0
    xFric, yFric = 0.4, 1
    gravity_default = 0.4
    gravity = 0
    onAir = false

    def __init__(self, ndepth = int(0), nx = int(0), ny = int(0)):
        self.depth = ndepth
        self.x, self.y = nx, ny

        global instance_list_spec
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

    def draw_self(self): # Simply draws its sprite on its position.
        if (self.sprite_index != None):
            draw_sprite(self.sprite_index, self.image_index, self.x, self.y)

    def event_step(self): # The basic machanism of objects.
        if self.xVel != 0:
            xc = self.x + self.xVel + functions.sign(self.xVel)
            if place_free(xc, self.y):
                self.x += self.xVel
            else:
                self.collide()

        if self.yVel > 0:   # Going up higher
            yc = self.y + self.yVel + 1
        else:               # Going down
            yc = self.y + self.yVel - 1

        if place_free(self.x, yc):
            self.y += self.yVel                     # let it moves first.
            self.gravity = self.gravity_default
            self.yVel -= self.gravity
            self.onAir = true
        else:
            self.gravity = 0
            if self.xVel != 0:                      # horizontal friction works only when it is on the ground
                self.xVel *= self.xFric
            self.thud()

    def event_draw(self): # This will be working for drawing.
        self.draw_self()

# Object : Solid Objects
class __Solid(__Graviton):
    # reset some inherited variables
    name = "Solid"
    identify = ID_SOLID
    step_enable = false
    gravity_default = 0
    xFric, yFric = 0, 0

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)

# Main : Game Settings
Game = __Game()
Game.begin()
Camera = Game.camera

# Object : Functions
def sprite_load(filepath: str, name = str("default"), number = int(1)):
    new = __Sprite(filepath, number)
    sprite_list[name] = new
    return new

def draw_sprite(spr: __Sprite, index, x = int(0), y = int(0), xscale = float(1), yscale = float(1), rot = float(0.0)):
    spr.draw(index, x, y, xscale, yscale, rot)

def instance_create(Ty, depth = int(0), x = int(0), y = int(0)):
    global Game, instance_update, instance_last

    temp = Ty.__new__(Ty)
    temp.depth = depth
    temp.x = x
    temp.y = y
    if instance_last != None and isinstance(__Graviton, instance_last):
        instance_last.next = temp

    instance_last = temp
    instance_list.append(instance_last)
    instance_update = true

    return instance_last

# TODO: Definite more objects.
# Definitions of Special Objects ( Need a canvas )
sMineBrick_0 = sprite_load("..\\res\\img\\theme\\brick_mine_0.png", "MineBrick1")
sMineBrick_1 = sprite_load("..\\res\\img\\theme\\brick_mine_1.png", "MineBrick2")
sMineBrick_b = sprite_load("..\\res\\img\\theme\\brick_mine_bot.png", "MineBrickB")
class oMineBrick(__Solid):
    name = "Brick of Mine"
    sprite_index = functions.distribute(sMineBrick_0, sMineBrick_1, 0.9)

testo = instance_create(oMineBrick, 0, 100, 100)

Game.process()

del Game
