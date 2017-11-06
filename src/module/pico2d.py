import sys
import types
import ctypes
import math
import json
import os

from sdl2 import *
from sdl2.sdlimage import *
from sdl2.sdlttf import *
from sdl2.sdlmixer import *
import sdl2.render

import sdl2.keyboard as keyboard
import module.keycode as keycode
import sdl2.events as events
import sdl2.rect as rect
from module.constants import *

lattice_on: bool = True
audio_on: bool = False
background_color: SDL_Color = SDL_Color(210, 210, 210)
draw_color: SDL_Color = SDL_Color()

__all__ = [
              "clamp", "get_time", "open_canvas", "close_canvas", "update_canvas", "clear_canvas", "clear_canvas_now",
              "show_lattice", "hide_lattice", "hide_cursor", "delay", "background_color", "draw_color", "audio_on",
              "draw_set_color", "draw_get_color", "draw_background_color_set",
              "get_events", "load_texture", "load_image", "load_font", "load_music", "load_wav",
              "Event", "Image", "Font",
              "SDL_SetWindowTitle", "SDL_SetWindowIcon", "SDL_Color",
          ] + sdl2.render.__all__ + keyboard.__all__ + events.__all__ + keycode.__all__ + rect.__all__


def draw_set_color(newa: SDL_Color or int, newb = None, newc = None):
    global draw_color
    if type(newa) == SDL_Color:
        draw_color = newa
    else:
        if newb != None and newc != None:
            del draw_color
            draw_color = SDL_Color(newa, newb, newc)


def draw_get_color():
    global draw_color
    return draw_color


def draw_background_color_set(r: int, g: int, b: int, a: int = 255):
    global background_color
    background_color.r = r
    background_color.g = g
    background_color.b = b
    background_color.a = a


def open_canvas(w = int(800), h = int(600), sync = False):
    global window, renderer
    global canvas_width, canvas_height
    global debug_font
    global audio_on

    canvas_width, canvas_height = w, h

    # all the initialization needs to be check for working
    SDL_Init(SDL_INIT_EVERYTHING)
    IMG_Init(IMG_INIT_JPG | IMG_INIT_PNG | IMG_INIT_TIF | IMG_INIT_WEBP)
    TTF_Init()

    Mix_Init(MIX_INIT_MP3 | MIX_INIT_OGG)

    ret = Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, MIX_DEFAULT_CHANNELS, 1024)
    if -1 == ret:
        print('WARNING: Audio functions are disabled due to speaker or sound problems')

    if audio_on:
        Mix_Volume(-1, 128)
        Mix_VolumeMusic(128)

    # SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 0);
    caption = ('Pico2D Canvas (' + str(w) + 'x' + str(h) + ')' + ' 1000.0 FPS').encode('UTF-8')
    # window = SDL_CreateWindow(caption, SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, w, h, SDL_WINDOW_SHOWN)
    window = SDL_CreateWindow(caption, SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, w, h, SDL_WINDOW_SHOWN)
    if sync:
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
    else:
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)
    # SDL_ShowCursor(SDL_DISABLE)

    clear_canvas()
    update_canvas()
    clear_canvas()
    update_canvas()
    debug_font = load_font('ConsolaMalgun.TTF', 16)
    draw_set_color(c_white)

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


def update_canvas():
    SDL_RenderPresent(renderer)


def clear_canvas():
    global background_color
    SDL_SetRenderDrawColor(renderer, background_color.r, background_color.g, background_color.b, background_color.a)
    SDL_RenderClear(renderer)
    if lattice_on:
        SDL_SetRenderDrawColor(renderer, 180, 180, 180, 255)
        for x in range(0, canvas_width, 10):
            SDL_RenderDrawLine(renderer, x, 0, x, canvas_height)
        for y in range(canvas_height - 1, 0, -10):
            SDL_RenderDrawLine(renderer, 0, y, canvas_width, y)
        SDL_SetRenderDrawColor(renderer, 160, 160, 160, 255)

        for x in range(0, canvas_width, 100):
            SDL_RenderDrawLine(renderer, x, 0, x, canvas_height)
        for y in range(canvas_height - 1, 0, -100):
            SDL_RenderDrawLine(renderer, 0, y, canvas_width, y)


def clear_canvas_now():
    clear_canvas()
    update_canvas()
    clear_canvas()
    update_canvas()


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


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def delay(sec):
    SDL_Delay(int(sec * 1000))


def get_time():
    return SDL_GetTicks() / 1000.0


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


def debug_print(str):
    global canvas_height
    global debug_font
    debug_font.draw(0, canvas_height - 10, str)


def to_sdl_rect(x, y, w, h):
    return SDL_Rect(int(x), int(-y + canvas_height - h), int(w), int(h))


def draw_rectangle(x1, y1, x2, y2):
    SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)
    rect = SDL_Rect(int(x1), int(-y2 + canvas_height - 1), int(x2 - x1 + 1), int(y2 - y1 + 1))
    SDL_RenderDrawRect(renderer, rect)


class Event:
    """Pico2D Event Class"""

    def __init__(self, evt_type):
        self.type = evt_type
        self.key = None
        self.button = None
        self.x = None
        self.y = None


def get_events():
    # print_fps()
    SDL_Delay(1)
    sdl_event = SDL_Event()
    events = []
    while SDL_PollEvent(ctypes.byref(sdl_event)):
        event = Event(sdl_event.type)
        if event.type in (SDL_QUIT, SDL_KEYDOWN, SDL_KEYUP, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
            events.append(event)
            if event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
                if not sdl_event.key.repeat:
                    event.key = sdl_event.key.keysym.sym
            elif event.type == SDL_MOUSEMOTION:
                event.x, event.y = sdl_event.motion.x, sdl_event.motion.y
            elif event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_MOUSEBUTTONUP:
                event.button, event.x, event.y = sdl_event.button.button, sdl_event.button.x, sdl_event.button.y

    return events


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
        if xoff != None and yoff != None:
            self.xoffset, self.yoffset = xoff, yoff
        else:
            self.xoffset, self.yoffset = self.w / 2, self.h / 2

    def rotate_draw(self, rad, x, y, w = None, h = None):
        """Rotate(in radian unit) and draw image to back buffer"""
        if w == None and h == None:
            w, h = self.w, self.h
        rect = to_sdl_rect(x - self.xoffset, y - self.yoffset, w, h)
        SDL_RenderCopyEx(renderer, self.texture, None, rect, math.degrees(-rad), None, SDL_FLIP_NONE);

    def draw(self, x, y, w = None, h = None):
        """Draw image to back buffer"""
        if w == None and h == None:
            w, h = self.w, self.h
        rect = to_sdl_rect(x - self.xoffset, y - self.yoffset, w, h)
        SDL_RenderCopy(renderer, self.texture, None, rect)

    def draw_to_origin(self, x, y, w = None, h = None):
        """Draw image to back buffer"""
        if w == None and h == None:
            w, h = self.w, self.h
        rect = to_sdl_rect(x, y, w, h)
        SDL_RenderCopy(renderer, self.texture, None, rect)

    def clip_draw(self, left, bottom, width, height, x, y, w = None, h = None):
        """Clip a rectangle from image and draw"""
        if w == None and h == None:
            w, h = width, height
        src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
        dest_rect = to_sdl_rect(x - int(self.xoffset), y - int(self.yoffset), w, h)
        SDL_RenderCopy(renderer, self.texture, src_rect, dest_rect)

    def clip_draw_to_origin(self, left, bottom, width, height, x, y, w = None, h = None):
        """Clip a rectangle from image and draw"""
        if w == None and h == None:
            w, h = width, height
        src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
        dest_rect = to_sdl_rect(x, y, w, h)
        SDL_RenderCopy(renderer, self.texture, src_rect, dest_rect)

    def draw_now(self, x, y, w = None, h = None):
        """Draw image to canvas immediately"""
        self.draw(x, y, w, h)
        update_canvas()
        self.draw(x, y, w, h)
        update_canvas()
        '''
        if w == None and h == None:
            w,h = self.w, self.h
        rect = to_sdl_rect(x-w/2, y-h/2, w, h)
        SDL_RenderCopy(renderer, self.texture, None, rect);
        SDL_RenderPresent(renderer)
        '''

    def opacify(self, o):
        SDL_SetTextureAlphaMod(self.texture, int(o * 255.0))


def load_texture(name):
    global renderer
    texture = IMG_LoadTexture(renderer, name.encode('UTF-8'))
    if (not texture):
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

    def draw(self, x, y, str):
        global draw_color
        # print(str)
        surface = TTF_RenderText_Blended(self.font, str.encode('utf-8'), draw_color)
        texture = SDL_CreateTextureFromSurface(renderer, surface)
        SDL_FreeSurface(surface)
        image = Image(texture, None, None)
        image.draw(x + image.w / 2, y)

    # unicode rendering not working well at the moment, needs to modify
    def draw_unicode(self, x, y, str):
        global draw_color
        surface = TTF_RenderUNICODE_Blended(self.font,
                                            ctypes.cast(str.encode('utf-16'), ctypes.POINTER(ctypes.c_uint16)),
                                            draw_color)
        texture = SDL_CreateTextureFromSurface(renderer, surface)
        SDL_FreeSurface(surface)
        image = Image(texture)
        image.draw(x + image.w / 2, y)


def load_font(name, size = 20):
    font = Font(name, size)
    return font


# only one music can exist at one time
class Music:
    def __init__(self, data):
        self.music = data

    def repeat_play(self):
        Mix_PlayMusic(self.music, -1)

    def play(self, n = 1):
        Mix_PlayMusic(self.music, n)

    def set_volume(self, v):
        Mix_VolumeMusic(v)

    def get_volume(self):
        return Mix_VolumeMusic(-1)

    def stop(self):
        Mix_HaltMusic()

    def pause(self):
        Mix_PauseMusic()

    def resume(self):
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
        if (not data):
            print('cannot load %s' % name)
            raise IOError

        return Music(data)
    else:
        print('audio fuctions cannot work due to sound or speaker problems')
        raise IOError


def load_wav(name):
    if audio_on:
        data = Mix_LoadWAV(name.encode('UTF-8'))
        if (not data):
            print('cannot load %s' % name)
            raise IOError

        return Wav(data)
    else:
        print('audio fuctions cannot work due to sound or speaker problems')
        raise IOError


def test_pico2d():
    print('testing pico2d')
    print('done')


print("Pico2d is prepared.")
if __name__ == "__main__":
    test_pico2d()
