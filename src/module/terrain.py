from module.functions import *
from module.constants import *

__all__ = [
    "tcontainer", "ThemeContainer", "TerrainManager", "TerrainAllocator"
]


# ==================================================================================================
#                                               지형
# ==================================================================================================
# Object : Terrain Container
class ThemeContainer:
    mess = {}

    def signin(self, string: str, ty: type):
        self.mess[string] = ty

    def clear(self):
        self.mess.clear()


# Object : Terrain Container
class TerrainContainer:
    mess = {}

    def signin(self, string: str, ty: type):
        self.mess[string] = ty

    def clear(self):
        self.mess.clear()


tcontainer = TerrainContainer()


# Object : Terrain Manager
class TerrainManager:
    fits = []
    type_theme = 0

    def __init__(self, theme: int = 0, numberw: int = 1, numberh: int = 1):
        self.type_theme = theme
        for i in range(0, numberw, 1):
            for j in range(0, numberh, 1):
                newone = TerrainAllocator(self.type_theme, i * screen_width, j * screen_height)
                self.fits.append(newone)

    def allocate(self, data: str, position: int = 0):
        try:
            self.fits[position].allocate(data, self.type_theme)
        except IndexError:
            pass

    def generate(self):
        for alloc in self.fits:
            alloc.generate()

    def __del__(self):
        try:
            for alloc in self.fits:
                del alloc
        except IndexError:
            return
        except KeyError:
            return
            # finally:
            # del self.fits


# Object : A Allocating block of Terrain
class TerrainAllocator:
    data: str = ""  # Determines what to generate
    type_theme: int = 0
    type_path: int = 0  # Determines how to do.
    tile_w: int = 20
    tile_h: int = 20
    x, y, w, h, hsz, vsz = 0, 0, 0, 0, 0, 0

    def __init__(self, nt: int, nx: int, ny: int, nw: int = screen_width, nh: int = screen_height):
        self.assignment(nt, nx, ny, nw, nh)

    def assignment(self, nt: int, nx: int, ny: int, nw: int = screen_width, nh: int = screen_height):
        # The position of a map
        self.x, self.y = nx, ny
        # The size of a map
        self.w, self.h = nw, nh
        # The number of grid
        self.hsz, self.vsz = int(nw / self.tile_w), int(nh / self.tile_h)
        self.type_theme = nt

    def generate(self):
        newx = self.x
        newy = self.y + self.h - self.tile_h
        for i in range(0, len(self.data)):
            current = self.data[i]
            if current == '0' or current == ' ' or current == '\n':
                continue
            if current == ';':
                newx = self.x
                newy -= self.tile_h
                continue
            # newx = (i - math.floor(i / self.hsz)) * self.tile_w
            # newy = math.floor(i / self.hsz) * self.tile_h
            # noinspection PyUnusedLocal
            try:
                whattocreate = tcontainer.mess[current]
                whattocreate(100, newx, newy)
            except KeyError:
                pass
            newx += self.tile_w
            if newx >= self.w:
                newx = self.x
                newy -= self.tile_h

    def allocate(self, data: str, newtype: int = 0):
        self.data = data
        self.type_theme = newtype
