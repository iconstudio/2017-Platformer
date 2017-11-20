from module.pico2d import *
from module.constants import *

from module import framework
from module.framework import Camera
from module.framework import io
from streams import game_pause
from streams.game_containers import *
from module.gobject_header import *

from module.sprite import *
from module.terrain import *

__all__ = [
    "name", "GameExecutor", "draw_clean", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "game_state"


def enter():
    StageIntro()
    delay(0.5)


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


def draw(frame_time):
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
    def update_begin(self):
        instance_draw_update()
        global instance_list, instance_draw_list
        instance_draw_list = sorted(instance_list, key = lambda gobject: -gobject.depth)
    
    def tassign_more(self):
        tcontainer.signin("s", oSoldier)
        tcontainer.signin("S", oSnake)
        tcontainer.signin("C", oCobra)


class StageIntro(GameExecutor):
    def __init__(self):
        framework.scene_set_size(screen_width * 3)
        Camera.set_pos(0, 0)
        io.key_add(SDLK_LEFT)
        io.key_add(SDLK_RIGHT)
        io.key_add(SDLK_UP)
        
        # Terrains
        tcontainer.signin("1", oBrickCastle)
        tcontainer.signin("2", oLush)
        tcontainer.signin("@", oPlayer)
        tcontainer.signin("w", oMillHousechip)
        tcontainer.signin("l", oMillHousechipL)
        tcontainer.signin("r", oMillHousechipR)
        tcontainer.signin("m", oMillHousechipM)
        tcontainer.signin("S", oMillHousestone)
        tcontainer.signin("e", oSoldier)
        tcontainer.signin("C", oCobra)
        
        first_scene = TerrainManager(0)
        first_scene.allocate(";;;;;;;;"
                             "0000 0000 00mm mmmm mm00 0000 0000 0000 0000 0000 00000 0000 0000 0000\n"
                             "0000 0000 lwSS SSSS SSwr 0000 0000\n"
                             "0000 0000 lwSS SSSS SSwr 0000 0000\n"
                             "0000 0000 lwSS SSSS SSwr 0000 0000\n"
                             "0000 0000 lwSS SSSS SSwr 0000 0000\n"
                             "00@0 0000 lwSS SSSS SSwr 0000 0000 0000 0000 0000 0000 0000 0000 0000\n"
                             "1112 2222 2122 2212 1112 2222 2212 2222 2222 2222 2222 2222 2222 2222 2222\n"
                             "2122 2212 2222 2222 2222 2122 2222 2222\n"
                             "2222 1211 2212 2222 2222 2222 2222 2211\n"
                             "0000 2022 0020 0000 0000 0000 0000 0022")
        
        first_scene.generate()
        self.update_begin()
