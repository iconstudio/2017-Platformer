import sdl2.pixels as px

__all__ = [
    "false", "true", "screen_width", "screen_height", "screen_scale",
    "path_resource", "path_image", "path_font", "path_theme", "path_entity", "path_background",
    "fps_target", "phy_mess", "phy_velocity",
    "c_white", "c_black"
]

# Global : Constants
false = False
true = True
fps_target = 60.0

# Physics
screen_width: int = 640
screen_height: int = 360
screen_scale: int = 1

# Physics Ratio
# 10 픽셀 == 1 미터
phy_mess = 10.0 / 1
phy_velocity = 1000.0 / (fps_target * fps_target) * phy_mess

path_resource = "..\\res\\"
path_image = path_resource + "img\\"
path_font = path_resource + "font\\"
path_theme = path_image + "theme\\"
path_entity = path_image + "entity\\"
path_background = path_image + "bg\\"

# Colors
c_white = px.SDL_Color(255, 255, 255)
c_black = px.SDL_Color(0, 0, 0)
