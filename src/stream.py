
import os
from pico2d import *

# Global : Constants
false = False
true = True

# Global : Variables
running = true

sprite_list = {}                                # 스프라이트는 이름으로 구분된다.
instance_list = []                              # 개체는 순서가 있다.
instance_iterator = (i for i in instance_list)  # 객체의 반복기를 저장한다.

# Global : Functions
def instance_iter_update(list = instance_list): # Update a iterator of instance list.
    global instance_iterator
    instance_iterator = (i for i in list)

# Object : Gravitons
class graviton:
    name = "None"

    depth = 0
    x, y = 0, 0

    gravity_current = 0
    gravity = 0

    sprite = None

    def __init__(self, ndepth = 0, nx = 0, ny = 0):
        self.depth = ndepth
        self.x, self.y = nx, ny

    def __str__(self):
        return self.name

    def event_step(self):
        pass

    def event_draw(self):
        pass

# Main : Canvas Settings
open_canvas()
show_cursor()

# Event : Global
def event_global():
    global events, running

    for event in events:
        if (event.type == SDL_QUIT):
            running = False
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False

    return running


# Main : Load Sprites
#grass = load_image('grass.png')
#character = load_image('run_animation.png')

while running:
    clear_canvas()

    events = get_events()
    if not event_global():
        break

    if instance_list.__sizeof__() > 0:
        instance_iter_update()
        for inst in instance_iterator:
            if inst.sprite != None:
                inst.sprite.event_step()

        for inst in instance_iterator:
            inst.event_draw()
        update_canvas()

    #grass.draw(400, 30)
    #character.clip_draw(frame * 100, 0, 100, 100, x, 90)

    delay(0.05)


close_canvas()
