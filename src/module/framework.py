import sdl2.keyboard as keyboard
from module.pico2d import *

__all__ = [
    "GameState", "change_state", "push_state", "pop_state", "quit", "run",
	"io",
] + keyboard.__all__


# Object : IO procedure
class oIOProc:
    checking = {}
    class iochecker:
        code = None
        gravity = 0
        life = 3
        owner = None

        def __init__(self, nowner, key: SDL_Keycode):
            self.owner = nowner
            self.code = key

        def event_step(self):
            if self.life <= 0:
                global io
                io.checking[self.code] = None
                self.owner.check_pressed = false
                del self
            else:
                self.life -= 1

    class ionode:
        code = None
        check: bool = false
        check_pressed: bool = false

        def __init__(self, key: SDL_Keycode):
            self.code = key

    # This dictionary contains only the Codes of keyboard.
    key_list = {}

    def key_add(self, key: SDL_Keycode):
        newnode = self.ionode(key)
        self.key_list[key] = newnode
        return newnode

    def key_check(self, key: SDL_Keycode) -> bool:
        try:
            return (self.key_list[key]).check
        except KeyError:
            return false

    def key_check_pressed(self, key: SDL_Keycode) -> bool:
        try:
            return (self.key_list[key]).check_pressed
        except KeyError:
            return false

    def proceed(self, kevent):
        try:
            node = self.key_list[kevent.key]

            if kevent.type == SDL_KEYDOWN:
                node.check = true
                node.check_pressed = true
                if self.checking[node.code] == None:
                    self.checking[node.code] = self.iochecker(node, node.code)
                # print(true)
            elif kevent.type == SDL_KEYUP:
                node.check = false
                node.check_pressed = false
                # print(false)
        except KeyError:
            return

io = oIOProc()

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


def change_state(state):
    global stack
    pop_state()
    stack.append(state)
    state.enter()


def push_state(state):
    close_canvas()

    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(state)
    print(": " + state.name + " begins")
    state.enter()


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


def quit():
    global running
    running = False


def run(start_state):
    global running, stack
    running = True
    stack = [start_state]
    start_state.enter()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        
    # repeatedly delete the top of the stack
    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()
