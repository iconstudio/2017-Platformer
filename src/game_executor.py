from pico2d import *
from functions import *
from constants import *

import framework
from framework import io
import game_pause
import game_complete
import game_clear_all

from camera import *
from sprite import *
from audio import *
import terrain as terrain
from game_doodad import *
from game_solid import *

from gobject_header import *
from game_containers import *
from game_variables import *
from game_item import *

__all__ = [
    "stage_init", "stage_complete", "stage_get_number",
    "stage_create", "game_update", "game_draw", "stage_clear",
    "game_handle_events"
]


class ui_PopupStage(GObject):
    sprite_index = sprite_get("sPopupStage")
    life = 3
    dmode = 0
    caption = "Stage"
    identify = ID_UI
    depth = -100000
    alpha = 1

    def event_step(self, frame_time):
        if self.alpha <= 0.01:
            self.destroy()
            return

        if self.life > 0:
            if self.life >= 1:
                self.x += (110 - self.x) / 20
            else:
                self.x += (-200 - self.x) / 10

            self.life -= frame_time
        if self.x <= -100:
            self.alpha -= self.alpha / 8

    def event_draw(self):
        draw_sprite(self.sprite_index, alpha = self.alpha)
        draw_set_alpha(self.alpha)
        draw_set_color(255, 255, 255)
        draw_set_halign(0)
        draw_set_valign(1)
        framework.draw_text(self.caption, self.x - 100, screen_height - 32, 1)


class GameExecutor:
    terrain_generator = None
    title = ""
    where: str = ""
    popup = None
    background_sprite = None

    def __init__(self):
        Camera.set_pos(0, 0)
        timer_clear()

    def clear(self):
        for inst in get_instance_list(ID_OVERALL):
            inst.x = -10000
        instance_clear_all()
        for inst in get_instance_list(ID_OVERALL):
            print(inst)
            del inst

    def update_begin(self):
        draw_list_sort()

        self.popup = ui_PopupStage(-10000)
        self.popup.caption = self.title

    def update(self, frame_time):
        timer_increase(frame_time)
        if len(get_instance_list(ID_OVERALL)) > 0:
            for inst in get_instance_list(ID_OVERALL):
                inst.event_step(frame_time)
        Camera.event_step()

    def draw(self, frame_time):
        draw_set_alpha(1)
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
                inst.event_draw()

        if not self.popup.visible:
            draw_set_alpha(1)
            varp = player_instance_get()
            if varp != None and varp.door_popup != None:
                draw_sprite(sprite_get("sPopupHotkeyC"), 0, varp.door_popup.x + 10, varp.door_popup.y + 27)

            tdx, tdy = 10, get_screen_height() - 40
            if player_ability_get_status(PLAYER_AB_DOUBLEJUMP):
                draw_sprite(sprite_get("sIconCape"), 0, tdx, tdy, 2, 2, alpha = 0.6)
                tdx += 36

            if player_ability_get_status(PLAYER_AB_SPIKESHOES):
                draw_sprite(sprite_get("sIconSpike"), 0, tdx, tdy, 2, 2, alpha = 0.6)
                tdx += 36

            if player_ability_get_status(PLAYER_AB_SPRINSHOES):
                draw_sprite(sprite_get("sIconSpring"), 0, tdx, tdy, 2, 2, alpha = 0.6)
                tdx += 36

            heart = sprite_get("sHeart")
            draw_sprite(heart, 0, screen_width - 94, screen_height - 48)
            draw_set_halign(0)
            draw_set_valign(1)
            framework.draw_text(str(player_get_lives()), screen_width - 50, screen_height - 38, scale = 2)

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

    def generate(self):
        self.terrain_generator = terrain.TerrainGenerator(self.where)
        self.terrain_generator.generate()
        self.update_begin()

        tgen = self.terrain_generator
        Camera.set_scene_size(tgen.tile_w * tgen.map_grid_w, tgen.tile_h * tgen.map_grid_h)


class StageIntro(GameExecutor):
    def __init__(self):
        super().__init__()

        self.title = "Stage 1 - Game Begins!"
        self.background_sprite = "bgNight"
        self.where = "stage00"

        # Terrains
        terrain.terrain_tile_assign(4, oMillHousestone, terrain.TYPE_BG)
        terrain.terrain_tile_assign(19, oMillHousechip, terrain.TYPE_BG)
        terrain.terrain_tile_assign(20, oMillHousechipL, terrain.TYPE_BG)
        terrain.terrain_tile_assign(21, oMillHousechipR, terrain.TYPE_BG)
        terrain.terrain_tile_assign(22, oMillHousechipM, terrain.TYPE_BG)

        audio_stream_play("musGame" + str(irandom_range(1, 3)))


class Stage01(GameExecutor):
    def __init__(self):
        super().__init__()

        self.title = "Stage 2 - Pit"
        self.background_sprite = "bgCave"
        self.where = "stage01"

        audio_stream_play("musGame" + str(irandom_range(1, 3)))


class Stage02(GameExecutor):
    def __init__(self):
        super().__init__()

        self.title = "Stage 3 - Cave"
        self.background_sprite = "bgCave"
        self.where = "stage02"

        audio_stream_play("musGame" + str(irandom_range(1, 3)))


class Stage03(GameExecutor):
    def __init__(self):
        super().__init__()

        self.title = "Stage 4 - Bottom Up"
        self.background_sprite = "bgCave"
        self.where = "stage03"

        audio_stream_play("musGame" + str(irandom_range(4, 5)))


class Stage04(GameExecutor):
    def __init__(self):
        super().__init__()

        self.title = "Stage 5 - The End"
        self.background_sprite = "bgCave"
        self.where = "stage04"

        audio_stream_play("musBoss")


def stage_init():
    # 아래의 타일들은 모든 스테이지에서 적용됨

    # Block
    terrain.terrain_tile_assign(1, oBrickCastle, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(50, oBrickCastleTop, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(52, oBrickCastleSewer, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(2, oBrickDirt, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(3, oLush, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(23, oDirtBrickFlat, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(24, oLushFlat, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(37, oBlock, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(9, oBlockMetal, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(6, oBlockBlack, terrain.TYPE_TERRAIN)

    # Tree
    terrain.terrain_tile_assign(28, oTreeTrunk, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(29, oTreeTop, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(30, oTreeTopDead, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(31, oTreeBranch, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(32, oTreeBranchDead, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(46, oTreeBranchLeft, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(47, oTreeBranchDeadLeft, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(33, oTreeLeavesEnd, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(34, oTreeLeavesDeadEnd, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(36, oTreeLeaves, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(48, oTreeLeavesEndLeft, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(49, oTreeLeavesDeadEndLeft, terrain.TYPE_TERRAIN)

    # Doodad & Traps
    terrain.terrain_tile_assign(5, oLadder, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(26, oTorch, terrain.TYPE_DOODAD)
    terrain.terrain_tile_assign(10, oGravestone, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(27, oGravestoneAsh, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(11, oDoor, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(7, oDoorMetalic, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(38, oLamp, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(39, oWeb, terrain.TYPE_TERRAIN)
    terrain.terrain_tile_assign(40, oThorns, terrain.TYPE_TERRAIN)

    # Entity
    terrain.terrain_tile_assign(25, oPlayer, terrain.TYPE_INSTANCE)
    terrain.terrain_tile_assign(14, oSoldier, terrain.TYPE_INSTANCE)
    terrain.terrain_tile_assign(15, oManBeard, terrain.TYPE_INSTANCE)
    terrain.terrain_tile_assign(13, oCobra, terrain.TYPE_INSTANCE)
    terrain.terrain_tile_assign(12, oSnake, terrain.TYPE_INSTANCE)
    terrain.terrain_tile_assign(41, oSpider, terrain.TYPE_INSTANCE)
    terrain.terrain_tile_assign(16, oToad, terrain.TYPE_INSTANCE)

    # Item
    terrain.terrain_tile_assign(18, oRock, terrain.TYPE_INSTANCE)
    terrain.terrain_tile_assign(43, oCape, terrain.TYPE_INSTANCE)
    terrain.terrain_tile_assign(44, oSpikeShoes, terrain.TYPE_INSTANCE)
    terrain.terrain_tile_assign(45, oSpringShoes, terrain.TYPE_INSTANCE)
    terrain.terrain_tile_assign(42, oAnkh, terrain.TYPE_INSTANCE)

    global stagelist, manager, time_local, time_total
    stagelist = []
    stagelist.append(StageIntro)
    stagelist.append(Stage01)
    stagelist.append(Stage02)
    stagelist.append(Stage03)
    stagelist.append(Stage04)
    stagelist.reverse()

    manager = None


def stage_create():
    global stagelist
    if len(stagelist) > 0:
        stg_type = stagelist[-1]
        stagelist.pop()
        global manager
        if manager is None:
            manager = stg_type()
        manager.generate()
        return manager
    else:  # Game complete!
        pass


def stage_complete():
    stage_clear()

    audio_stream_stop()
    global stagelist
    if len(stagelist) > 0:
        framework.push_state(game_complete)
    else:
        framework.change_state(game_clear_all)


def stage_clear():
    global manager
    manager.clear()
    del manager
    manager = None


def stage_get_number() -> int:
    global stage_number
    return stage_number


def game_update(frame_time):
    global manager
    if manager is not None:
        manager.update(frame_time)


def game_draw(frame_time):
    global manager
    if manager is not None:
        manager.draw(frame_time)


def game_handle_events(frame_time):
    global manager
    if manager is not None:
        manager.handle_events(frame_time)
