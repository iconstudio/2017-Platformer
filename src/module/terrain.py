from module.constants import *

from module import framework

import json
from module.game.gobject_header import *

__all__ = [
    "terrain_tile_assign", "terrain_tile_clear", "TerrainGenerator",
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
                                obj.tile_up = true
                            if i < length - self.map_grid_w and self.data[i + self.map_grid_w] == current:
                                obj.tile_down = true
                        except IndexError:
                            pass
                        try:
                            if nx < self.tile_w or (i > 0 and self.data[i - 1] == current):
                                obj.tile_left = true
                            if nx >= (self.map_grid_w - 1) * self.tile_w \
                                    and (i <= length - 1) and self.data[i + 1] == current:
                                obj.tile_right = true
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

        # Optimization
        for inst in clist:
            if inst.tile_left and inst.tile_up and inst.tile_right and inst.tile_down:
                instance_list_remove_something(ID_SOLID, inst)
                continue
