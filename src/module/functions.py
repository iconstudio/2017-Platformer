from pico2d import *
import math
import random
import ctypes
import collections

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

def degtorad(degree):
    return degree * math.pi / 180

def radtodeg(radian):
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
def distribute(x1, x2, ratio):
    if irandom(100) <= ratio * 100:
        return x1
    else:
        return x2
