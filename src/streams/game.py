from module.pico2d import *
from module.constants import *

from module import framework
from module.framework import Camera
from module.framework import io
import game_pause

from module.sprite import *
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
        # manager.clear()
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
        for _ in range(22):
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

    if len(get_instance_list(ID_DRAW)) > 0:
        for inst in get_instance_list(ID_DRAW):
            if inst.visible:
                inst.event_draw()
    else:
        raise RuntimeError("개체가 존재하지 않습니다!")

    if manager is None:  # Drawing UI
        return

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
        Camera.set_pos(0, 0)

        io.key_add(SDLK_LEFT)
        io.key_add(SDLK_UP)
        io.key_add(SDLK_RIGHT)
        io.key_add(SDLK_DOWN)
        io.key_add(ord('x'))
        io.key_add(ord('9'))
        io.key_add(ord('8'))

        # 아래의 타일들은 모든 스테이지에서 적용됨
        terrain_tile_assign(1, oBrickCastle, TYPE_TERRAIN)
        terrain_tile_assign(2, oBrickDirt, TYPE_TERRAIN)
        terrain_tile_assign(3, oLush, TYPE_TERRAIN)
        terrain_tile_assign(5, oLadder, TYPE_TERRAIN)
        terrain_tile_assign(26, oTorch, TYPE_DOODAD)

        terrain_tile_assign(25, oPlayer, TYPE_INSTANCE)
        terrain_tile_assign(14, oSoldier, TYPE_INSTANCE)
        terrain_tile_assign(13, oCobra, TYPE_INSTANCE)
        terrain_tile_assign(12, oSnake, TYPE_INSTANCE)

    def clear(self):
        player_lives_clear()
        # alllist, drawlist = get_instance_list(ID_OVERALL), get_instance_list(ID_DRAW)
        # for inst in alllist:
        #    inst.destroy()
        #    del inst
        # alllist.clear()
        # drawlist.clear()

    def update_begin(self):
        draw_list_sort()


class StageIntro(GameExecutor):
    def __init__(self):
        super().__init__()

        # Terrains
        terrain_tile_assign(4, oMillHousestone, TYPE_BG)
        terrain_tile_assign(19, oMillHousechip, TYPE_BG)
        terrain_tile_assign(20, oMillHousechipL, TYPE_BG)
        terrain_tile_assign(21, oMillHousechipR, TYPE_BG)
        terrain_tile_assign(22, oMillHousechipM, TYPE_BG)

        scene = TerrainGenerator("begin")
        scene.generate()
        self.update_begin()
