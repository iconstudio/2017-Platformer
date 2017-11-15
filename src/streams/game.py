from module.pico2d import *
from module.functions import *
from module.constants import *

from module import framework
from module.framework import io
from module.framework import Camera
from streams import game_pause
from streams.game_containers import *

from module.sprite import *
from module.terrain import *
from module.gobject_header import *

__all__ = [
    "name", "GameExecutor", "draw_clean", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "game_state"


def enter():
    GameExecutor()
    delay(1)


def exit():
    pass


def update(frame_time):
    if len(instance_list) > 0:
        for inst in instance_list:
            inst.event_step(frame_time)


def draw_clean():
    dx = -32
    back = sprite_get("bgCave")
    for x in range(22):
        dy = -32
        for y in range(13):
            draw_sprite(back, 0, dx, dy)
            dy += 32
        dx += 32
        if dx > screen_width:
            dx -= screen_width
        elif dx < 0:
            dx += screen_width

    instance_draw_update()
    global instance_draw_list
    if len(instance_draw_list) > 0:
        for inst in instance_draw_list:
            inst.event_draw()
    else:
        raise RuntimeError("개체가 존재하지 않습니다!")


def draw():
    clear_canvas()
    draw_clean()
    update_canvas()


def handle_events(frame_time):
    event_queue = get_events()
    for event in event_queue:
        if event.event == SDL_WINDOWEVENT_FOCUS_LOST:
            io.clear()
        elif event.type == SDL_QUIT:
            framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            io.clear()
            framework.pause()
            framework.push_state(game_pause)
        else:
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
        tcontainer.signin("S", oSnake)
        tcontainer.signin("C", oCobra)

        Camera.set_pos(0, 0)
        first_scene = TerrainManager(1, 1)
        first_scene.allocate("1111 1111 1111 1111 1111 1111 1111 1111  \
                              1111 1111 1111 1111 1111 1111 1111 1111  \
                              1111 1111 1111 1111 1111 1111 1111 1111  \
                              1111 1111 1111 1111 1111 1111 1111 1111  \
                              1111 1111 1111 1111 1111 1111 1111 1111  \
                              ;;;; \
                              00C0 00S0 1111 0000 0000 0000 0000 0000  \
                              1111 1111 1111 @000 00ss 0001 0s11 1C11  \
                              ;;  \
                              0000 0000 0000 0000 0000 0000 0000 0000  \
                              1111 1111 1111 1111 1111 1111 1111 1111  \
                              ", 0)

        first_scene.generate()
        instance_draw_update()
