import sdl2.pixels as px

__all__ = [
    "false", "true", "screen_width", "screen_height", "screen_scale",
    "path_resource", "path_image", "path_font", "path_theme", "path_entity", "path_background",
    "c_white",
]

# Global : Constants
false = False
true = True
screen_width: int = 640
screen_height: int = 360
screen_scale: int = 1

path_resource = "..\\res\\"
path_image = path_resource + "img\\"
path_font = path_resource + "font\\"
path_theme = path_image + "theme\\"
path_entity = path_image + "entity\\"
path_background = path_image + "bg\\"

# Colors
c_white = px.SDL_Color(255, 255, 255)
