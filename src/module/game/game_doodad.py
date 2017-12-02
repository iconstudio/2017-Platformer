from module.pico2d import *
from module.functions import *
from module.constants import *

from module.game.gobject_header import *

__all__ = [
    "oLushDecoration", "oDirtBrickDecoration",
    "oMillHousechip", "oMillHousestone", "oMillHousechipL", "oMillHousechipR",
    "oMillHousechipM", "oTorch", "oLadder"
]


# A Decorator of Dirt
class oDirtBrickDecoration(oDoodadParent):
    name = "Dirt Decoration"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sDirtBrickDoodad")
        self.image_speed = 0
        self.image_index = choose(0, 0, 0, 0, 0, 0, 0, 1, 1)


# A Decorator of Lush
class oLushDecoration(oDoodadParent):
    name = "Lush Decoration"

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sLushDoodad")
        self.image_speed = 0
        self.image_index = choose(0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2)


# Tiki Torch
class oTorch(oDoodadParent):
    name = "Torch"
    image_speed = 0.6
    step_enable = true

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sTorch")
        self.image_index = irandom(4)


# Ladder
class oLadder(oDoodadParent):
    name = "Ladder"
    depth = 900

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sLadder")
        self.image_speed = 0


# A tile of mil at intro
class oMillHousechip(oDoodadParent):
    name = "Wood"
    depth = 900

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sWood")
        self.image_speed = 0


# A tile of mil at intro
class oMillHousestone(oDoodadParent):
    name = "Stone"
    depth = 900
    image_index = 0

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sStonewall")


# A tile of mil at intro
class oMillHousechipL(oMillHousechip):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 1


# A tile of mil at intro
class oMillHousechipR(oMillHousechip):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 2


# A tile of mil at intro
class oMillHousechipM(oMillHousechip):
    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.image_index = 3
