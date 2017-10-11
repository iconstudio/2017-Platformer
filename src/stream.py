
from pico2d import *
import math
import random
import collections

# Global : Constants
false = False
true = True
scr_defw = 608
scr_defh = 352

# Global : Variables
running = true                                  # 전역 진행 변수

sprite_list = {}                                # 스프라이트는 이름으로 구분된다.
instance_last = None                            # 마지막 개체
instance_list = []                              # 개체는 순서가 있다.
'''
        <List> instance_list_spec:

            목적: 객체를 종류 별로 담기 위한 리스트
            용법:
                instance_list_spec[객체 이름] = []
                instance_list_spec[객체 이름].append(객체 ID)

            비고: 객체 이름 외에도 "Solid", "Particle" 등의 구별자 사용.
'''
instance_list_spec = {}                         # 객체 종류 별 목록
instance_draw_list = []                         # 개체 그리기 목록
instance_update = false                         # 개체 반복기 갱신 여부
#event_queue = []                               # 이벤트 목록

# Global : Functions
def sqr(v):
    return v * v

def sign(x):
    ret = 0
    if x > 0:
        ret = 1
    elif x < 0:
        ret = - 1
    return ret

def degtorad(degree):
    return degree * math.pi / 180

def radtodeg(radian):
    return radian * 180 / math.pi

def point_distance(x1, y1, x2, y2):
    return math.hypot((x2 - x1), (y2 - y1))

def irandom(n):
    return random.randint(0, int(n))

def irandom_range(n1, n2):
    return random.randint(int(n1), int(n2))

# Object : Game
class game:
    width = scr_defw
    height = scr_defh
    dgan = 0.05

    def __init__(self, nw = int(scr_defw), nh = int(scr_defh)):
        self.width = nw
        self.height = nh

    def __del__(self):
        close_canvas()

    def begin(self):
        open_canvas(self.width, self.height, true)
        show_cursor()

        self.__draw_update__ = false

    # Proceed instance
    def instance_draw_update(self):
        global instance_draw_list
        if self.__draw_update__:
            del instance_draw_list
            self.__draw_update__ = false
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
class sprite:
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
            self.__data__.rotate_draw(rot, x, y, int(self.width * xscale), int(self.height * yscale))
        else:
            self.__data__.clip_draw(int(index * self.width), 0, self.width, self.height, x, y, int(self.width * xscale), int(self.height * yscale))

def place_free(dx, dy):
    clist = instance_list_spec["Solid"]; # 고체 개체 목록 불러오기

# Object : Gravitons
class graviton(object):
    name = "None"
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
        if (self.sprite_index != None and type(self.sprite_index) == sprite):
            draw_sprite(self.sprite_index, self.image_index, self.x, self.y)

    def event_step(self): # The basic machanism of objects.
        if self.xVel != 0:
            xc = self.x + self.xVel + sign(self.xVel)
            if place_free(xc, self.y):
                self.x += self.xVel
            else:
                self.collide()

        if self.yVel < 0:
            yc = self.y - self.yVel - 1
        else:
            yc = self.y - self.yVel + 1

        if place_free(self.x, yc):
            self.y -= self.yVel                     # let it moves first.
            self.gravity = self.gravity_default
            self.yVel += self.gravity
            self.onAir = true
        else:
            self.gravity = 0
            if self.xVel != 0:                      # horizontal friction works only when it is on the ground
                self.xVel *= self.xFric
            self.thud()

    def event_draw(self): # This will be working for drawing.
        self.draw_self()

# Object : Solid Objects
class solid(graviton):
    # reset some inherited variables
    name = "Solid"
    gravity_default = 0
    xFric, yFric = 0, 0

# Object : Functions
def sprite_load(filepath, name = str("default"), number = int(1)):
    new = sprite(filepath, number)
    sprite_list[name] = new
    return new

def draw_sprite(spr, index, x = int(0), y = int(0), xscale = float(1), yscale = float(1), rot = float(0.0)):
    spr.draw(index, x, y, xscale, yscale, rot)

def instance_create(Ty, depth = int(0), x = int(0), y = int(0)):
    global instance_update, instance_last

    temp = Ty(depth, x, y)
    if instance_last != None and isinstance(instance_last, graviton):
        instance_last.next = temp

    instance_last = temp
    instance_list.append(instance_last)
    instance_update = true

    return instance_last

# Main : Game Settings
Game = game()
Game.begin()

# Definitions of Special Objects ( Need a canvas )
sMineBrick = sprite_load("~\res\img\brick_mine_0", "sMineBrick")
class oMineBrick(solid):
    name = "Brick of Mine"
    sprite_index = sMineBrick

testo = instance_create(oMineBrick, 0, 300, 200)

Game.process()

del Game
