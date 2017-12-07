from module.pico2d import *
from module.functions import *
from module.constants import *

import module.framework as framework
from stages import game
from stages.game_executor import stage_clear, stage_get_number

__all__ = [
    "name", "enter", "exit", "update", "handle_events", "draw", "pause", "resume"
]

# ==================================================================================================
#                                       프레임워크 함수
# ==================================================================================================
name = "stagecomplete_state"
alpha: float = 0
dmode = 0
tpush: float = 0


# noinspection PyGlobalUndefined
def enter():
    global alpha, dmode, tpush
    alpha = 0
    dmode = 0
    tpush = 0


def exit():
    pass


def update(frame_time):
    global alpha, dmode, tpush
    if dmode == 0:
        if tpush < 2:
            alpha = bezier4(tpush / 2, 0.21, 0.61, 0.35, 1)
            tpush += frame_time
        else:
            alpha = 1
            tpush = 5
            dmode = 1


def draw(frame_time):
    global alpha
    clear_canvas()
    draw_set_alpha(alpha)
    draw_set_color(0, 0, 0)
    draw_rectangle(0, 0, screen_width, screen_height)
    # add tiles

    ui_left = 20
    ui_bot = screen_height - 180
    ui_width = screen_width - ui_left * 2
    ui_height = screen_height - ui_bot - 10
    draw_set_color(255, 255, 255)
    draw_rectangle_sized(ui_left - 10, ui_bot - 10, ui_width + 20, ui_height + 20)
    draw_set_color(0, 0, 0)
    draw_rectangle_sized(ui_left, ui_bot, ui_width, ui_height)
    draw_set_halign(2)
    draw_set_valign(1)
    framework.draw_text("Press X to continue", screen_width - 10, ui_bot - 20)
    draw_set_halign(0)
    framework.draw_text("Stage %d Complete!" % (stage_get_number() + 1), 20, ui_bot - 60, scale = 1.5)
    update_canvas()


def handle_events(frame_time):
    global tpush

    bevents = get_events()
    for event in bevents:
        if event.type == SDL_QUIT or (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            framework.quit()
        elif tpush > 1.2:
            if (event.type, event.key) == (SDL_KEYDOWN, ord('x')):
                framework.change_state(game)


def pause():
    pass


def resume():
    pass
