from module.constants import *
from module.functions import *

from module import framework

import json
from game.gobject_header import *

__all__ = [
    "terrain_tile_assign", "terrain_tile_clear", "TerrainManager", "TerrainGenerator",
    "TYPE_TERRAIN", "TYPE_DOODAD", "TYPE_INSTANCE", "TYPE_BG"
]

# ==================================================================================================
#                                               지형
# ==================================================================================================

TYPE_TERRAIN = 0
TYPE_DOODAD = 1
TYPE_INSTANCE = 2
TYPE_BG = 3
tile_mess = {}


def terrain_tile_assign(string: str or int, *ty: (type, int)):
    global tile_mess
    tile_mess[string] = ty


def terrain_tile_clear():
    global tile_mess
    tile_mess.clear()


# Terrain Manager
class TerrainManager:
    data = ""
    path_world = ""

    def __init__(self, themepath: str):
        self.path_world = themepath

    def allocate(self, world: str):
        print("Allocating a chunk.")
        self.data = world

    def generate(self):
        global tile_mess
        print("Generating a chunk.")

        newx = 0
        newy = 16 * 20 - 20
        neww = 32
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
                    whattocreate = tile_mess[current]
                    obj = (whattocreate[0])(None, newx, newy)
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
                    newx = 0
                    newy -= 20
                    continue

            j += 1
            currln += current
            newx += 20
            # Wrap
            if current == '\n':
                neww = j
                j = 0
                newx = 0
                newy -= 20
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

        for inst in get_instance_list(ID_SOLID):
            inst.tile_correction()

    def __del__(self):
        del self.data


# Terrain Generator
class TerrainGenerator:
    parsed: dict = {}
    data: list = []
    number: int = 0
    grid_w: int = 32
    grid_h: int = 18
    tile_w: int = 20
    tile_h: int = 20
    map_grid_w: int = 32
    map_grid_h: int = 16
    time: float = 90

    def __init__(self, paths: str):
        # Parsing
        with open(path_data + paths + ".json") as mapfile:
            self.parsed = json.load(mapfile)
            self.data = self.parsed["data"]
            self.number = self.parsed["number"]
            self.grid_w = self.parsed["grid_w"]
            self.grid_h = self.parsed["grid_h"]
            self.tile_w = self.parsed["tile_w"]
            self.tile_h = self.parsed["tile_h"]
            self.map_grid_w = self.parsed["map_grid_w"]
            self.map_grid_h = self.parsed["map_grid_h"]
            self.time = self.parsed["time"]
        framework.scene_set_size(self.tile_w * self.map_grid_w)

    def get_stage_title(self) -> str:
        return self.parsed["title"]

    def generate(self):
        print("Generating a chunk.")

        length = len(self.data)
        if length <= 0:
            return

        currln, prevln = [], []
        nx, ny = 0, self.map_grid_h * self.tile_h
        for i in range(length):
            current = self.data[i]

            if current is not '0':
                try:
                    def icreate(ty, depth, x, y):
                        ninst = ty(depth, x, y)
                        return ninst

                    whattocreate = tile_mess[current]
                    obj = icreate(whattocreate[0], None, nx, ny)
                    # print(str(obj) + "<" + str(current) + "> (x = " + str(nx) + ", y = " + str(ny) + ")")
                    if ny >= framework.scene_height - 20:
                        obj.tile_up = true
                    if ny <= 20:
                        obj.tile_down = true

                    if obj.identify == ID_SOLID:
                        # print("solid")
                        try:
                            if i >= self.map_grid_w and self.data[i - self.map_grid_w] == current:
                                #print(str(obj) + "<" + str(current) + "> (x = " + str(nx) + ", y = " + str(ny) + ")")
                                obj.tile_up = true
                            if i < length - self.map_grid_w and self.data[i + self.map_grid_w] == current:
                                #print(str(obj) + "<" + str(current) + "> (x = " + str(nx) + ", y = " + str(ny) + ")")
                                obj.tile_down = true
                        except IndexError:
                            pass
                    currln.append(current)
                    try:
                        if whattocreate[1] in (TYPE_INSTANCE, TYPE_DOODAD):
                            obj.x += self.tile_w / 2
                            obj.y += self.tile_h / 2
                    except AttributeError:
                        pass
                except KeyError:
                    pass

            nx += self.tile_w
            if nx >= self.map_grid_w * self.tile_w:
                del prevln
                prevln = currln.copy()  # push current line back to previous line
                currln.clear()  # make new list

                nx = 0
                ny -= self.tile_h

        clist = get_instance_list(ID_SOLID)
        for inst in clist:
            inst.tile_correction()
