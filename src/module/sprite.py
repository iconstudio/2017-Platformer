from pico2d import *
from functions import *

__all__ = [
    "Sprite",
    "sprite_list",
    "sprite_load", "sprite_get", "draw_sprite"
]

sprite_list: dict = {}  # 스프라이트는 이름으로 구분된다.


# Object : Sprites
class Sprite(object):
    number: int = 0
    width, height = 0, 0
    isSummed: bool = false

    def __init__(self, filepath:list or str, number, xoffset=None, yoffset=None):
        """
            이미지 불러오기, 이미지 분할, 리스트화 작업
            :param filepath:
            :param number:
        """
        if type(filepath) == list:
            self.isSummed = true
            self.number = len(filepath)

            try:
                if self.number > 0:
                    self.__data__ = []
                    for specpath in filepath:
                        img = load_image(specpath)
                        if xoffset != None and yoffset != None:
                            img.offset(xoffset, yoffset)
                        self.__data__.append(img)
                    self.width = int(self.__data__[0].w)
                    self.height = int(self.__data__[0].h)
            except IndexError:
                raise RuntimeError("스프라이트 목록아 비어있습니다!")
        else:  # load only an image, so dosent need spliting one image.
            self.__data__ = load_image(filepath)
            self.number = number  # the number of sprite in an image
            # size of each index
            self.width = int(self.__data__.w / number)
            self.height = int(self.__data__.h)

        try:
            tempTy = type(number)
            if tempTy != int and tempTy != float:
                raise RuntimeError("스프라이트 불러오기 시 인자가 숫자가 아닙니다.")
        except ZeroDivisionError:
            raise RuntimeError("스프라이트의 갯수는 0개가 될 수 없습니다.")

    def draw(self, index:int or float, x, y, xscale=float(1), yscale=float(1), rot=float(0.0), alpha=float(1.0)) -> None:
        dx = 0
        if not self.isSummed:
            data = self.__data__
            dx = int(self.width * index)
        else:
            data = self.__data__[int(index)]
        data.opacify(alpha)

        if rot != 0.0:  # pico2d does not support clipping + rotating draw.
            data.rotate_draw(rot, x, y, int(self.width * xscale), int(self.height * yscale))
        else:
            data.clip_draw(dx, 0, self.width, self.height, x, y,
                           int(self.width * xscale), int(self.height * yscale))

    def get_handle(self):
        return self.__data__


def sprite_load(filepaths, name=str("default"), xoffset=None, yoffset=None, number=int(1)) -> Sprite:
    global sprite_list
    new = Sprite(filepaths, number, xoffset, yoffset)
    sprite_list[name] = new
    return new


def sprite_get(name: str) -> Sprite:
    global sprite_list
    return sprite_list[name]


def draw_sprite(spr: Sprite, index=int(0) or float(0), x=int(0), y=int(0), xscale=float(1), yscale=float(1),
                rot=float(0.0), alpha=float(1.0)) -> None:
    spr.draw(index, x, y, xscale, yscale, rot, alpha)
