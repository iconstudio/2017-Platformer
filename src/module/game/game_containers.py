from module.pico2d import *
from module.functions import *
from module.constants import *

from module import framework
from module.framework import Camera
from module.framework import io
from streams import game_over

from game.gobject_header import __all__ as gobject_all
from game.gobject_header import *
from game.game_doodad import __all__ as doodad_all
from game.game_doodad import *
from game.game_solid import __all__ as solid_all
from game.game_solid import *

from module.sprite import *

__all__ = [
              "player_got_damage", "player_lives_clear", "player_get_lives",
              "oPlayer", "oSoldier", "oSnake", "oCobra",
          ] + gobject_all + doodad_all + solid_all

# ==================================================================================================
#                                               게임
# ==================================================================================================


player_lives = 3


def player_got_damage(how: int):
    global player_lives
    player_lives -= how


def player_lives_clear(how: int = 3):
    global player_lives
    player_lives = how


def player_get_lives() -> int:
    global player_lives
    return player_lives


# ==================================================================================================
#                                    사용자 정의 객체 / 함수
# ==================================================================================================
def instance_place(Ty, fx, fy) -> (list, int):
    try:
        ibj = Ty.identify
    except AttributeError:
        raise RuntimeError("Cannot find variable 'identify' in %s" % (str(Ty)))

    __returns = []
    global instance_list, instance_list_spec
    if ibj == "":
        clist = instance_list
    else:
        clist = instance_list_spec[ibj]
    length = len(clist)
    if length > 0:
        for inst in clist:
            if isinstance(inst, Ty) and point_in_rectangle(fx, fy, *inst.get_bbox()):
                __returns.append(inst)

    return __returns, len(__returns)


# Declaring of Special Objects ( Need a canvas )
# Definitions of Special Objects


# Player
class oPlayer(GObject):
    name = "Player"
    depth = 0
    image_speed = 0
    # anitem what to hold on
    held: object = None
    invincible: float = 0
    controllable: float = 0
    wladder = None

    # real-scale: 54 km per hour
    xVelMin, xVelMax = -54, 54

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_index = sprite_get("Player")

        global container_player
        container_player = self

    def get_dmg(self, how: int = 1, dir = 1):
        player_got_damage(how)
        if player_lives <= 0:
            self.oStatus = oStatusContainer.DEAD
            self.xVel = 0

            framework.change_state(game_over)
        else:
            self.invincible = 3
            io.clear()
            self.xVel = -dir * 20
            self.yVel += 15
            self.controllable = 0.5

    def event_step(self, frame_time):
        if (self.oStatus is oStatusContainer.LADDERING):
            self.gravity_default = 0
            self.gravity = 0
        else:
            self.gravity_default = delta_gravity()
        super().event_step(frame_time)

        if player_get_lives() <= 0:
            self.get_dmg()
            return

        if io.key_check_pressed(ord('9')):
            self.get_dmg(3)
            return

        if self.invincible > 0:
            self.invincible -= frame_time
            self.image_alpha = 0.5
        else:
            self.image_alpha = 1
        if self.controllable > 0:
            self.controllable -= frame_time

        # ==================================================================================================
        elist, ecount = instance_place(oEnemyParent, self.x, self.y)
        dlist, dcount = instance_place(oEnemyDamage, self.x, self.y)
        tlist, tcount = elist + dlist, ecount + dcount
        if tcount > 0:
            for enemy in tlist:
                if not enemy.collide_with_player and enemy.oStatus < oStatusContainer.STUNNED:
                    enemy.collide_with_player = true
                    if enemy.name in (
                            "ManEater", "Lavaman",):  # Cannot ignore getting damages from these kind of enemies.
                        self.get_dmg(1, enemy.image_xscale)
                    elif self.invincible <= 0 and self.y <= enemy.y:
                        self.get_dmg(1, enemy.image_xscale)
                    enemy.collide_with_player = true

        # ==================================================================================================
        if self.oStatus < oStatusContainer.CHANNELING:  # Player can control its character.
            Camera.set_pos(self.x - Camera.width / 2, self.y - Camera.height / 2)
            # Stomps enemies under the character
            whothere, howmany = instance_place(oEnemyParent, self.x, self.y - 9)
            if howmany > 0 > self.yVel and self.onAir:
                for enemy in whothere:
                    if enemy.oStatus < oStatusContainer.STUNNED:
                        if enemy.name not in ("ManEater", "Lavaman",):  # Cannot stomping these kind of enemies.
                            self.yVel = 60
                            enemy.hp -= 1
                            enemy.yVel = 30
                            enemy.collide_with_player = false
                            if enemy.hp <= 0:
                                enemy.status_change(oStatusContainer.DEAD)
                            else:
                                enemy.status_change(oStatusContainer.STUNNED)
                                enemy.stunned = 5
                        else:
                            enemy.collide_with_player = true
                            self.get_dmg(1, enemy.image_xscale)
            elif howmany > 0:  # Cannot Stomp but collide with enemy
                for enemy in whothere:
                    enemy.collide_with_player = false
                    if enemy.oStatus < oStatusContainer.STUNNED:
                        if enemy.name in (
                                "ManEater", "Lavaman",):  # Cannot ignore getting damages from these kind of enemies.
                            self.get_dmg(1, enemy.image_xscale)
                        elif self.invincible <= 0:
                            self.get_dmg(1, enemy.image_xscale)
                        enemy.collide_with_player = true

            # ==================================================================================================
            mx, my = 0, 0
            if self.controllable <= 0:  # Player can controllable
                if io.key_check(SDLK_LEFT): mx -= 1
                if io.key_check(SDLK_RIGHT): mx += 1
                if io.key_check(SDLK_UP): my += 1
                if io.key_check(SDLK_DOWN): my -= 1

                if self.oStatus != oStatusContainer.LADDERING:
                    if my != 0:  # Get on a ladder
                        instl, cl = instance_place(oLadder, self.x, self.y)
                        if cl > 0:  # get stick to the ladder
                            if abs(instl[0].x + 10 - self.x) <= 4 and abs(instl[0].y + 10 - self.y) <= 10:
                                self.wladder = instl[0]
                                self.x = self.wladder.x + 10
                                self.y = self.wladder.y + 10
                                self.xVel, self.yVel = 0, 0
                                self.oStatus = oStatusContainer.LADDERING
                                self.sprite_set("Player")
                                return  # change attributes only one time

                    if mx != 0:  # Move horizontal
                        self.xFric = 0
                        if not self.onAir:
                            self.xVel += mx * 5
                        else:
                            self.xVel += mx * 2
                        self.image_xscale = mx
                    else:
                        self.xFric = 0.6

                    if io.key_check_pressed(ord('x')):  # Jump
                        if not self.onAir:
                            self.yVel = 90

                    # ==================================================================================================
                    self.yFric = 0
                    if not self.onAir:  # Play Moving sprite
                        if self.xVel != 0:
                            self.image_speed = 0.8
                            self.sprite_index = sprite_get("PlayerRun")
                        else:  # Play Idle sprite
                            self.sprite_set("Player")
                    else:  # Play Jumping sprite
                        self.sprite_set("PlayerJump")

                else:  # On the ladder
                    if my != 0:
                        self.yFric = 0
                        self.yVel = clamp(-20, self.yVel + my, 20)
                    else:
                        self.yFric = 0.8

                    if self.yVel != 0:  # Get off the ladder
                        instl, cl = instance_place(oLadder, self.x, self.y)
                        if cl <= 0 or (my <= 0 and not self.onAir):  # If there is no ladder or it is grounded.
                            self.oStatus = oStatusContainer.IDLE
                            self.sprite_set("Player")
                            self.y += 1

        else:  # It would be eventual, and uncontrollable
            self.image_alpha = 1

            if self.oStatus == oStatusContainer.DEAD:
                self.sprite_set("PlayerDead")


# Parent of Enemies
class oEnemyParent(GObject):
    """
            모든 적 객체의 부모 객체
    """
    name = "NPC"
    identify = ID_ENEMY
    # sprite_index = sprite_get("Snake")
    depth = 500

    hp, maxhp = 1, 1
    mp, maxmp = 0, 0
    oStatus = oStatusContainer.IDLE
    image_speed = 0
    collide_with_player: bool = false
    attack_delay = 0

    def handle_none(self, *args):
        pass

    def handle_be_idle(self, *args):
        pass

    def handle_be_patrol(self, *args):
        pass

    def handle_be_walk(self, *args):
        pass

    def handle_be_track(self, *args):
        pass

    def handle_be_stunned(self, *args):
        pass

    def handle_be_dead(self, *args):
        pass

    def handle_idle(self, *args):
        pass

    def handle_patrol(self, *args):
        pass

    def handle_walk(self, *args):
        pass

    def handle_track(self, *args):
        pass

    def handle_dead(self, *args):
        pass

    def handle_stunned(self, frame_time):
        if self.stunned <= 0:
            if self.hp > 0:
                self.status_change(oStatusContainer.IDLE)
            else:
                self.status_change(oStatusContainer.DEAD)
        if not self.onAir:
            self.stunned -= frame_time

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.table = {
            oStatusContainer.IDLE: (self.handle_idle, self.handle_be_idle),
            oStatusContainer.WALK: (self.handle_walk, self.handle_be_walk),
            oStatusContainer.PATROL: (self.handle_patrol, self.handle_be_patrol),
            oStatusContainer.TRACKING: (self.handle_track, self.handle_be_track),
            oStatusContainer.STUNNED: (self.handle_stunned, self.handle_be_stunned),
            oStatusContainer.DEAD: (self.handle_dead, self.handle_be_dead)
        }

    def status_change(self, what):
        if self.oStatus != what:
            (self.table[what])[1]()
        self.oStatus = what

    def event_step(self, frame_time):
        super().event_step(frame_time)

        (self.table[self.oStatus])[0](frame_time)


class oSoldier(oEnemyParent):
    hp, maxhp = 4, 4
    name = "Soldier"
    xVelMin, xVelMax = -45, 45
    count = 0

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("SoldierIdle")
        self.runspr = sprite_get("SoldierRun")
        self.image_speed = 0
        self.image_xscale = choose(-1, 1)

    def phy_collide(self, how: float or int):
        super().phy_collide(how)
        if self.oStatus < oStatusContainer.STUNNED and abs(how) > 1:
            self.xVel *= -1
            self.image_xscale *= -1

    def handle_be_idle(self):
        self.sprite_set("SoldierIdle")

    def handle_be_walk(self, *args):
        self.sprite_index = self.runspr
        self.image_speed = 0.7

    def handle_be_stunned(self):
        self.sprite_set("SoldierStunned")

    def handle_be_dead(self):
        self.sprite_set("SoldierDead")

    def handle_idle(self, *args):
        """
            This method does not mean literally stopping when idle.
            Some gobjects can move while idle status.
        """
        self.count += delta_velocity() * args[0]
        if self.count >= delta_velocity(1) and irandom(99) == 0:
            self.status_change(oStatusContainer.WALK)
            self.count = 0
            if irandom(4) == 0:
                self.image_xscale *= -1

    # moves slowly
    def handle_walk(self, *args):
        checkl, checkr = self.place_free(-10, -10), self.place_free(10, -10)
        if checkl and checkr:
            self.status_change(oStatusContainer.IDLE)
            return

        distance = delta_velocity(10) * args[0]
        # self.count += delta_velocity() * args[0]
        if self.image_xscale == 1:
            if self.place_free(distance + 10, 0) and not self.place_free(distance + 10, -10):
                self.xVel = 10
            else:
                self.image_xscale = -1
                self.xVel = -10
        else:
            if self.place_free(distance - 10, 0) and not self.place_free(distance - 10, -10):
                self.xVel = -10
            else:
                self.image_xscale = 1
                self.xVel = 10

        if irandom(99) == 0:
            self.xVel = 0
            self.status_change(oStatusContainer.IDLE)

    def handle_dead(self, *args):
        pass

    def handle_stunned(self, frame_time):
        super().handle_stunned(frame_time)


class oSnake(oEnemyParent):
    hp, maxhp = 1, 1
    name = "Snake"
    count = 0

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("SnakeIdle")
        self.runspr = sprite_get("SnakeRun")
        self.image_speed = 0

    def handle_be_idle(self):
        self.sprite_set("SnakeIdle")

    def handle_be_walk(self, *args):
        self.sprite_index = self.runspr
        self.image_speed = 0.65

    def handle_idle(self, *args):
        self.count += delta_velocity()
        if self.count >= delta_velocity(irandom_range(8, 12)) and irandom(99) == 0:
            self.status_change(oStatusContainer.WALK)
            self.count = 0

    def handle_walk(self, *args):
        checkl, checkr = self.place_free(-10, -10), self.place_free(10, -10)
        if checkl and checkr:
            self.status_change(oStatusContainer.IDLE)
            return

        distance = delta_velocity(15) * args[0]
        self.count += delta_velocity() * args[0]
        if self.image_xscale == 1:
            if self.place_free(distance + 10, 0) and not self.place_free(distance + 10, -10):
                self.xVel = 15
            else:
                self.image_xscale = -1
                self.xVel = -15
        else:
            if self.place_free(distance - 10, 0) and not self.place_free(distance - 10, -10):
                self.xVel = -15
            else:
                self.image_xscale = 1
                self.xVel = 15

        if self.count >= delta_velocity(20):
            if irandom(99) == 0:
                self.xVel = 0
                self.status_change(oStatusContainer.IDLE)
                self.count = 0

    def handle_be_dead(self, *args):
        self.destroy()


class oCobra(oSnake):
    name = "Cobra"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("CobraIdle")
        self.runspr = sprite_get("CobraRun")
        self.image_speed = 0

    def handle_be_idle(self):
        self.sprite_set("CobraIdle")


class oBlood(oEffectParent):
    name = "Blood"
    depth = 700

    def event_step(self, frame_time):
        super().event_step(frame_time)