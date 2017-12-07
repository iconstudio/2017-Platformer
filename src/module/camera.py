from module.pico2d import *
from module.functions import *
from module.constants import *

__all__ = [
    "Camera", "scene_set_size", "scene_get_width", "scene_get_height"
]

scene_width = screen_width
scene_height = screen_height


def scene_set_size(w = screen_width, h = screen_height):
    global scene_width, scene_height
    scene_width = w
    scene_height = h


def scene_get_width():
    global scene_width
    return scene_width


def scene_get_height():
    global scene_height
    return scene_height


# Object : View Camera
class oCamera:
    x: float = 0
    y: float = 0
    target_object = None
    lock: bool = false

    def set_taget(self, arg):
        self.target_object = arg

    def limit(self):
        global scene_width, scene_height
        self.x = clamp(0, int(self.x), scene_width - get_screen_width())
        self.y = clamp(20, int(self.y), scene_height - get_screen_height() + 40)

    def set_pos(self, nx: float = None, ny: float = None):
        if nx is not None:
            if abs(nx - self.x) < 2:
                self.x = nx
            elif self.x != nx:
                self.x += (nx - self.x) / 5
        if ny is not None:
            self.y = ny
        self.limit()

    def add_pos(self, ax: float = None, ay: float = None):
        if ax is not None:
            self.x += ax
        if ay is not None:
            self.y += ay
        self.limit()

    def event_step(self):
        if self.target_object is not None and self.target_object.visible:
            self.set_pos(self.target_object.x - get_screen_width() / 2, self.target_object.y - get_screen_height() / 2)


Camera = oCamera()
