from module.pico2d import *
from module.functions import *
from module.constants import *

from module.framework import Camera
from module.framework import io

from module.gobject_header import *
from module.sprite import *

__all__ = [
    "instance_create", "instance_draw_update",
    "oBrickCastle", "oLush", "oBrickDirt",
    "oPlayer", "oSoldier", "oSnake", "oCobra",
]


def instance_draw_update():
    global instance_list, instance_draw_list, instance_update
    if instance_update or len(instance_draw_list) <= 0:
        print("instance drawing list would be updated")
        # del instance_draw_list
        instance_update = false
        instance_draw_list = sorted(instance_list, key = lambda gobject: -gobject.depth)


# ==================================================================================================
#                                               게임
# ==================================================================================================


# Declaring of Special Objects ( Need a canvas )
player_lives = 3


# ==================================================================================================
#                                    사용자 정의 객체 / 함수
# ==================================================================================================
# Object : Functions
def instance_create(Ty, ndepth = 0, nx = int(0), ny = int(0)) -> object:
    temp = Ty(ndepth, nx, ny)
    global instance_last
    instance_last = temp
    return temp


def instance_place(Ty, fx, fy) -> (list, int):
    try:
        ibj = Ty.identify
    except AttributeError:
        print("Cannot find variable 'identify' in %s" % (str(Ty)))
        sys.exit(-1)

    __returns = []
    global instance_list, instance_list_spec
    if ibj == "":
        clist = instance_list
    else:
        clist = instance_list_spec[ibj]
    length = len(clist)
    if length > 0:
        for inst in clist:
            tempspr: Sprite = inst.sprite_index
            otho_left = int(inst.x - tempspr.xoffset)
            otho_top = int(inst.y - tempspr.yoffset)
            if point_in_rectangle(fx, fy, otho_left, otho_top, otho_left + tempspr.width, otho_top + tempspr.height):
                __returns.append(inst)

    return __returns, len(__returns)


# Definitions of Special Objects

# Castle Brick
class oBrickCastle(Solid):
    name = "Brick of Mine"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sCastleBrick")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3)


# Lush
class oLush(Solid):
    name = "Brick of Forest"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sLush")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 1, 1)

    def tile_correction(self):
        if not self.tile_up or not self.tile_down:
            self.sprite_set("sLushDirectional")
            if self.tile_up and not self.tile_down:
                self.image_index = 0
            elif self.tile_down:
                self.image_index = 1
            else:
                self.image_index = 2
        if not self.tile_up:
            newdeco = instance_create(oLushDecoration, None, self.x + 4, self.y + 20)
            newdeco.parent = self


# Dirt Brick
class oBrickDirt(Solid):
    name = "Brick of Mine"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sDirt")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 1, 1)


# Player
class oPlayer(GObject):
    name = "Player"
    depth = 0
    image_speed = 0
    # anitem what to hold on
    held: object = None
    invincible: int = 0

    # real-scale: 54 km per hour
    xVelMin, xVelMax = -54, 54

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_index = sprite_get("Player")

        global container_player
        container_player = self
        self.hfont = load_font(path_font + "윤고딕_310.ttf", 20)

    def event_step(self, frame_time):
        super().event_step(frame_time)
        if self.oStatus < oStatusContainer.CHANNELING:  # Player can control its character.
            Camera.set_pos(self.x - Camera.width / 2, self.y - Camera.height / 2)
            # Stomp enemies under the character
            whothere, howmany = instance_place(oEnemyParent, self.x, self.y - 9)
            if howmany > 0 > self.yVel and self.onAir:
                for enemy in whothere:
                    if enemy.oStatus < oStatusContainer.STUNNED:
                        if enemy.name not in ("ManEater", "Lavaman",):
                            if self.yVel < -50:
                                self.yVel *= -0.6
                            else:
                                self.yVel = 60
                            enemy.hp -= 1
                            if enemy.hp <= 0:
                                enemy.status_change(oStatusContainer.DEAD)
                            else:
                                enemy.status_change(oStatusContainer.STUNNED)
                                enemy.stunned = delta_velocity(5)

            mx = 0
            if io.key_check(SDLK_LEFT): mx -= 1
            if io.key_check(SDLK_RIGHT): mx += 1

            if mx != 0:
                self.xFric = 0
                if not self.onAir:
                    self.xVel += mx * 5
                else:
                    self.xVel += mx * 2
                self.image_xscale = mx
            else:
                self.xFric = 0.6

            if io.key_check_pressed(SDLK_UP):
                if not self.onAir:
                    self.yVel = 90

            if not self.onAir:
                if self.xVel != 0:
                    self.image_speed = 0.8
                    self.sprite_index = sprite_get("PlayerRun")
                else:
                    self.sprite_set("Player")
            else:
                self.sprite_set("PlayerJump")
        else:  # It would be eventual, and uncontrollable
            if self.oStatus == oStatusContainer.DEAD:
                self.sprite_set("PlayerDead")

    def event_draw(self):
        super().event_draw()
        self.hfont.draw(200, screen_height - 50, 'Time: %1.0f' % get_time())


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
            self.stunned -= delta_velocity() * frame_time

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
        self.sprite_set("SoldierDead")

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

    def handle_dead(self, *args):
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


# A Decorator of Lush
class oLushDecoration(oDoodadParent):
    name = "Lush Decoration"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sLushDoodad")
        self.image_speed = 0
        self.image_index = choose(0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2)


class oBlood(oEffectParent):
    name = "Blood"
    depth = 700

    def event_step(self, frame_time):
        super().event_step(frame_time)
