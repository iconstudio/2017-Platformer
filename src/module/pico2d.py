import ctypes
import math
import sys

# noinspection PyUnresolvedReferences
try:
    from sdl2 import *
    from sdl2.sdlimage import *
    from sdl2.sdlttf import *
    from sdl2.sdlmixer import *
    import sdl2.render

    import sdl2.video as video
    import sdl2.keyboard as keyboard
    import sdl2.events as events
    import sdl2.rect as rect
except ImportError:
    print("Error: cannot import pysdl2 - probably not installed")
    sys.exit(-1)  # abort program execution

import module.keycode as keycode
from module.constants import *

window, renderer, debug_font = None, None, None
canvas_width, canvas_height = 0, 0
lattice_on: bool = True
audio_on: bool = False
background_color: SDL_Color = SDL_Color(210, 210, 210)
draw_color: SDL_Color = SDL_Color()
screen_rect = SDL_Rect(0, 0, screen_width, screen_height)
rectangle = None

#   글자 정렬용 변수
# | (halign, valign)               |
# +----------+----------+----------+
# |  (0, 0)  |  (1, 0)  |  (2, 0)  |
# +----------+----------+----------+
# |  (0, 1)  |  (1, 1)  |  (2, 1)  |
# +----------+----------+----------+
# |  (0, 2)  |  (1, 2)  |  (2, 2)  |
# +----------+----------+----------+
halign, valign = 0, 0

__all__ = [
              "clamp", "get_time", "delay", "screen_rect",
              "Event", "Image", "Font", "Font_sprite", "get_events", "load_texture", "load_image", "load_font",
              "open_canvas", "close_canvas", "update_canvas", "clear_canvas", "clear_canvas_now",
              "show_lattice", "hide_lattice", "lattice_on", "audio_on", "show_cursor", "hide_cursor",
              "background_color", "draw_color", "draw_set_color", "draw_get_color", "draw_set_alpha",
              "draw_set_halign", "draw_set_valign",
              "draw_background_color_set",
              "draw_rectangle",
              "load_music", "load_wav",

              "SDL_SetWindowTitle", "SDL_SetWindowIcon", "SDL_Color",
          ] + sdl2.render.__all__ + keyboard.__all__ + events.__all__ + keycode.__all__ + rect.__all__ + video.__all__


def clamp(minimum, val, maximum):
    return max(minimum, min(val, maximum))


def draw_set_color(newr: SDL_Color or int, newg = None, newb = None):
    global renderer, draw_color
    if type(newr) == SDL_Color:
        draw_color = newr
    else:
        if newg is not None and newb is not None:
            draw_color.r, draw_color.g, draw_color.b = newr, newg, newb
    SDL_SetRenderDrawColor(renderer, draw_color.r, draw_color.g, draw_color.b, draw_color.a)


def draw_set_alpha(newa: float):
    global renderer, draw_color
    draw_color.a = int(newa * 255)
    SDL_SetRenderDrawColor(renderer, draw_color.r, draw_color.g, draw_color.b, draw_color.a)


def draw_get_color() -> SDL_Color:
    global draw_color
    return draw_color


def draw_get_alpha() -> float:
    global draw_color
    return draw_color.a / 255


def draw_background_color_set(cr: int, cg: int, cb: int, ca: int = 255):
    global background_color
    background_color.r = cr
    background_color.g = cg
    background_color.b = cb
    background_color.a = ca


# 가로 정렬
def draw_set_halign(arg: int):
    global halign
    halign = arg


# 가로 정렬
def draw_set_valign(arg: int):
    global valign
    valign = arg


def open_canvas(w = int(800), h = int(600), sync = False, full = False):
    global window, renderer
    global canvas_width, canvas_height
    global debug_font
    global audio_on
    global rectangle

    canvas_width, canvas_height = w, h

    # all the initialization needs to be check for working
    SDL_Init(SDL_INIT_EVERYTHING)
    IMG_Init(IMG_INIT_JPG | IMG_INIT_PNG | IMG_INIT_TIF | IMG_INIT_WEBP)
    TTF_Init()

    Mix_Init(MIX_INIT_MP3 | MIX_INIT_OGG)

    ret = Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, MIX_DEFAULT_CHANNELS, 1024)
    if -1 == ret:
        print('WARNING: Audio functions are disabled due to speaker or sound problems')
    else:
        audio_on = True

    if audio_on:
        Mix_Volume(-1, 128)
        Mix_VolumeMusic(128)

    # SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 0);
    caption = ('Pico2D Canvas (' + str(w) + 'x' + str(h) + ')' + ' 1000.0 FPS').encode('UTF-8')
    if full:
        flags = SDL_WINDOW_FULLSCREEN
    else:
        flags = SDL_WINDOW_SHOWN
    # window = SDL_CreateWindow(caption, SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, w, h, flags)
    window = SDL_CreateWindow(caption, SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, w, h,
                              flags | SDL_WINDOW_BORDERLESS)
    if sync:
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
    else:
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

    if renderer is None:
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_SOFTWARE)
    SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND)
    rectangle = load_texture(path_image + "rectangle.png")

    # SDL_ShowCursor(SDL_DISABLE)

    clear_canvas()
    update_canvas()
    clear_canvas()
    update_canvas()

    debug_font_path = path_font + '윤고딕_310.ttf'
    debug_font = load_font(debug_font_path, 16)
    return window


def get_canvas_width():
    return canvas_width


def get_canvas_height():
    return canvas_height


def show_cursor():
    SDL_ShowCursor(SDL_ENABLE)


def hide_cursor():
    SDL_ShowCursor(SDL_DISABLE)


def show_lattice():
    global lattice_on
    lattice_on = True
    clear_canvas()
    update_canvas()


def hide_lattice():
    global lattice_on
    lattice_on = False
    clear_canvas()
    update_canvas()


def clear_canvas():
    global background_color
    SDL_SetRenderDrawColor(renderer, background_color.r, background_color.g, background_color.b, background_color.a)
    SDL_RenderClear(renderer)
    if lattice_on:
        SDL_SetRenderDrawColor(renderer, 180, 180, 180, 255)
        for gx in range(0, canvas_width, 10):
            SDL_RenderDrawLine(renderer, gx, 0, gx, canvas_height)
        for gy in range(canvas_height - 1, 0, -10):
            SDL_RenderDrawLine(renderer, 0, gy, canvas_width, gy)
        SDL_SetRenderDrawColor(renderer, 160, 160, 160, 255)

        for gx in range(0, canvas_width, 100):
            SDL_RenderDrawLine(renderer, gx, 0, gx, canvas_height)
        for gy in range(canvas_height - 1, 0, -100):
            SDL_RenderDrawLine(renderer, 0, gy, canvas_width, gy)
    SDL_SetRenderDrawColor(renderer, draw_color.r, draw_color.g, draw_color.b, draw_color.a)


def clear_canvas_now():
    clear_canvas()
    update_canvas()
    clear_canvas()
    update_canvas()


def update_canvas():
    SDL_RenderPresent(renderer)


def close_canvas():
    if audio_on:
        Mix_HaltMusic()
        Mix_HaltChannel(-1)
        Mix_CloseAudio()
        Mix_Quit()
    TTF_Quit()
    IMG_Quit()
    SDL_DestroyRenderer(renderer)
    SDL_DestroyWindow(window)
    SDL_Quit()


def delay(sec):
    SDL_Delay(int(sec * 1000))


def get_time():
    return SDL_GetTicks() / 1000.0


def make_sdlrect(rx, ry, w, h):
    return SDL_Rect(int(rx), int(-ry + canvas_height - h), int(w), int(h))


def draw_rectangle(x1, y1, x2, y2):
    global renderer, rectangle, draw_color

    drect = SDL_Rect(int(x1), int(-y2 + canvas_height - 1), int(x2 - x1 + 1), int(y2 - y1 + 1))
    trect = SDL_Rect()
    SDL_SetRenderTarget(renderer, rectangle)
    SDL_SetRenderDrawColor(renderer, draw_color.r, draw_color.g, draw_color.b, draw_color.a)
    SDL_RenderFillRect(renderer, drect)
    SDL_RenderCopy(renderer, rectangle, trect, drect)

    del drect, trect


class Event:
    """Pico2D Event Class"""
    key = None
    button = None
    x, y = None, None
    event = None

    def __init__(self, evt_type, evt_subevent = None):
        self.type = evt_type
        self.event = evt_subevent


def get_events():
    # print_fps()
    SDL_Delay(1)
    inner_event = SDL_Event()
    events_return = []
    while SDL_PollEvent(ctypes.byref(inner_event)):
        curr_event = Event(inner_event.type)
        if curr_event.type in (SDL_WINDOWEVENT,):
            curr_event.event = inner_event.window.event
            events_return.append(curr_event)
        if curr_event.type in (
                SDL_QUIT, SDL_KEYDOWN, SDL_KEYUP, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
            events_return.append(curr_event)
            if curr_event.type == SDL_KEYDOWN or curr_event.type == SDL_KEYUP:
                if not inner_event.key.repeat:
                    curr_event.key = inner_event.key.keysym.sym
            elif curr_event.type == SDL_MOUSEMOTION:
                curr_event.x, curr_event.y = inner_event.motion.x, inner_event.motion.y
            elif curr_event.type == SDL_MOUSEBUTTONDOWN or curr_event.type == SDL_MOUSEBUTTONUP:
                curr_event.button, curr_event.x, curr_event.y = inner_event.button.button, inner_event.button.x, inner_event.button.y

    return events_return


class Image:
    """Pico2D Image Class"""
    xoffset: float = 0
    yoffset: float = 0

    def __init__(self, texture, xoff, yoff):
        self.texture = texture
        # http://wiki.libsdl.org/SDL_QueryTexture
        w, h = c_int(), c_int()
        SDL_QueryTexture(self.texture, None, None, ctypes.byref(w), ctypes.byref(h))
        self.w, self.h = w.value, h.value
        self.offset(xoff, yoff)

    def __del__(self):
        SDL_DestroyTexture(self.texture)

    def offset(self, xoff: float, yoff: float):
        if xoff is not None and yoff is not None:
            self.xoffset, self.yoffset = xoff, yoff
        else:
            self.xoffset, self.yoffset = self.w / 2, self.h / 2

    def make_draw_region(self, dx, dy, dw, dh):
        return make_sdlrect(dx - self.xoffset, dy - self.yoffset, dw, dh)

    def make_draw_region_origin(self, dx, dy, dw, dh):
        return make_sdlrect(dx, dy, dw, dh)

    def rotate_draw(self, rad, dx, dy, w = None, h = None):
        """Rotate(in radian unit) and draw image to back buffer, center of rotation is the image center"""
        if w is None and h is None:
            w, h = self.w, self.h
        drect = self.make_draw_region(dx, dy, w, h)
        SDL_RenderCopyEx(renderer, self.texture, None, drect, math.degrees(-rad), None, SDL_FLIP_NONE)

    def composite_draw(self, rad, flip: str, dx, dy, w = None, h = None):
        if w is None and h is None:
            w, h = self.w, self.h
        drect = self.make_draw_region(dx, dy, w, h)
        flip_flag = SDL_FLIP_NONE
        if 'h' in flip:
            flip_flag |= SDL_FLIP_HORIZONTAL
        if 'v' in flip:
            flip_flag |= SDL_FLIP_VERTICAL
        SDL_RenderCopyEx(renderer, self.texture, None, drect, math.degrees(-rad), None, flip_flag)

    def draw(self, dx, dy, w = None, h = None):
        """Draw image to back buffer"""
        if w is None and h is None:
            w, h = self.w, self.h
        drect = self.make_draw_region(dx, dy, w, h)
        SDL_RenderCopy(renderer, self.texture, None, drect)

    def draw_to_origin(self, dx, dy, w = None, h = None):
        """Draw image to back buffer"""
        if w is None and h is None:
            w, h = self.w, self.h
        drect = self.make_draw_region_origin(dx, dy, w, h)
        SDL_RenderCopy(renderer, self.texture, None, drect)

    def clip_draw(self, left, bottom, width, height, dx, dy, w = None, h = None):
        """Clip a rectangle from image and draw"""
        if w is None and h is None:
            w, h = width, height
        src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
        dest_rect = self.make_draw_region(dx, dy, w, h)
        SDL_RenderCopy(renderer, self.texture, src_rect, dest_rect)

    def clip_composite_draw(self, left, bottom, width, height, rad, flip: str, dx, dy, w = None, h = None):
        if w is None and h is None:
            w, h = self.w, self.h
        src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
        dst_rect = self.make_draw_region(dx, dy, w, h)
        flip_flag = SDL_FLIP_NONE
        if 'h' in flip:
            flip_flag |= SDL_FLIP_HORIZONTAL
        if 'v' in flip:
            flip_flag |= SDL_FLIP_VERTICAL
        SDL_RenderCopyEx(renderer, self.texture, src_rect, dst_rect, math.degrees(-rad), None, flip_flag)

    def clip_composite_draw_angle(self, left, bottom, width, height, deg, flip: str, dx, dy, w = None, h = None):
        if w is None and h is None:
            w, h = self.w, self.h
        src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
        dst_rect = self.make_draw_region(dx, dy, w, h)
        flip_flag = SDL_FLIP_NONE
        if 'h' in flip:
            flip_flag |= SDL_FLIP_HORIZONTAL
        if 'v' in flip:
            flip_flag |= SDL_FLIP_VERTICAL
        SDL_RenderCopyEx(renderer, self.texture, src_rect, dst_rect, deg, None, flip_flag)

    def clip_draw_to_origin(self, left, bottom, width, height, dx, dy, w = None, h = None):
        """Clip a rectangle from image and draw"""
        if w is None and h is None:
            w, h = width, height
        src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
        dest_rect = self.make_draw_region_origin(dx, dy, w, h)
        SDL_RenderCopy(renderer, self.texture, src_rect, dest_rect)

    def draw_now(self, dx, dy, w = None, h = None):
        """Draw image to canvas immediately"""
        self.draw(dx, dy, w, h)
        update_canvas()
        self.draw(dx, dy, w, h)
        update_canvas()
        '''
        if w == None and h == None:
            w,h = self.w, self.h
        rect = make_sdlrect(dx-w/2, dy-h/2, w, h)
        SDL_RenderCopy(renderer, self.texture, None, rect);
        SDL_RenderPresent(renderer)
        '''

    def opacify(self, o):
        SDL_SetTextureAlphaMod(self.texture, int(o * 255.0))


def load_texture(name):
    global renderer
    texture = IMG_LoadTexture(renderer, name.encode('UTF-8'))
    SDL_SetTextureBlendMode(texture, SDL_BLENDMODE_BLEND)
    if not texture:
        print('cannot load %s' % name)
        raise IOError
    return texture


def load_image(name, xoff = None, yoff = None):
    texture = load_texture(name)

    image = Image(texture, xoff, yoff)
    return image


class Font:
    def __init__(self, name, size = 20):
        # print('font' + name + 'loaded')
        self.font = TTF_OpenFont(name.encode('utf-8'), size)
        if not self.font:
            print('cannot load %s' % name)
            raise IOError

    def draw(self, dx, dy, caption: str, scale: float = 1.0):
        sdl_color = draw_get_color()
        fsurface = TTF_RenderUTF8_Blended(self.font, caption.encode(), sdl_color)
        texture = SDL_CreateTextureFromSurface(renderer, fsurface)
        SDL_SetTextureBlendMode(texture, SDL_BLENDMODE_BLEND)
        SDL_FreeSurface(fsurface)
        image = Image(texture, None, None)
        image.opacify(sdl_color.a / 255)

        global halign, valign
        hscale, vscale = scale * image.w, scale * image.h
        image.draw(dx - hscale * (halign - 1) / 2, dy + vscale * (valign - 1) / 2, int(hscale), int(vscale))


class Font_sprite:
    sprite_index = None
    char_list = {}
    height = 0

    def __init__(self, sprite, data: str):
        length = len(data)
        if length > 0:
            for i in range(length):
                currchr = data[i]
                self.char_list[currchr] = i
            self.sprite_index = sprite
            self.height = sprite.height

    def draw(self, sx, sy, caption: str, scale: float = 1.0):
        length = len(caption)
        if length > 0:
            dx, dy = sx, sy - scale * self.height * (caption.count('\n'))
            for i in range(length):
                currchr = caption[i].upper()
                if currchr in (" ", ' '):
                    # print(currchr + " - ")
                    dx += 16 * scale
                    continue
                elif currchr is '\n':
                    dx = sx
                    dy -= self.height * scale
                    continue
                else:
                    currind: int = self.char_list[currchr]
                    # print(currchr + " - " + str(currind))
                    global halign, valign
                    hscale, vscale = scale * self.sprite_index.width, scale * self.sprite_index.height
                    self.sprite_index.draw(currind, dx - hscale * (halign - 1) / 2, dy + hscale * (valign - 1) / 2,
                                           scale, scale, 0, draw_get_alpha())
                    dx += 16 * scale


def load_font(name, size = 20):
    font = Font(name, size)
    return font


cur_time = 0.0


def print_fps():
    global window
    global cur_time
    global canvas_width, canvas_height
    dt = get_time() - cur_time
    cur_time += dt
    dt = max(dt, 0.0001)
    caption = (
        'Pico2D Canvas (' + str(canvas_width) + 'x' + str(canvas_height) + ')' + ' %4.2f FPS' % (1.0 / dt)).encode(
        'UTF-8')
    SDL_SetWindowTitle(window, caption)


def debug_print(caption):
    global canvas_height
    global debug_font
    debug_font.draw(0, canvas_height - 10, caption, (0, 255, 0))


# only one music can exist at one time
class Music:
    def __init__(self, data):
        self.music = data

    def repeat_play(self):
        Mix_PlayMusic(self.music, -1)

    def play(self, n = 1):
        Mix_PlayMusic(self.music, n)

    @staticmethod
    def set_volume(v):
        Mix_VolumeMusic(v)

    @staticmethod
    def get_volume():
        return Mix_VolumeMusic(-1)

    @staticmethod
    def stop():
        Mix_HaltMusic()

    @staticmethod
    def pause():
        Mix_PauseMusic()

    @staticmethod
    def resume():
        Mix_ResumeMusic()

    def __del__(self):
        Mix_FreeMusic(self.music)


class Wav:
    def __init__(self, data):
        self.wav = data

    def repeat_play(self):
        Mix_PlayChannel(-1, self.wav, -1)

    def play(self, n = 1):
        Mix_PlayChannel(-1, self.wav, n - 1)

    def set_volume(self, v):
        Mix_VolumeChunk(self.wav, v)

    def get_volume(self):
        return Mix_VolumeChunk(self.wav, -1)

    def __del__(self):
        Mix_FreeChunk(self.wav)


def load_music(name):
    if audio_on:
        data = Mix_LoadMUS(name.encode('UTF-8'))
        if not data:
            print('cannot load %s' % name)
            raise IOError

        return Music(data)
    else:
        print('audio fuctions cannot work due to sound or speaker problems')
        raise IOError


def load_wav(name):
    if audio_on:
        data = Mix_LoadWAV(name.encode('UTF-8'))
        if not data:
            print('cannot load %s' % name)
            raise IOError

        return Wav(data)
    else:
        print('audio functions cannot work due to sound or speaker problems')
        raise IOError


# for pytmx
import pytmx


def pico2d_image_loader(filename, colorkey, **kwargs):
    def extract_image(crect = None, flags = None):
        if crect:
            try:
                flip = ''
                if flags.flipped_horizontally:
                    flip = 'h'
                if flags.flipped_vertically:
                    flip = 'v'
                if flags.flipped_diagonally:
                    flip = 'hv'

                return image, crect, flip

            except ValueError:
                print('Tile bounds outside bounds of tileset image')
                raise
        else:
            return image, None, ''

    image = load_image(filename)

    if colorkey:
        print('color key deprecated')

    return extract_image


def load_tilemap(filename):
    return pytmx.TiledMap(filename, image_loader = pico2d_image_loader)


def test_pico2d():
    pass


def main():
    pass


print("Pico2d is prepared.")
if __name__ == "__main__":
    test_pico2d()
