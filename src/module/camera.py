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
    width_scene, height_scene = screen_width, screen_height
    target_object = None
    lock: bool = false

    def set_taget(self, arg):
        self.target_object = arg

    def set_size(self, w = screen_width, h = screen_height):
        self.width = w
        self.height = h

    def set_scene_size(self, w = screen_width, h = screen_height):
        self.width_scene = w
        self.height_scene = h

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_scene_width(self):
        return self.width_scene

    def get_scene_height(self):
        return self.height_scene

    def get_bbox(self) -> tuple:
        return int(self.x), int(self.y), self.width, self.height

    def limit(self):
        self.x = clamp(0, int(self.x), self.width_scene - self.width)
        self.y = clamp(0, int(self.y), self.height_scene - self.height + 40)

    def set_pos(self, nx: float = None, ny: float = None):
        if nx is not None:
            dx = nx - self.width / 2
            if abs(dx - self.x) < 2:
                self.x = dx
            elif self.x != dx:
                self.x += (dx - self.x) / 5
        if ny is not None:
            dy = ny - self.height / 2
            self.y = dy
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
