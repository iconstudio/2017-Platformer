from module.pico2d import *
from module.constants import *

from module import framework
from module.framework import io
import game_pause

from module.camera import *
from module.sprite import *
from module.audio import *
import module.terrain as terrain
from module.game.game_doodad import *
from module.game.game_solid import *

from module.game.gobject_header import *
from module.game.game_containers import *

__all__ = [
    "stage_init", "stage_add", "stage_complete", "stage_get_number",
    "stage_create", "manager_get_id", "manager_update", "manager_draw", "manager_delete",
    "manager_handle_events"
]

time_local = 0  # a Timer of current stage
time_total = 0
manager = None
stagelist = []
stage_number = 0

# 아래의 타일들은 모든 스테이지에서 적용됨
terrain.terrain_tile_assign(1, oBrickCastle, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(2, oBrickDirt, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(3, oLush, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(23, oDirtBrickFlat, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(24, oLushFlat, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(37, oBlock, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(9, oBlockMetal, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(6, oBlockBlack, terrain.TYPE_TERRAIN)

terrain.terrain_tile_assign(28, oTreeTrunk, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(29, oTreeTop, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(30, oTreeTopDead, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(31, oTreeBranch, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(32, oTreeBranchDead, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(33, oTreeLeavesEnd, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(34, oTreeLeavesDeadEnd, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(36, oTreeLeaves, terrain.TYPE_TERRAIN)

terrain.terrain_tile_assign(5, oLadder, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(26, oTorch, terrain.TYPE_DOODAD)
terrain.terrain_tile_assign(10, oGravestone, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(27, oGravestoneAsh, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(11, oDoor, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(7, oDoorMetalic, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(38, oLamp, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(39, oWeb, terrain.TYPE_TERRAIN)
terrain.terrain_tile_assign(40, oThorns, terrain.TYPE_TERRAIN)

terrain.terrain_tile_assign(25, oPlayer, terrain.TYPE_INSTANCE)
terrain.terrain_tile_assign(14, oSoldier, terrain.TYPE_INSTANCE)
terrain.terrain_tile_assign(13, oCobra, terrain.TYPE_INSTANCE)
terrain.terrain_tile_assign(12, oSnake, terrain.TYPE_INSTANCE)

class GameExecutor:
    terrain_generator = None

    def __init__(self):
        global time_local

        self.background_sprite = "bgCave"
        time_local = 0

    def clear(self):
        global time_local
        time_local = 0
        player_lives_clear()
        alllist, drawlist = get_instance_list(ID_OVERALL), get_instance_list(ID_DRAW)
        for inst in alllist:
            inst.visible = false
            inst.destroy()
        instance_list_clear(ID_OVERALL)
        instance_list_clear(ID_DRAW)

    def update_begin(self):
        draw_list_sort()

    def update(self, frame_time):
        global time_local, time_total
        time_local += frame_time
        time_total += frame_time
        if len(get_instance_list(ID_OVERALL)) > 0:
            for inst in get_instance_list(ID_OVERALL):
                inst.event_step(frame_time)

    def draw(self, frame_time):
        if self.background_sprite is not None:
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
        draw_set_halign(0)
        draw_set_valign(1)
        framework.draw_text(str(player_get_lives()), screen_width - 50, screen_height - 38, scale = 2)
        draw_set_halign(0)
        draw_set_valign(0)
        framework.draw_text("Time: %0.1f / %.0f" % (time_local, time_total), 10, screen_height - 10)

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
                audio_play("sndPauseIn")
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

        scene_set_size(screen_width * 3)
        self.terrain_generator = terrain.TerrainGenerator("begin")
        self.terrain_generator.generate()
        self.update_begin()


class Stage01(GameExecutor):
    def __init__(self):
        super().__init__()

        self.background_sprite = None

        self.terrain_generator = terrain.TerrainGenerator("stage01")
        self.terrain_generator.generate()
        self.update_begin()

        scene_set_size(self.terrain_generator.tile_w * self.terrain_generator.map_grid_w,
                                 screen_height * 2)


def stage_add(arg):
    global stagelist
    stagelist.append(arg)


def stage_complete():
    global manager, stage_number
    stage_number = manager.terrain_generator.get_stage_number()

    import stages.game_complete as game_complete
    framework.push_state(game_complete)


def stage_get_number() -> int:
    global stage_number
    return stage_number


def manager_delete():
    global manager
    manager.clear()
    del manager
    manager = None


def manager_get_id() -> GameExecutor:
    global manager
    return manager


def stage_init():
    Camera.set_pos(0, 0)

    stage_add(StageIntro)
    stage_add(Stage01)
    stagelist.reverse()


def stage_create() -> GameExecutor:
    global stagelist
    stg_type = stagelist.pop()
    global manager
    if manager is None:
        manager = stg_type()
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
