from module.constants import *
from module.functions import *

from module.game.gobject_header import *
from module.game.game_doodad import oLushDecoration, oDirtBrickDecoration

__all__ = [
    "oFloor", "oPlatform",
    "oBrickCastle", "oBrickCastleSewer", "oLush", "oBrickDirt", "oStonewall", "oLushFlat", "oDirtBrickFlat",
    "oBlock", "oBlockMetal", "oBrickCastleTop",
    "oBlockBlack", "oGravestone", "oGravestoneAsh", "oTreeTrunk", "oTreeTop", "oTreeTopDead", "oTreeLeaves",
    "oTreeLeavesEnd", "oTreeLeavesDeadEnd", "oTreeBranch", "oTreeBranchDead",
    "oTreeLeavesEndLeft", "oTreeLeavesDeadEndLeft", "oTreeBranchLeft", "oTreeBranchDeadLeft",
]


# Real Solids
class oFloor(Solid):
    name = "Floor Hard"
    identify = ID_SOLID

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sBlank")


# Real Solids
class oPlatform(Solid):
    name = "Floor Soft"
    identify = ID_SOLID
    isPlatform = true

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sBlank")


# Castle Brick
class oBrickCastle(Solid):
    name = "Brick of Castle"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sCastleBrick")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3)


# Castle Top Brick
class oBrickCastleTop(Solid):
    name = "Top Brick of Castle"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sCastleBrickDirectional")
        if self.tile_down != 1:
            self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 1, 1, 1)
        else:
            self.image_index = 0


# Castle Sewer Brick
class oBrickCastleSewer(Solid):
    name = "Sewer Brick of Castle"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sCastleBrickSewer")
        self.image_index = choose(0, 0, 0, 1, 1, 2, 2)


# Lush
class oLush(Solid):
    name = "Brick of Forest"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sLush")
        self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 1, 1)

    def tile_correction(self):
        onUp, onDown = (self.tile_up == 1), (self.tile_down == 1)
        if not onUp or not onDown:
            self.sprite_set("sLushDirectional")
            if onUp and not onDown:
                self.image_index = 0
            elif onDown:
                self.image_index = 1
            else:
                self.image_index = 2
            if self.image_index != 0:
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
            else:
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
class oLushFlat(oLush):
    name = "Flat of Lush"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sLushFlat")

    def tile_correction(self):
        if self.tile_down != 1:
            self.image_index = 1


# Flat wood of Dirt
class oDirtBrickFlat(oBrickDirt):
    name = "Flat of Dirt"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sDirtBrickFlat")

    def tile_correction(self):
        if self.tile_down != 1:
            self.image_index = 1


# Block (Brown)
class oBlock(Solid):
    name = "Block"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sBlock")


# Block (Metal)
class oBlockMetal(Solid):
    name = "Iron Block"
    coll = None

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sBlockMetal")
        self.coll = oFloor(0, nx, ny)

    def __del__(self):
        self.coll.destroy()


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
    name = "Tree Trunk"
    depth = 1000

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTreeTrunk")

    def tile_correction(self):
        if self.tile_up == 0:
            self.image_index = 1


# Top of Tree
class oTreeTop(Solid):
    name = "Tree Top"
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
    name = "Tree Leaves"
    isPlatform = true

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTreeLeaves")
        self.image_index = 2


# Leaves of Tree at End
class oTreeLeavesEnd(Solid):
    name = "End of Tree Leaves"
    isPlatform = true

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTreeLeaves")
        self.image_index = 0
        self.image_speed = 0


# Died Leaves of Tree at End
class oTreeLeavesDeadEnd(oTreeLeavesEnd):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 1


# Died Leaves of Tree at End
class oTreeLeavesEndLeft(oTreeLeavesEnd):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 3


# Died Leaves of Tree at End
class oTreeLeavesDeadEndLeft(oTreeLeavesEnd):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 4


# Branch of Tree
class oTreeBranch(Solid):
    name = "Tree Branches"
    isPlatform = true

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTreeBranches")


# Dead Branch of Tree
class oTreeBranchDead(oTreeBranch):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 1


# Branch of Tree
class oTreeBranchLeft(oTreeBranch):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 2


# Branch of Tree
class oTreeBranchDeadLeft(oTreeBranch):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 3
