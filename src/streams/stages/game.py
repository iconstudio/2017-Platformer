from module.pico2d import *

import stages.game_executor as stages
from module.audio import *

__all__ = [
    "name", "draw_clean", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "game_state"


stages.stage_init()


def enter():
    stages.stage_create()


def exit():
    audio_stream_stop()


def update(frame_time):
    stages.game_update(frame_time)


def draw_clean(frame_time):
    stages.game_draw(frame_time)


def draw(frame_time):
    clear_canvas()
    draw_clean(frame_time)
    update_canvas()


def handle_events(frame_time):
    stages.game_handle_events(frame_time)


def pause():
    pass


def resume():
    pass
