from module.pico2d import *
from module.functions import *
from module.constants import *

from module import framework
from module.framework import io
from module.framework import Camera
from streams import game_pause

from module.sprite import *
from module.terrain import *
from streams.game_containers import *

__all__ = [
    "name", "GameExecutor", "draw_clean", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "game_state"


def enter():
    GameExecutor()


def exit():
    """
    while (true):
        try:
            data_tuple = sprite_list.popitem()
            olddb: Sprite = data_tuple[1]
            del olddb
        except KeyError as e:
            break
        else:
            del olddb
    """


def update(frame_time):
    if len(instance_list) > 0:
        for inst in instance_list:
            inst.event_step(frame_time)
    else:
        raise RuntimeError("No instance")


def draw_clean():
    back = sprite_get("bgCave")
    for x in range(0, screen_width, 32):
        for y in range(0, screen_height, 32):
            draw_sprite(back, 0, x, y)
    
    instance_draw_update()
    if len(instance_draw_list) > 0:
        for inst in instance_draw_list:
            inst.event_draw()
    else:
        raise RuntimeError("No instance")


def draw():
    clear_canvas()
    draw_clean()
    update_canvas()


# noinspection PyGlobalUndefined
def instance_draw_update():
    global instance_list, instance_draw_list, instance_update
    if instance_update:
        del instance_draw_list
        instance_update = false
        instance_draw_list = []
        instance_draw_list = sorted(instance_list, key=lambda gobject: -gobject.depth)
        # for inst in instance_list:
        #    instance_draw_list.append(inst)


def handle_events(frame_time):
    event_queue = get_events()
    for event in event_queue:
        if event.type == SDL_QUIT:
            framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            framework.push_state(game_pause)
        elif event.type == SDL_KEYDOWN or SDL_KEYUP:
            io.proceed(event)


def pause():
    pass


def resume():
    pass


class GameExecutor:
    def __init__(self):
        io.key_add(SDLK_LEFT)
        io.key_add(SDLK_RIGHT)
        io.key_add(SDLK_UP)
        # Terrains
        tcontainer.signin("1", oBrick)
        tcontainer.signin("@", oPlayer)
        tcontainer.signin("s", oSoldier)

        Camera.set_pos(0, 0)
        first_scene = TerrainManager(1, 1)
        first_scene.allocate("1111 1111 1111 1111 1111 1111 1111 1111\
                              1111 1111 1111 1111 1111 1111 1111 1111\
                              1111 1111 1111 1111 1111 1111 1111 1111\
                              1111 1111 1111 1111 1111 1111 1111 1111\
                              1111 1111 1111 1111 1111 1111 1111 1111\
                              ;;;; \
                              0000 0000 1111 0000 0000 0000 0000 0000  \
                              1111 1111 1111 @000 00ss 0001 0s11 1111 \
                              ;;  \
                              0000 0000 0000 0000 0000 0000 0000 0000\
                              1111 1111 1111 1111 1111 1111 1111 1111\
                              ", 0)
        
        first_scene.generate()
        global instance_update
        instance_update = true
        instance_draw_update()
