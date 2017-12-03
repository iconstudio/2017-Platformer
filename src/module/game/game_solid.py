from module.constants import *
from module.functions import *

from module.game.gobject_header import *
from module.game.game_doodad import oLushDecoration, oDirtBrickDecoration

__all__ = [
    "oBrickCastle", "oLush", "oBrickDirt", "oStonewall", "oLushFlat", "oDirtBrickFlat", "oBlock", "oBlockMetal",
    "oBlockBlack", "oGravestone", "oGravestoneAsh", "oTreeTrunk", "oTreeTop", "oTreeTopDead", "oTreeLeaves",
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
        if self.tile_up != 1 or self.tile_down != 1:
            self.sprite_set("sLushDirectional")
            if self.tile_up == 1 and self.tile_down != 1:
                self.image_index = 0
            elif self.tile_down == 1:
                self.image_index = 1
            elif self.tile_up == 0 and self.tile_down == 0:
                self.image_index = 2
        if self.tile_up != 1:
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
        if self.tile_up != 1 or self.tile_down != 1:
            self.sprite_set("sDirtBrickDirectional")
            if self.tile_up == 1 and self.tile_down != 1:
                self.image_index = 0
            elif self.tile_down == 1:
                self.image_index = 1
            elif self.tile_up == 0 and self.tile_down == 0:
                self.image_index = 2
            if self.tile_up != 1:
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
        if self.tile_down != 0:
            self.image_index = 1


# Flat wood of Dirt
class oDirtBrickFlat(Solid):
    name = "Flat of Dirt"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sDirtBrickFlat")

    def tile_correction(self):
        if self.tile_down != 0:
            self.image_index = 1


# Block (Brown)
class oBlock(Solid):
    name = "oBlock"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sBlock")


# Block (Metal)
class oBlockMetal(Solid):
    name = "oBlock"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sBlockMetal")


# Block (Black)
class oBlockBlack(Solid):
    name = "Gravestone"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sBlockBlack")


# Gravestone
class oGravestone(Solid):
    name = "Gravestone"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sGrave")


# Ash Gravestone
class oGravestoneAsh(Solid):
    name = "Ash Gravestone"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sGraveAsh")


# Body of Tree
class oTreeTrunk(Solid):
    depth = 1000

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTreeTrunk")

    def tile_correction(self):
        if self.tile_up == 0:
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


# Leaves of Tree at End
class oTreeLeavesEnd(Solid):
    isPlatform = true

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTreeLeaves")
        self.image_index = 0
        self.image_speed = 0

    def tile_correction(self):
        if not instance_place(oTreeTop, self.x + 21, self.y + 10) \
                and not instance_place(oTreeLeaves, self.x + 21, self.y):
            self.image_xscale = -1


# Died Leaves of Tree at End
class oTreeLeavesDeadEnd(oTreeLeavesEnd):
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
        if instance_place(oTreeTrunk, self.x, self.y + 4):
            self.image_xscale = -1


# Body of Tree
class oTreeBranchDead(oTreeBranch):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 1
