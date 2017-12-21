from module.pico2d import *
from module.functions import *
from module.constants import *

__all__ = [
    "player_got_damage", "player_lives_clear", "player_get_lives", "container_player",
    "player_ability_get_status", "player_ability_activate", "PLAYER_AB_DOUBLEJUMP",
    "PLAYER_AB_SPIKESHOES", "PLAYER_AB_SPRINSHOES", "PLAYER_AB_DASH",
    "timer_get", "timer_set_all", "timer_clear", "timer_increase",
    "killcount_get", "killcount_increase", "kill_local", "killcount_get", "killcount_increase", "killcount_clear"
]

player_lives = 3
container_player = None


def player_got_damage(how: int):
    global player_lives
    player_lives -= how


def player_lives_clear(how: int = 3):
    global player_lives
    player_lives = how


def player_get_lives() -> int:
    global player_lives
    return player_lives


player_ability = {}
PLAYER_AB_DOUBLEJUMP = "DoubleJump"  # 더블 점프
PLAYER_AB_SPIKESHOES = "SpikeShoes"  # 밟기 피해량 증가
PLAYER_AB_SPRINSHOES = "SprinShoes"  # 높이 점프
PLAYER_AB_DASH = "Dash"  # 고속 이동
player_ability[PLAYER_AB_DOUBLEJUMP] = false
player_ability[PLAYER_AB_SPIKESHOES] = false
player_ability[PLAYER_AB_SPRINSHOES] = false
player_ability[PLAYER_AB_DASH] = false


def player_ability_get_status(what: str) -> bool:
    global player_ability
    try:
        return player_ability[what]
    except KeyError:
        return false


def player_ability_activate(what: str) -> None:
    global player_ability
    player_ability[what] = true


kill_local = 0  # Count of killed enemy
kill_total = 0
time_local = 0  # a Timer of current stage
time_total = 0


# Killing count be treated with methods
def killcount_get() -> (int, int):
    global kill_local, kill_total
    return kill_local, kill_total


def killcount_increase():
    global kill_local, kill_total
    kill_local += 1
    kill_total += 1


def killcount_clear():
    global kill_local
    kill_local = 0


def timer_get() -> (int, int):
    global time_local, time_total
    return time_local, time_total


def timer_set_all(arg):
    global time_local, time_total
    time_local = arg
    time_total = arg


def timer_increase(frame_time):
    global time_local, time_total
    time_local += frame_time
    time_total += frame_time


def timer_clear():
    global time_local
    time_local = 0
