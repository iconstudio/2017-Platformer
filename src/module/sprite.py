from module.pico2d import *
from module.constants import *

import json

__all__ = [
    "Sprite",
    "sprite_list",
    "sprite_load", "sprite_get", "draw_sprite", "sprite_json_loads"
]

sprite_list: dict = {}  # 스프라이트는 이름으로 구분된다.


# Object : Sprites
class Sprite(object):
    name: str = ""
    number: int = 0
    width, height = 0, 0
    isSeparate: bool = false
    xoffset, yoffset = 0, 0
    __data__ = []

    def __init__(self, filepath: list or str, number, xoffset, yoffset):
        """
            이미지 불러오기, 이미지 분할, 리스트화 작업
        """
        self.__data__ = []
        if type(filepath) == list:  # 스프라이트가 여러 개의 이미지로 구성됨.
            self.isSeparate = true
            self.number = len(filepath)

            try:
                if self.number > 0:
                    for specpath in filepath:
                        img = load_image(specpath, xoffset, yoffset)
                        self.__data__.append(img)
                    self.width = int(self.__data__[0].w)
                    self.height = int(self.__data__[0].h)
            except IndexError:
                raise RuntimeError("스프라이트 목록이 비어있습니다!")
        else:  # 스프라이트가 낱장의 이미지로 구성됨.
            img = load_image(filepath, xoffset, yoffset)
            self.__data__.append(img)
            self.number = number  # the number of sprite in an image
            # size of each index
            self.width = int(self.__data__[0].w / number)
            self.height = int(self.__data__[0].h)

        self.xoffset, self.yoffset = self.__data__[0].xoffset, self.__data__[0].yoffset
        try:
            tempTy = type(number)
            if tempTy != int and tempTy != float:
                raise RuntimeError("스프라이트 불러오기 시 인자가 숫자가 아닙니다.")
        except ZeroDivisionError:
            raise RuntimeError("스프라이트의 갯수는 0개가 될 수 없습니다.")

    def __eq__(self, other) -> bool:
        if type(other) != Sprite:
            return false
        if self.__repr__() == other.__repr__():
            return true
        return false

    def __repr__(self) -> str:
        return self.name

    def draw(self, index: int or float, sx, sy, xscale = float(1), yscale = float(1), rot = float(0.0),
             alpha = float(1.0)) -> None:
        dx = 0
        if not self.isSeparate:
            data = self.__data__[0]
            dx = int(self.width * index)
        else:
            data = self.__data__[int(index % self.number)]

        data.opacify(alpha)
        flipmod: str = ""
        if xscale < 0:
            flipmod += "h"
        if yscale < 0:
            flipmod += "v"
        xscale, yscale = abs(xscale), abs(yscale)

        data.clip_composite_draw_angle(dx, 0, self.width, self.height, rot, flipmod, sx, sy, int(self.width * xscale),
                                       int(self.height * yscale))

    def get_handle(self):
        return self.__data__


def sprite_load(filepaths, name = str("default"), xoffset = None, yoffset = None, number = int(1)) -> Sprite:
    global sprite_list
    new = Sprite(filepaths, number, xoffset, yoffset)
    new.name = name
    sprite_list[name] = new
    return new


def sprite_get(name: str) -> Sprite:
    global sprite_list
    try:
        val = sprite_list[name]
    except KeyError as e:
        raise RuntimeError(str(e) + "\n 해당 스프라이트가 존재하지 않습니다!")
    return val


def draw_sprite(spr: Sprite, index = int(0) or float(0), sx = int(0), sy = int(0), xscale = float(1), yscale = float(1), rot = float(0.0), alpha = float(1.0)) -> None:
    spr.draw(index, sx, sy, xscale, yscale, rot, alpha)


def sprite_json_loads():
    try:
        with open(path_data + "sprite.json") as sprfile:
            parsed = json.load(sprfile)

            for content in parsed:
                sprite_load(content["path"], content["name"], content["xoffset"], content["yoffset"], content["number"])

    except FileNotFoundError:
        pass
