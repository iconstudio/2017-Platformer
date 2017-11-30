from module.pico2d import *
from module.functions import *
from module.constants import *

from game.gobject_header import *
from game.game_doodad import *

__all__ = []
__all__ += [
    "__all__",
    "oBrickCastle", "oLush", "oBrickDirt", "oStonewall",
]


# Castle Brick
class oBrickCastle(Solid):
    name = "Brick of Castle"

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
            newdeco = instance_create(oLushDecoration, None, self.x + 2, self.y + 20)
            newdeco.parent_set(self)


# Dirt Brick
class oBrickDirt(Solid):
    name = "Brick of Mine"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sDirtBrick")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 1, 1)

    def tile_correction(self):
        if not self.tile_up or not self.tile_down:
            self.sprite_set("sDirtBrickDirectional")
            if self.tile_up and not self.tile_down:
                self.image_index = 0
            elif self.tile_down:
                self.image_index = 1
            else:
                self.image_index = 2
            if not self.tile_up:
                newdeco = instance_create(oDirtBrickDecoration, None, self.x, self.y + 19)
                newdeco.parent_set(self)


# Stone Wall
class oStonewall(Solid):
    name = "Brick of Stone"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sStonewall")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 0, 1, 2)
