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
    sx: float = 0
    sy: float = 0
    width, height = screen_width, screen_height
    width_scene, height_scene = screen_width, screen_height
    target_object = None
    lock: bool = false

    shake_rot = 0
    shake = 0

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
        self.x = clamp(0, int(self.x), self.width_scene - self.width) + self.sx
        self.y = clamp(0, int(self.y), self.height_scene - self.height + 10) + self.sy

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

    def screen_shake(self, value):
        self.shake = max(self.shake, value)
        self.shake_rot = irandom(360)

    def event_step(self):
        if self.shake != 0 and self.shake > 0.02:
            self.sx = math.cos(degtorad(self.shake_rot)) * self.shake
            self.sy = math.sin(degtorad(self.shake_rot)) * self.shake

            self.shake_rot = (self.shake_rot + 50 + irandom(140)) % 360
            self.shake -= self.shake / 12
        else:
            self.sx, self.sy = 0, 0
            self.shake = 0


Camera = oCamera()
