import sdl2.rect as rect
import sdl2.pixels as px
import sdl2.keycode as keycode
from sdl2.rect import SDL_Rect
import math
from random import *
import module.constants as constants

__all__ = [
    "sqr", "sign", "degtorad", "radtodeg", "point_distance", "point_in_rectangle", "rect_in_rectangle",
    "rect_in_rectangle_opt",
    "irandom", "irandom_range", "distribute", "choose",
    "make_color_rgb",
    "Camera", "oStatusContainer"
]


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


def degtorad(degree: float) -> float:
    return degree * math.pi / 180


def radtodeg(radian: float) -> float:
    return radian * 180 / math.pi


# vector
def point_distance(x1, y1, x2, y2) -> float:
    return math.hypot((x2 - x1), (y2 - y1))


def point_in_rectangle(px, py, x1, y1, x2, y2) -> bool:
    return x1 <= px <= x2 and y1 <= py <= y2


def rect_in_rectangle_opt(pstr: SDL_Rect, dstr: SDL_Rect) -> bool:
    first = pstr
    #first.x -= 1; first.y -= 1; first.w += 1; first.h += 1
    second = dstr
    result = bool(rect.SDL_HasIntersection(first, second))
    return result


def rect_in_rectangle(px1, py1, pw, ph, x1, y1, w, h) -> bool:
    first = rect.SDL_Rect(px1, py1 , pw, ph)
    second = rect.SDL_Rect(x1, y1, w, h)
    result = bool(rect.SDL_HasIntersection(first, second))
    return result


# Randoms
# integer random
def irandom(n) -> int:
    return randint(0, int(n))


# integer random in range
def irandom_range(n1, n2) -> int:
    return randint(int(n1), int(n2))


# get percentage of ratio to x1, else then x2
def distribute(x1, x2, ratio: float):
    if irandom(100) <= ratio * 100:
        return x1
    else:
        return x2


# choice random
def choose(*args):
    length = len(args)
    if length <= 0:
        raise RuntimeError("choose 함수에 값이 제대로 전달되지 않았습니다!" + __name__)

    pick = None
    try:
        pick = args[irandom(length - 1)]
    except ValueError:
        pass
    return pick


# For Drawing
def make_color_rgb(r, g, b):
    return px.SDL_Color(r, g, b)


# Object : View Camera
class oCamera:
    x: float = 0
    y: float = 0
    width, height = constants.screen_width, constants.screen_height

    def set_pos(self, x: float = None, y: float = None):
        if not x.__eq__(None):
            self.x = x
        if not y.__eq__(None):
            self.y = y

    def add_pos(self, x: float = None, y: float = None):
        if not x.__eq__(None):
            self.x += x
        if not y.__eq__(None):
            self.y += y


Camera = oCamera()


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

