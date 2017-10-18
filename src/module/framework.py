from pico2d import *

__all__ = [
    "GameState", "change_state", "push_state", "pop_state", "quit", "run"
]

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
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(state)
    state.enter()

def pop_state():
    global stack
    if (len(stack) > 0):
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()

    # execute resume function of the previous state
    if (len(stack) > 0):
        stack[-1].resume()

def quit():
    global running
    running = False

def run(start_state):
    global running, stack
    running = True
    stack = [start_state]
    start_state.enter()
    while (running):
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].exit()
        stack.pop()
