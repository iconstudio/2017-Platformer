from sdl2.pixels import SDL_Color

__all__ = [
    "false", "true", "screen_width", "screen_height", "screen_scale",
    "path_resource", "path_image", "path_font", "path_theme", "path_entity", "path_background", "path_ui", "path_map",
    "path_effect", "path_data",
    "fps_target", "phy_mess", "phy_velocity", "phy_gravity",
    "c_white", "c_ltgray", "c_gray", "c_dkgray", "c_black", "c_red", "c_green", "c_blue", "c_lime",
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
phy_velocity = (((1000.0 / 60.0) / 60.0) * phy_mess)
phy_gravity = phy_velocity * 100

path_resource = "..\\res\\"
path_image = path_resource + "img\\"
path_font = path_resource + "font\\"
path_theme = path_image + "theme\\"
path_entity = path_image + "entity\\"
path_effect = path_image + "effect\\"
path_background = path_image + "bg\\"
path_ui = path_image + "ui\\"
path_map = path_resource + "maps\\"
path_data = "..\\data\\"


# Colors
# 흑백
c_white = SDL_Color(255, 255, 255)
c_ltgray = SDL_Color(192, 192, 192)
c_gray = SDL_Color(128, 128, 128)
c_dkgray = SDL_Color(64, 64, 64)
c_black = SDL_Color(0, 0, 0)

# 적녹청
c_red = SDL_Color(255, 0, 0)
c_lime = SDL_Color(0, 255, 0)
c_green = SDL_Color(0, 128, 0)
c_blue = SDL_Color(0, 0, 255)

# 어두운 적녹청
c_maroon = SDL_Color(128, 0, 0)
c_dkrose = SDL_Color(64, 0, 0)
c_dkgreen = SDL_Color(0, 64, 0)
c_ultramarine = SDL_Color(0, 0, 128)
c_navy = SDL_Color(0, 0, 96)

# 적녹청 혼합
c_yellow = SDL_Color(255, 255, 0)
c_fuchsia = SDL_Color(255, 0, 255)
c_aqua = SDL_Color(0, 255, 255)

# 적녹청 + 어두운 적녹청 혼합
c_orange = SDL_Color(255, 128, 0)
c_cyan = SDL_Color(0, 128, 255)
c_magenta = SDL_Color(255, 0, 128)
c_purple = SDL_Color(128, 0, 255)
c_teal = SDL_Color(0, 255, 128)
