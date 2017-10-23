from pico2d import *
from random import *
import math
import ctypes
import collections

__all__ = [
    "false", "true", "screen_width", "screen_height", "screen_scale",
    "sqr", "sign", "degtorad", "radtodeg", "point_distance", "point_in_rectangle", "irandom", "irandom_range", "distribute",
    "Camera"
]

# Global : Constants
false = False
true = True
screen_width:int = 800
screen_height:int = 450
screen_scale:int = 1

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
    return randint(int(n1), int(n2))

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
