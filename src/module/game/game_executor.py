from module.pico2d import *
from module.functions import *
from module.constants import *

from module import framework
from module.framework import Camera
from module.framework import io
import game_pause

from module.sprite import *
import module.terrain as terrain
from module.game.game_doodad import *
from module.game.game_solid import *

from module.game.gobject_header import *
from module.game.game_containers import *

__all__ = [
    "StageIntro", "manager_create", "manager_get_id", "manager_update", "manager_draw", "manager_handle_events"
]

manager = None


class GameExecutor:
    def __init__(self):
        self.background_sprite = "bgCave"
        Camera.set_pos(0, 0)

        io.key_add(SDLK_LEFT)
        io.key_add(SDLK_UP)
        io.key_add(SDLK_RIGHT)
        io.key_add(SDLK_DOWN)
        io.key_add(ord('z'))
        io.key_add(ord('x'))
        io.key_add(ord('c'))
        io.key_add(ord('9'))
        io.key_add(ord('8'))

        # 아래의 타일들은 모든 스테이지에서 적용됨
        terrain.terrain_tile_assign(1, oBrickCastle, terrain.TYPE_TERRAIN)
        terrain.terrain_tile_assign(2, oBrickDirt, terrain.TYPE_TERRAIN)
        terrain.terrain_tile_assign(3, oLush, terrain.TYPE_TERRAIN)
        terrain.terrain_tile_assign(5, oLadder, terrain.TYPE_TERRAIN)
        terrain.terrain_tile_assign(26, oTorch, terrain.TYPE_DOODAD)

        terrain.terrain_tile_assign(25, oPlayer, terrain.TYPE_INSTANCE)
        terrain.terrain_tile_assign(14, oSoldier, terrain.TYPE_INSTANCE)
        terrain.terrain_tile_assign(13, oCobra, terrain.TYPE_INSTANCE)
        terrain.terrain_tile_assign(12, oSnake, terrain.TYPE_INSTANCE)

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

    def update(self, frame_time):
        if len(get_instance_list(ID_OVERALL)) > 0:
            for inst in get_instance_list(ID_OVERALL):
                inst.event_step(frame_time)

    def draw(self, frame_time):
        global manager
        back = sprite_get(self.background_sprite)
        if self.background_sprite in ("bgCave",):
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
        elif self.background_sprite in ("bgNight",):
            draw_sprite(back, 0, 0, 0)

        if len(get_instance_list(ID_DRAW)) > 0:
            for inst in get_instance_list(ID_DRAW):
                if inst.visible:
                    inst.event_draw()

        draw_set_alpha(1)
        heart = sprite_get("sHeart")
        draw_sprite(heart, 0, screen_width - 94, screen_height - 48)
        draw_set_halign(1)
        draw_set_valign(1)
        framework.draw_text(str(player_get_lives()), screen_width - 50, screen_height - 38, scale = 2)
        draw_set_halign(0)
        draw_set_valign(0)
        framework.draw_text("Time: %0.3f" % get_time(), 10, screen_height - 10)

    def handle_events(self, frame_time):
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


class StageIntro(GameExecutor):
    def __init__(self):
        super().__init__()

        self.background_sprite = "bgNight"

        # Terrains
        terrain.terrain_tile_assign(4, oMillHousestone, terrain.TYPE_BG)
        terrain.terrain_tile_assign(19, oMillHousechip, terrain.TYPE_BG)
        terrain.terrain_tile_assign(20, oMillHousechipL, terrain.TYPE_BG)
        terrain.terrain_tile_assign(21, oMillHousechipR, terrain.TYPE_BG)
        terrain.terrain_tile_assign(22, oMillHousechipM, terrain.TYPE_BG)

        scene = terrain.TerrainGenerator("begin")
        scene.generate()
        self.update_begin()


def manager_get_id() -> GameExecutor:
    global manager
    return manager


def manager_create(stage_number: int) -> GameExecutor:
    """
    :param stage_number: 스테이지 번호. 0 ~
    :return:
    """
    global manager
    if manager is None:
        if stage_number == 0: # 첫번째
            manager = StageIntro()
    return manager


def manager_update(frame_time):
    global manager
    if manager is not None:
        manager.update(frame_time)


def manager_draw(frame_time):
    global manager
    if manager is not None:
        manager.draw(frame_time)


def manager_handle_events(frame_time):
    global manager
    if manager is not None:
        manager.handle_events(frame_time)
