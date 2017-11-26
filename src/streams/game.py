from module.pico2d import *
from module.constants import *

from module import framework
from module.framework import Camera
from module.framework import io
import game_pause

import json

from module.sprite import *
#import module.terrain as terrain
from module.terrain import *
from module.game.game_containers import *

__all__ = [
    "name", "GameExecutor", "draw_clean", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "game_state"
background_sprite = "bgNight"
manager = None


def enter():
    global manager
    if manager is None:
        manager = StageIntro()
    delay(0.5)


def exit():
    global manager
    if manager is not None:
        manager.clear()
        del manager
        manager = None


def update(frame_time):
    if len(instance_list) > 0:
        for inst in instance_list:
            inst.event_step(frame_time)


def draw_clean():
    back = sprite_get(background_sprite)
    if background_sprite in ("bgCave",):
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

    if manager is None:
        return

    global instance_draw_list
    if len(instance_draw_list) > 0:
        for inst in instance_draw_list:
            if inst.visible:
                inst.event_draw()
    else:
        raise RuntimeError("개체가 존재하지 않습니다!")

    draw_set_alpha(1)
    heart = sprite_get("sHeart")
    draw_sprite(heart, 0, screen_width - 94, screen_height - 48)
    framework.draw_text(str(player_get_lives()), screen_width - 50, screen_height - 4, scale = 2)
    framework.draw_text("Time: %0.3f" % get_time(), 20, screen_height - 20)


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
    def __init__(self):
        framework.scene_set_size(screen_width * 3)
        Camera.set_pos(0, 0)
        io.key_add(SDLK_LEFT)
        io.key_add(SDLK_RIGHT)
        io.key_add(ord('x'))
        io.key_add(ord('9'))
        io.key_add(ord('8'))

        terrain_tile_assign(1, oBrickCastle, 0)
        terrain_tile_assign(2, oBrickDirt, 0)
        terrain_tile_assign(3, oLush, 0)
        terrain_tile_assign("1", oBrickCastle, 0)
        terrain_tile_assign("2", oLush, 0)
        terrain_tile_assign("@", oPlayer, 2)
        terrain_tile_assign(24, oPlayer, 2)

    def clear(self):
        global instance_list, instance_list_spec, instance_draw_list
        player_lives_clear(3)
        #for inst in instance_list:
        #    inst.destroy()
        #    del inst
        #instance_list.clear()
        #instance_draw_list.clear()

    def update_begin(self):
        global instance_list, instance_draw_list
        instance_draw_list = sorted(instance_list, key = lambda gobject: -gobject.depth)


class StageIntro(GameExecutor):
    def __init__(self):
        super().__init__()

        # Terrains
        terrain_tile_assign("w", oMillHousechip, 3)
        terrain_tile_assign("l", oMillHousechipL, 3)
        terrain_tile_assign("r", oMillHousechipR, 3)
        terrain_tile_assign("m", oMillHousechipM, 3)
        terrain_tile_assign("S", oMillHousestone, 3)
        terrain_tile_assign("e", oSoldier, 2)
        terrain_tile_assign("C", oCobra, 2)
        terrain_tile_assign("z", oSnake, 2)
        terrain_tile_assign("T", oTorch, 1)

        first_scene = TerrainGenerator("begin")

        #first_scene.allocate(";;;;;;" \
        #                     "0000 0000 00mm mmmm mm00 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000\n"
        #                     "0000 0000 lwSS SSSS SSwr 0000 0000 0000 0000 0000 0000 0000 0000 0000 1111 0000 0000 0000 0000 0000 0000 0000 0000\n"
        #                     "0100 0000 lwSS SSSS SSwr 0000 0000 0000 0000 0000 0000 0000 0000 0000 1111 0000 0000 0000 0000 0000 0000 0000 0000\n"
        #                     "1100 0000 lwSS SSSS SSwr 0000 0000 0000 0000 0000 0000 0000 0000 1100 1111 0011 0000 0000 0000 0000 0000 0000 0000\n"
        #                     "1100 0000 lwSS SSSS SSwr 0000 0000 0000 0000 0000 0000 0000 0000 1110 1111 0111 0000 0000 0000 0000 0000 0000 0000\n"
        #                     "1100 0T00 lwSS S@SS SSwr 0000 0000 0000 0T0e 0T00 0000 0000 0000 0ee0 0000 000C 0000 0000 00z0 0e0z 0000 00C0 0zz0 0000\n"
        #                     "1112 2222 2122 2212 1112 2222 2212 2222 2212 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222\n"
        #                     "2122 2212 2222 2222 2222 2122 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222\n"
        #                     "2222 1211 2212 2222 2222 2222 2222 2211 2222 2211 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222 2222\n"
        #                     "0000 2022 0020 0000 0000 0000 0000 0022 0000 0022 0000 0000 0000")
        first_scene.generate()
        self.update_begin()
