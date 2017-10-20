from pico2d import *
from random import *
import math
import ctypes
import collections

__all__ = [
    "false", "true", "screen_width", "screen_height", "screen_scale",
    "sqr", "sign", "degtorad", "radtodeg", "point_distance", "point_in_rectangle", "irandom", "irandom_range", "distribute",
    "Camera", "Sprite", "sprite_list",
    "sprite_load", "sprite_get", "draw_sprite"
]

# Global : Constants
false = False
true = True
screen_width:int = 800
screen_height:int = 450
screen_scale:int = 1

# Global : Variables 1
sprite_list:dict = {}                               # 스프라이트는 이름으로 구분된다.

# Global : Functions
# arithmetics
def sqr(v):
    return v * v

def sign(x):
    ret = 0
    if x > 0:
        ret = 1
    elif x < 0:
        ret = - 1
    return ret

def degtorad(degree:float):
    return degree * math.pi / 180

def radtodeg(radian:float):
    return radian * 180 / math.pi

def point_distance(x1, y1, x2, y2):
    return math.hypot((x2 - x1), (y2 - y1))

def point_in_rectangle(px, py, x1, y1, x2, y2):
    return x1 <= px <= x2 and y1 <= py <= y2

# integer random
def irandom(n):
    return random.randint(0, int(n))

# integer random in range
def irandom_range(n1, n2):
    return random.randint(int(n1), int(n2))

# get percentage of ratio to x1, else then x2
def distribute(x1, x2, ratio:float):
    if irandom(100) <= ratio * 100:
        return x1
    else:
        return x2

# Object : View Camera
class __Camera:
    x:float = 0
    y:float = 0
    width, height = screen_width, screen_height

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

Camera = __Camera()

# Object : Sprites
class Sprite(object):
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
            self.__data__.rotate_draw(rot, x, y, int(self.width * xscale),  int(self.height * yscale))
        else:
            self.__data__.clip_draw(int(index * self.width), 0, self.width, self.height, x, y, int(self.width * xscale), int(self.height * yscale))

def sprite_load(filepath:str, name = str("default"), number = int(1)):
    global sprite_list
    new = Sprite(filepath, number)
    sprite_list[name] = new
    return new

def sprite_get(name:str):
    global sprite_list
    return sprite_list[name]

def draw_sprite(spr:Sprite, index, x = int(0), y = int(0), xscale = float(1), yscale = float(1), rot = float(0.0)):
    spr.draw(index, x, y, xscale, yscale, rot)
