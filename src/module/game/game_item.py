from module.functions import *
from module.constants import *

from module.game.gobject_header import *

__all__ = [
    "oRock", "oSpringShoes"
]


# Object : Rock
class oRock(oItemParent):
    name = "Door"
    depth = 1000

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sRock")


# Object : Shoes with Spring
class oSpringShoes(oItemParent):
    name = "Metal Door"
    depth = 1000

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sSpringShoes")
