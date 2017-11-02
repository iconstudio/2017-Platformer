from pico2d import *
from functions import *
from constants import *

import framework
import streams.game_pause as game_pause

from sprite import *
from terrain import *
from streams.game_containers import *

__all__ = [
    "name", "GameExecutor"
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


def update():
    if len(instance_list) > 0:
        for inst in instance_list:
            inst.event_step()
    else:
        raise RuntimeError("No instance")
    delay(0.01)


def draw_clean():
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


def instance_draw_update():
    global instance_list, instance_draw_list, instance_update
    if instance_update:
        del instance_draw_list
        instance_update = false
        instance_draw_list = []
        instance_draw_list = sorted(instance_list, key=lambda gobject: gobject.depth)
        # for inst in instance_list:
        #    instance_draw_list.append(inst)


def handle_events():
    event_queue = get_events()
    for event in event_queue:
        if event.type == SDL_QUIT:
            framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            framework.push_state(game_pause)
        elif event.type in (SDL_KEYDOWN, SDL_KEYUP):
            io.procede(event)


def pause():
    pass


def resume():
    pass


class GameExecutor:
    def __init__(self):
        # TODO: Definite more objects.
        # Declaring of Special Objects ( Need a canvas )
        sprite_load(
            [path_theme + "brick_castle_0.png", path_theme + "brick_castle_1.png", path_theme + "brick_castle_2.png",
             path_theme + "brick_castle_3.png"], "sCastleBrick", 0, 0)
        sprite_load(path_entity + "vampire.png", "Player", 0, 0)

        tcontainer.signin("1", oBrick)
        tcontainer.signin("@", oPlayer)

        Camera.set_pos(0, 0)
        first_scene = TerrainManager(1, 1)
        first_scene.allocate("1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     ;;;;@;;; \
                                     0000 0000 0000 0000 0000 0000 0000 0000\
                                     1111 1111 1111 1111 1111 1111 1111 1111\
                                     ", 0)

        first_scene.generate()
        global instance_update
        instance_update = true
        instance_draw_update()
