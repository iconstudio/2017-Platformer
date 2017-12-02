from module.constants import *
from module.functions import *

from module.game.gobject_header import *
from module.game.game_doodad import oLushDecoration, oDirtBrickDecoration

__all__ = [
    "oBrickCastle", "oLush", "oBrickDirt", "oStonewall", "oLushFlat", "oDirtBrickFlat",
    "oGravestone", "oGravestoneAsh", "oTreeTrunk", "oTreeTop", "oTreeTopDead", "oTreeLeaves",
    "oTreeLeavesEnd", "oTreeLeavesDeadEnd", "oTreeBranch", "oTreeBranchDead"
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


# Flat wood of Lush
class oLushFlat(Solid):
    name = "Flat of Lush"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sLushFlat")

    def tile_correction(self):
        if self.tile_down:
            self.image_index = 1


# Flat wood of dir
class oDirtBrickFlat(Solid):
    name = "Flat of Lush"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sLushFlat")

    def tile_correction(self):
        if self.tile_down:
            self.image_index = 1


# Gravestone
class oGravestone(Solid):
    name = "Gravestone"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("Grave")


# Ash Gravestone
class oGravestoneAsh(Solid):
    name = "Gravestone"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("GraveAsh")


# Body of Tree
class oTreeTrunk(Solid):
    depth = 1000

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTreeTrunk")

    def tile_correction(self):
        if not self.tile_up:
            self.image_index = 1


# Top of Tree
class oTreeTop(Solid):
    depth = 1000

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTreeTop")


# Top of Died Tree
class oTreeTopDead(oTreeTop):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 1


# Leaves of Tree
class oTreeLeaves(Solid):
    isPlatform = true

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTreeLeaves")
        self.image_index = 2

    def tile_correction(self):
        if self.tile_right:
            self.image_xscale = -1


# Leaves of Tree at End
class oTreeLeavesEnd(oTreeLeaves):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 0


# Died Leaves of Tree at End
class oTreeLeavesDeadEnd(oTreeLeaves):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 1


# Branch of Tree
class oTreeBranch(Solid):
    isPlatform = true

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTreeBranches")

    def tile_correction(self):
        if not instance_place(oTreeTrunk, self.x + 21, self.y + 10):
            self.image_xscale = -1


# Body of Tree
class oTreeBranchDead(oTreeBranch):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 1
