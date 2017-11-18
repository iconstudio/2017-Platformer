from module.pico2d import *
from module.constants import *

__all__ = [
    "GameState", "change_state", "push_state", "pop_state", "quit", "run",
    "io", "Camera", "game_begin", "game_end", "HWND", "current_time", "game_realtime",
    "scene_width", "scene_height", "scene_set_size"
]

HWND = None
keylogger_list = []
scene_width = screen_width
scene_height = screen_height


def game_begin():
    global HWND
    HWND = open_canvas(screen_width, screen_height)
    SDL_SetWindowTitle(HWND, "Vampire Exodus".encode("UTF-8"))
    # icon = load_texture(path_image + "icon.png")
    # SDL_SetWindowIcon(hwnd, icon)
    # SDL_SetWindowSize(hwnd, screen_width * screen_scale, screen_height * screen_scale)
    # SDL_SetWindowFullscreen(self.hwnd, ctypes.c_uint32(1))
    hide_cursor()
    hide_lattice()
    draw_background_color_set(0, 0, 0)


def game_end():
    close_canvas()


def scene_set_size(w = scene_width, h = scene_height):
    global scene_width, scene_height
    scene_width = w
    scene_height = h


# Object : IO procedure
class oIOProc:
    key_list = []
    # This dictionary contains only the Node of keyboard.
    key_map = {}
    # list of checking obj.
    checker_list = {}

    class iochecker:
        code = None
        life = 2
        owner = None

        def __init__(self, nowner, key: SDL_Keycode):
            self.owner = nowner
            self.code = key

        def __del__(self):
            self.owner.timer = None
            try:
                global keylogger_list
                keylogger_list.remove(self)
            except ValueError:
                pass
            except AttributeError:
                pass

        def event_step(self):
            if self.life == 0:
                self.owner.check_pressed = false
                del self
            else:
                self.life -= 1

    class ionode:
        code = None
        timer = None
        check: bool = false
        check_pressed: bool = false

        def __init__(self, key: SDL_Keycode):
            self.code = key

        def enter(self):
            self.check = true
            self.check_pressed = true

            if self.timer is None:
                global io
                self.timer = io.iochecker(self, self.code)
                io.checker_list[self.code] = self.timer

                global keylogger_list
                keylogger_list.append(self.timer)

        def close(self):
            self.check = false
            self.check_pressed = false

            if self.timer is not None:
                del self.timer
                self.timer = None

    def key_add(self, key: SDL_Keycode):
        newnode = self.ionode(key)
        self.key_map[key] = newnode
        self.key_list.append(key)
        return newnode

    def key_check(self, key: SDL_Keycode) -> bool:
        try:
            return (self.key_map[key]).check
        except KeyError:
            return false

    def key_check_pressed(self, key: SDL_Keycode) -> bool:
        try:
            return (self.key_map[key]).check_pressed
        except KeyError:
            return false

    def proceed(self, kevent):
        try:
            node = self.key_map[kevent.key]

            if kevent.type == SDL_KEYDOWN:
                node.enter()
            elif kevent.type == SDL_KEYUP:
                node.close()
        except KeyError:
            return

    def clear(self):
        if len(self.key_list) > 0:
            for codes in self.key_list:
                node = self.key_map[codes]
                node.close()


def keyboard_update():
    global keylogger_list
    klen = len(keylogger_list)
    if klen > 0:
        for checker in keylogger_list:
            checker.event_step()


io = oIOProc()


# Object : View Camera
class oCamera:
    x: float = 0
    y: float = 0
    lock: bool = false
    width, height = screen_width, screen_height

    def limit(self):
        global screen_width, screen_height, scene_width, scene_height
        self.x = clamp(0, self.x, scene_width - screen_width)
        self.y = clamp(20, self.y, scene_height - screen_height)

    def set_pos(self, x: float = None, y: float = None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.limit()

    def add_pos(self, x: float = None, y: float = None):
        if x is not None:
            self.x += x
        if y is not None:
            self.y += y
        self.limit()


Camera = oCamera()


class GameState:
    def __init__(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.pause = state.pause
        self.resume = state.resume
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw


running = None
stack = None
current_time: float = 0.0
game_realtime: float = 0.0
paused = false


def get_frame_time():
    global current_time, game_realtime, paused

    frame_time = get_time() - current_time
    current_time += frame_time
    if not paused:
        game_realtime += frame_time
    return frame_time


def change_state(state):
    global stack
    pop_state()
    stack.append(state)
    state.enter()
    io.clear()


def push_state(state):
    # close_canvas()

    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(state)
    print(": " + state.name + " begins")
    state.enter()
    io.clear()


def pop_state():
    global stack
    if len(stack) > 0:
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()

    # execute resume function of the previous state
    if len(stack) > 0:
        stack[-1].resume()
    io.clear()


def quit():
    global running
    running = False


def pause():
    global paused
    paused = true


def unpause():
    global paused
    paused = false


def run(start_state):
    global running, stack, io, current_time
    running = True

    stack = [start_state]
    start_state.enter()
    current_time = get_time()
    while running:
        ftime = get_frame_time()
        keyboard_update()
        stack[-1].handle_events(ftime)
        stack[-1].update(ftime)
        stack[-1].draw(ftime)
    # repeatedly delete the top of the stack
    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()
