from pico2d import *

import game_executor as game_manager
from audio import *

__all__ = [
    "name", "draw_clean", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "game_state"


game_manager.stage_init()


def enter():
    game_manager.stage_create()


def exit():
    audio_stream_stop()


def update(frame_time):
    game_manager.game_update(frame_time)


def draw_clean(frame_time):
    game_manager.game_draw(frame_time)


def draw(frame_time):
    clear_canvas()
    draw_clean(frame_time)
    update_canvas()


def handle_events(frame_time):
    game_manager.game_handle_events(frame_time)


def pause():
    pass


def resume():
    pass
