from module.pico2d import *

from stages.game_executor import *

__all__ = [
    "name", "draw_clean", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "game_state"


def enter():
    stage_create()


def exit():
    pass


def update(frame_time):
    game_update(frame_time)


def draw_clean(frame_time):
    game_draw(frame_time)


def draw(frame_time):
    clear_canvas()
    draw_clean(frame_time)
    update_canvas()


def handle_events(frame_time):
    game_handle_events(frame_time)


def pause():
    pass


def resume():
    pass
