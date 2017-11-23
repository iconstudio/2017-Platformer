from game.gobject_header import *
from module import framework
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
    def __init__(self, theme: int = 0):
        self.type_theme = theme
        self.data = TerrainAllocator(self.type_theme, 0, 0)

    def allocate(self, world: str, nx = None, ny = None):
        try:
            print("Allocating a chunk.")
            self.data.allocate(world, self.type_theme)
            if nx is not None:
                self.data.x = nx
            if ny is not None:
                self.data.y = ny

        except IndexError:
            print("Cannot add new chunk!")

    def generate(self):
        self.data.generate()

        global instance_list_spec
        clist = instance_list_spec[ID_SOLID]
        for inst in clist:
            inst.tile_correction()

    def __del__(self):
        del self.data


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
        print("Generating a chunk.")
        newx = self.x
        newy = self.y + self.h - self.tile_h
        neww = self.hsz
        currln = ""
        currlist: list = []
        prevlist: list = []
        j = 0

        for i in range(len(self.data)):
            current = self.data[i]

            # ignore blanks
            if current == ' ':
                continue

            if current is not ';' and current is not '0' and current is not '\n':
                try:
                    whattocreate = tcontainer.mess[current]
                    obj = whattocreate(None, newx, newy)
                    if newy >= framework.scene_height - 20:
                        obj.tile_up = true
                    if newy <= 20:
                        obj.tile_down = true

                    length = len(currln)
                    if length > 0:
                        try:
                            if currln[length - neww] == current:
                                obj.tile_up = true
                        except IndexError:
                            pass
                    currlist.append(obj)  # save objects in current line

                    try:
                        tempspr = obj.sprite_index
                        obj.x += tempspr.xoffset
                        obj.y += tempspr.yoffset
                    except AttributeError:
                        pass
                except KeyError:
                    pass
            else:
                # Skip this line
                if current == ';':
                    currlist.clear()
                    j = 0
                    newx = self.x
                    newy -= self.tile_h
                    continue

            j += 1
            currln += current
            newx += self.tile_w
            # Wrap
            if current == '\n':
                neww = j
                j = 0
                newx = self.x
                newy -= self.tile_h
                # Parsing
                # """   * previous line     <- X [preprevlist.?]
                # """   * current line      <- prevlist (but refered when parsing 'next' line)
                # """   * next line         <- currlist
                length = len(currlist)
                if len(prevlist) > 0 and length > 0:
                    k = 0
                    for inst in range(length):
                        try:
                            if prevlist[k].name is currlist[k].name:
                                prevlist[k].tile_down = true
                        except IndexError:
                            break
                        k += 1

                del prevlist
                prevlist = currlist.copy()  # push current line back to previous line
                currlist.clear()  # make new list

    def allocate(self, data: str, newtype: int = 0):
        self.data = data
        self.type_theme = newtype
