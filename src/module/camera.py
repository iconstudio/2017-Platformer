from module.pico2d import *
from module.functions import *
from module.constants import *

__all__ = [
    "Camera"
]


# Object : View Camera
class oCamera:
    x: float = 0
    y: float = 0
    width, height = screen_width, screen_height
    target_object = None
    lock: bool = false

    def set_taget(self, arg):
        self.target_object = arg

    def set_size(self, w = screen_width, h = screen_height):
        self.width = w
        self.height = h

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def limit(self):
        self.x = clamp(0, int(self.x), self.width - get_screen_width())
        self.y = clamp(00, int(self.y), self.height - get_screen_height() + 20)

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
        # if self.target_object is not None:
        #    self.set_pos(self.target_object.x - get_screen_width() / 2,
        #                 self.target_object.y - get_screen_height() / 2)
        pass


Camera = oCamera()
