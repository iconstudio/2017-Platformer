from gobject_header import *

__all__ = [
    "oRock", "oSpringShoes", "oSpikeShoes", "oCape", "oAnkh"
]


# Object : Rock
class oRock(oItemParent):
    name = "Rock"
    depth = 1000

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sRock")


# Object : Shoes with Spring
class oSpringShoes(oItemParent):
    name = "Spring Shoes"
    depth = 1000
    gravity_default = 0

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sSpringShoes")


# Object : Shoes with Spike
class oSpikeShoes(oItemParent):
    name = "Spike Shoes"
    depth = 1000
    gravity_default = 0

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sSpikeShoes")


# Object : Cape which can double jump
class oCape(oItemParent):
    name = "Cape"
    depth = 1000
    gravity_default = 0

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sCape")


# Object : Ankh that adds one life
class oAnkh(oItemParent):
    name = "Ankh"
    depth = 1000
    gravity_default = 0

    def __init__(self, ndepth, nx, ny):
        super().__init__(ndepth, nx, ny)
        self.sprite_set("sAnkh")
