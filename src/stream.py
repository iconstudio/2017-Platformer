
from pico2d import *
import math
import random

# Global : Constants
false = False
true = True

# Global : Variables
running = true

sprite_list = {}                                # 스프라이트는 이름으로 구분된다.
instance_list = []                              # 개체는 순서가 있다.
instance_iterator = (i for i in instance_list)  # 객체의 반복기를 저장한다.
#event_queue = []                               # 이벤트 목록

# Global : Functions
def sqr(v):
    return v * v

def degtorad(degree):
    return degree * math.pi / 180

def radtodeg(radian):
    return radian * 180 / math.pi

def point_distance(x1, y1, x2, y2):
    return math.hypot((x2 - x1), (y2 - y1))

def instance_iter_update(list = instance_list): # Update the iterator of a instance list.
    global instance_iterator
    instance_iterator = (i for i in list)

def irandom(n):
    return random.randint(0, int(n))

def irandom_range(n1, n2):
    return random.randint(int(n1), int(n2))

# Object : Game
class game:
    width = 960
    height = 540

    def __init__(self, nw = int(960), nh = int(540)):
        self.width = nw
        self.height = nh

    def __del__(self):
        close_canvas()

    def begin(self):
        open_canvas(self.width, self.height, true)
        show_cursor()

# Object : Sprites
class sprite():
    number = 0

    def __init__(self, filepath, number):
        self.__data__ = load_image(filepath)

        # the number of sprite in a image
        self.number = number
        # size of each index
        try:
            self.width = self.__data__.w / number
            self.height = self.__data__.h / number

            tempTy = type(number)
            if tempTy != int and tempTy != float:
                raise RuntimeError("스프라이트 불러오기 시 인자가 숫자가 아닙니다.")
        except ZeroDivisionError:
            raise RuntimeError("스프라이트의 갯수는 0개가 될 수 없습니다.")

    def draw(self, index, x, y, xscale = int(1), yscale = int(1), rot = float(0.0)):
        if rot != 0.0: # pico2d does not support scaling + rotating draw.
            self.__data__.rotate_draw(rot, x, y, self.width * xscale, self.height * yscale)
        else:
            self.__data__.clip_draw(index * self.width, 0, self.width, self.height, x, y, self.width * xscale, self.height * yscale)

# Object : Gravitons
class graviton(object):
    name = "None"

    sprite_index = None
    image_index = float(0)
    image_speed = float(0)

    visible = true
    depth = 0

    x, y = 0, 0
    gravity_current = 0
    gravity = 0

    def __init__(self, ndepth = int(0), nx = int(0), ny = int(0)):
        self.depth = ndepth
        self.x, self.y = nx, ny

    def __str__(self):
        return self.name

    def draw_self(self):
        if (self.sprite_index != None and type(self.sprite_index) == sprite):
            draw_sprite(self.sprite_index, self.image_index, self.x, self.y)

    def event_step(self):
        pass

    def event_draw(self):
        self.draw_self()

# Object : Functions
def sprite_load(filepath, name = str("default"), number = int(1)):
    new = sprite(filepath, number)
    sprite_list[name] = new
    return new

def draw_sprite(sprite, index, x = int(0), y = int(0), xscale = int(1), yscale = int(1), rot = float(0.0)):
    sprite.draw(index, x, y, xscale, yscale, rot)

def instance_create(Ty, depth = int(0), x = int(0), y = int(0)):
    tempObj = Ty(depth, x, y)
    instance_list.append(tempObj)

    return tempObj

# Main : Game Settings
Game = game()
Game.begin()

test = sprite_load("test.png", "ball", 1)
testo = instance_create(graviton)
testo.sprite_index = test

# Event : Global
def event_global():
    global event_queue, running

    for event in event_queue:
        if (event.type == SDL_QUIT):
            running = False
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False

    return running

while running:
    clear_canvas()

    event_queue = get_events()
    if not event_global():
        break

    if len(instance_list) > 0:
        #print(instance_list.__len__())
        instance_iter_update()
        for inst in instance_iterator:
            inst.event_step()

        for inst in instance_iterator:
            inst.event_draw()
        update_canvas()

    #grass.draw(400, 30)
    #character.clip_draw(frame * 100, 0, 100, 100, x, 90)

    delay(0.03)

del Game
