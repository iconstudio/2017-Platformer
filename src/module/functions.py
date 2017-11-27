import math
from random import *

import sdl2.pixels as px
import sdl2.rect as rect
from sdl2.rect import SDL_Rect

import module.constants as constants

__all__ = [
    "sqr", "sign", "degtorad", "radtodeg", "direction", "point_distance", "oParser", "bezier4",
    "point_in_rectangle", "rect_in_rectangle", "rect_in_rectangle_opt", "delta_velocity", "delta_gravity",
    "irandom", "irandom_range", "distribute", "choose", "list_seek",
    "make_color_rgb"
]


# Global : Functions
# arithmetics
def sqr(v) -> float:
    return v * v


def sign(x) -> int:
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


def bezier4(t, x1, x2, x3, x4) -> float:
    factor = 1 - t

    return factor * (factor * (factor * x1 + t * x2)
                     + t * (factor * x2 + t * x3)) + t * (factor * (factor * x2 + t * x3) + t * (factor * x3 + t * x4))


# vector
# distance
def point_distance(x1, y1, x2, y2) -> float:
    return math.hypot((x2 - x1), (y2 - y1))


def point_in_rectangle(px1, py1, x, y, w, h) -> bool:
    return 0 <= px1 - x <= w and 0 <= py1 - y <= h


def rect_in_rectangle_opt(pstr: SDL_Rect, dstr: SDL_Rect) -> bool:
    first = pstr
    second = dstr
    result = bool(rect.SDL_HasIntersection(first, second))
    return result


def rect_in_rectangle(px1, py1, pw, ph, x1, y1, w, h) -> bool:
    if px1 > x1 + w: return False
    if px1 + pw < x1: return False
    if py1 + ph < x1: return False
    if py1 > y1 + h: return False

    return True


# Object : Parser
class oParser:
    value: float = 0.0
    value_min: float = 0.0
    value_max: float = 1.0

    def limitation(self):
        if self.value < self.value_min:
            self.value = self.value_min
        while self.value >= self.value_max:
            self.value -= self.value_max

    def __init__(self, nvalue = 0.0):
        self.value = nvalue

    def __abs__(self) -> float:
        return abs(self.value)

    def __eq__(self, other) -> bool:
        try:
            return bool(self.value == other.value)
        except AttributeError:
            return constants.false

    def __gt__(self, values) -> bool:
        if type(values) is int or float:
            self.value += values
        elif values is None:
            return constants.false
        else:
            try:
                return bool(self.value > values.value)
            except AttributeError:
                return constants.false

    def __lt__(self, values) -> bool:
        if type(values) is int or float:
            self.value += values
        elif values is None:
            return constants.false
        else:
            try:
                return bool(self.value < values.value)
            except AttributeError:
                return constants.false

    def __add__(self, values) -> object:
        if type(values) is int or float:
            self.value += values
        elif values is None:
            pass
        else:
            try:
                self.value += values.value
            except AttributeError:
                pass
        self.limitation()
        return self

    def __sub__(self, values) -> object:
        return self.__add__(-values)

    def __mul__(self, values) -> object:
        if type(values) is int or float:
            self.value *= values
        elif values is None:
            pass
        else:
            try:
                self.value *= values.value
            except AttributeError:
                pass
        self.limitation()
        return self

    def __neg__(self) -> float:
        return -self.value

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__


class direction(oParser):
    value_max = 360.0


# physics
def delta_velocity(spd = 1) -> float:
    return constants.phy_velocity * spd


def delta_gravity() -> float:
    return constants.phy_gravity


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


def list_seek(alist: list, value) -> int:
    index = 0
    lengths = len(alist)
    for i in range(lengths):
        if alist[i] == value:
            index = i
            break
    return index


# For Drawing
def make_color_rgb(r, g, b):
    return px.SDL_Color(r, g, b)
