from module.pico2d import *
from module.constants import *

import sdl2.keyboard as keyboard

__all__ = [
              "GameState", "change_state", "push_state", "pop_state", "quit", "run",
              "io", "Camera",
          ] + keyboard.__all__

keylogger_list = []


# Object : IO procedure
class oIOProc:
    # This dictionary contains only the Node of keyboard.
    key_list = {}
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
            if self.timer == None:
                global io
                self.timer = io.iochecker(self, self.code)
                io.checker_list[self.code] = self.timer
                
                global keylogger_list
                keylogger_list.append(self.timer)
        
        def close(self):
            if self.timer != None:
                del self.timer
                self.timer = None
    
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
                node.enter()
            elif kevent.type == SDL_KEYUP:
                node.check = false
                node.check_pressed = false
                node.close()
        except KeyError:
            return
 
    def clear(self):
        pass


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
    width, height = screen_width, screen_height
    
    def set_pos(self, x: float = None, y: float = None):
        if not x.__eq__(None):
            self.x = x
        if not y.__eq__(None):
            self.y = y
    
    def add_pos(self, x: float = None, y: float = None):
        if not x.__eq__(None):
            self.x += x
        if not y.__eq__(None):
            self.y += y


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


def change_state(state):
    global stack
    pop_state()
    stack.append(state)
    state.enter()


def push_state(state):
    #close_canvas()
    
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
    global running, stack, io
    running = True
    stack = [start_state]
    start_state.enter()
    while running:
        keyboard_update()
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
    # repeatedly delete the top of the stack
    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()
