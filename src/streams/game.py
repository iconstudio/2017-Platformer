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
background_sprite = "bgNight"

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
    back = sprite_get(background_sprite)
    if background_sprite in ("bgCave", ):
        dx = -32
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
    elif background_sprite in ("bgNight",):
        draw_sprite(back, 0, 0, 0)
    
    global instance_draw_list
    if len(instance_draw_list) > 0:
        for inst in instance_draw_list:
            if inst.visible:
                inst.event_draw()
    else:
        raise RuntimeError("개체가 존재하지 않습니다!")

    global player_lives
    heart = sprite_get("sHeart")
    dx, dy = screen_width - 56, screen_height - 48
    for i in range(player_lives):
        draw_sprite(heart, 0, dx, dy)
        dx -= 40


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
        global instance_list, instance_draw_list
        instance_draw_list = sorted(instance_list, key = lambda gobject: -gobject.depth)
    
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
        tcontainer.signin("z", oSnake)
        tcontainer.signin("T", oTorch)
        
        
        first_scene = TerrainManager(0)
        first_scene.allocate(";;;;;;;;"
                             "0000 0000 00mm mmmm mm00 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000\n"
                             "0000 0000 lwSS SSSS SSwr 0000 0000 0000 0000 0000 0000 0000 0000 0000 1111 0000 0000 0000 0000 0000 0000 0000 0000\n"
                             "0100 0000 lwSS SSSS SSwr 0000 0000 0000 0000 0000 0000 0000 0000 0000 1111 0000 0000 0000 0000 0000 0000 0000 0000\n"
                             "1100 0000 lwSS SSSS SSwr 0000 0000 0000 0000 0000 0000 0000 0000 1100 1111 0011 0000 0000 0000 0000 0000 0000 0000\n"
                             "1100 0000 lwSS SSSS SSwr 0000 0000 0000 0000 0000 0000 0000 0000 1110 1111 0111 0000 0000 0000 0000 0000 0000 0000\n"
                             "1100 0T00 lwSS S@SS SSwr 0000 0000 0000 0T0e 0T00 0000 0000 0000 0ee0 0000 000C 0000 0000 00z0 0e0z 0000 00C0 0zz0 0000\n"
                             "1112 2222 2122 2212 1112 2222 2212 2222 2212 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222\n"
                             "2122 2212 2222 2222 2222 2122 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222\n"
                             "2222 1211 2212 2222 2222 2222 2222 2211 2222 2211 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222\n"
                             "0000 2022 0020 0000 0000 0000 0000 0022 0000 0022 0000 0000 0000")
        
        first_scene.generate()
        self.update_begin()
