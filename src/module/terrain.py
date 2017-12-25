from module.constants import *

from module import framework
import json

from module.game.gobject_header import *
from module.game.game_solid import *

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
    tile_w: int = 20
    tile_h: int = 20
    map_grid_w: int = 32
    map_grid_h: int = 16
    time: float = 90

    def __init__(self, paths: str):
        # Parsing
        with open(path_data + paths + ".json") as mapfile:
            self.parsed = json.load(mapfile)
            self.data = self.parsed["layers"][0]["data"]
            self.floors = self.parsed["layers"][1]["data"]
            self.tile_w = self.parsed["tilewidth"]
            self.tile_h = self.parsed["tileheight"]
            self.map_grid_w = self.parsed["width"]
            self.map_grid_h = self.parsed["height"]

    def get_stage_title(self) -> str:
        return self.parsed["title"]

    def generate(self):
        print("Generating a chunk.")

        length = len(self.data)
        if length <= 0:
            return

        currln, prevln = [], []
        nx, ny = 0, self.map_grid_h * self.tile_h - 20
        for i in range(length):
            current = self.data[i]

            if current is not 0:
                try:
                    def icreate(ty, depth, x, y):
                        ninst = ty(depth, x, y)
                        return ninst

                    def get_createtype(char: str):
                        return tile_mess[char]

                    whattocreate = get_createtype(current)
                    obj = icreate(whattocreate[0], None, nx, ny)
                    # obj_identify = obj.identify
                    # print(str(obj) + "<" + str(current) + "> (x = " + str(nx) + ", y = " + str(ny) + ")")

                    if obj.identify == ID_TILE:
                        try:
                            if i >= self.map_grid_w:  # check top
                                getu = self.data[i - self.map_grid_w]
                                whattocheck: str = get_createtype(getu)[0].identify
                                if getu == current:
                                    obj.tile_up = 1
                                elif getu != 0 and whattocheck is ID_TILE:
                                    obj.tile_up = 2
                            else:
                                obj.tile_up = 1

                            if i < length - self.map_grid_w:  # check bottom
                                getd = self.data[i + self.map_grid_w]
                                whattocheck: str = get_createtype(getd)[0].identify
                                if getd == current:
                                    obj.tile_down = 1
                                elif getd != 0 and whattocheck is ID_TILE:
                                    obj.tile_down = 2
                            else:
                                obj.tile_down = 1

                            if i > 0 and self.tile_w <= nx:  # check left
                                getl = self.data[i - 1]
                                whattocheck: str = get_createtype(getl)[0].identify
                                if getl == current:
                                    obj.tile_left = 1
                                elif getl != 0 and whattocheck is ID_TILE:
                                    obj.tile_left = 2
                            else:
                                obj.tile_left = 1

                            if i <= length - 1 and (self.map_grid_w - 1) * self.tile_w >= nx:  # check right
                                getr = self.data[i + 1]
                                whattocheck: str = get_createtype(getr)[0].identify
                                if getr == current:
                                    obj.tile_right = 1
                                elif getr != 0 and whattocheck is ID_TILE:
                                    obj.tile_right = 2
                            else:
                                obj.tile_right = 1
                        except IndexError:
                            pass
                    currln.append(obj)
                    try:
                        if whattocreate[1] is TYPE_DOODAD:
                            obj.x += self.tile_w / 2
                            obj.y += self.tile_h / 2
                        elif whattocreate[1] is TYPE_INSTANCE:
                            obj.x += self.tile_w / 2
                            obj.y += self.tile_h
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

        nx, ny = 0, self.map_grid_h * self.tile_h - 20
        for i in range(length):
            current = self.floors[i]

            if current is 53:  # floor
                oFloor(0, nx, ny)
            elif current is 54:  # platform
                oPlatform(0, nx, ny)

            nx += self.tile_w
            if nx >= self.map_grid_w * self.tile_w:
                del prevln
                prevln = currln.copy()  # push current line back to previous line
                currln.clear()  # make new list

                nx = 0
                ny -= self.tile_h

        clist = get_instance_list(ID_TILE)
        for inst in clist:
            inst.tile_correction()

        framework.stage_number += 1
