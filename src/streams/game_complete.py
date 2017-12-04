from module.pico2d import *
from module.functions import *
from module.constants import *

import module.framework as framework
from streams import game
from module.game.game_executor import stage_get_number, manager_delete, stage_create

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
    global alpha, tpush
    alpha = 0
    tpush = 0


def exit():
    pass


def update(frame_time):
    global alpha, dmode, tpush
    if dmode == 0:
        if tpush < 5:
            alpha = bezier4(tpush / 5, 0.21, 0.61, 0.35, 1)
            tpush += frame_time
        else:
            alpha = 1
            tpush = 5
            dmode = 1
    elif dmode == 1:
        if tpush > 0:
            alpha = 0.2 + bezier4(1 - tpush / 5, .77, 0, .47, 0)
            tpush -= frame_time
        else:
            alpha = 0.2
            tpush = 0


def draw(frame_time):
    global alpha
    clear_canvas()
    game.draw_clean(frame_time)
    draw_set_alpha(alpha)
    draw_set_color(0, 0, 0)
    draw_set_alpha(1)
    draw_rectangle(0, 0, screen_width, screen_height)
    draw_set_halign(0)
    draw_set_valign(1)
    framework.draw_text("Stage %d Complete!" % (stage_get_number() + 1), 20, 60, scale = 2)
    update_canvas()


def handle_events(frame_time):
    bevents = get_events()
    for event in bevents:
        if event.type == SDL_QUIT or (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, ord('x')):
                #framework.change_state(game)
                framework.pop_state()
                manager_delete()
                stage_create()


def pause():
    pass


def resume():
    pass
