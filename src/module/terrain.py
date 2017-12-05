from module.constants import *

import json
from module.camera import *
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
        scene_set_size(self.tile_w * self.map_grid_w)

    def get_stage_title(self) -> str:
        return self.parsed["title"]

    def get_stage_number(self) -> int:
        return self.parsed["number"]

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

                    def get_createtype(char: str):
                        return tile_mess[char]

                    whattocreate = get_createtype(current)
                    obj = icreate(whattocreate[0], None, nx, ny)
                    # print(str(obj) + "<" + str(current) + "> (x = " + str(nx) + ", y = " + str(ny) + ")")

                    if obj.identify == ID_SOLID:
                        try:
                            if i >= self.map_grid_w:  # check top
                                getu = self.data[i - self.map_grid_w]
                                whattocheck: str = get_createtype(getu)[0].identify
                                if getu == current:
                                    obj.tile_up = 1
                                elif getu != 0 and whattocheck is ID_SOLID:
                                    obj.tile_up = 2
                            else:
                                obj.tile_up = 1

                            if i < length - self.map_grid_w:  # check bottom
                                getd = self.data[i + self.map_grid_w]
                                whattocheck: str = get_createtype(getd)[0].identify
                                if getd == current:
                                    obj.tile_down = 1
                                elif getd != 0 and whattocheck is ID_SOLID:
                                    obj.tile_down = 2
                            else:
                                obj.tile_down = 1

                            if i > 0:  # check left
                                getl = self.data[i - 1]
                                whattocheck: str = get_createtype(getl)[0].identify
                                if getl == current:
                                    obj.tile_left = 1
                                elif getl != 0 and whattocheck is ID_SOLID:
                                    obj.tile_left = 2
                            else:
                                obj.tile_left = 1

                            if i <= length - 1:  # check right
                                getr = self.data[i + 1]
                                whattocheck: str = get_createtype(getr)[0].identify
                                if getr == current:
                                    obj.tile_right = 1
                                elif getr != 0 and whattocheck is ID_SOLID:
                                    obj.tile_right = 2
                            else:
                                obj.tile_right = 1
                        except IndexError:
                            pass
                    currln.append(obj)
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

        # Optimization
        rlist = []
        for inst in clist:
            if inst.tile_left != 0 and inst.tile_up != 0 and inst.tile_right != 0 and inst.tile_down != 0:
                rlist.append(inst)

        clist = get_instance_list(ID_SOLID)
        for inst in clist:
            inst.tile_correction()

        for inst in rlist:
            instance_list_remove_something(ID_SOLID_EX, inst)
            # inst.destroy()
