from module.pico2d import *
from module.functions import *
from module.constants import *

from module import framework
from streams import begin
from streams import game

from module.sprite import *

"""
        수정 사항:
            1. pico2d.py 의 open_canvas 함수 수정 (창 핸들 반환)
            2. pico2d.py 의 image 클래스 수정 (중심점 설정: xoffset, yoffset), 설정 함수 추가
            3. pico2d.py 의 printfps 함수 실행부 삭제
            4. sdl2.keycode.py 에 __all__ 추가 (확인 바람)
            5. pico2d.py 에 background_color, draw_color 와 그 set, get 메서드 추가
            6. pico2d.py 에 문자 정렬 추가
            7. rect.py 의 생성자에 int 변환 씌움
]
"""

if __name__ == "__main__":
    framework.game_begin()

    # Background
    sprite_load(path_background + "bgCastle.png", "bgCastle", 0, 0)
    sprite_load(path_background + "bgCave.png", "bgCave", 0, 0)
    sprite_load(path_background + "bgTemple.png", "bgTemple", 0, 0)

    # Theme
    sprite_load(
        [path_theme + "brick_castle_0.png", path_theme + "brick_castle_1.png", path_theme + "brick_castle_2.png",
         path_theme + "brick_castle_3.png"], "sCastleBrick", 0, 0)

    # Entity
    sprite_load(path_entity + "vampire.png", "Player", 8, 8)
    sprite_load(path_entity + "VampireJump_0.png", "PlayerJump", 8, 8)
    sprite_load([path_entity + "VampireRun_0.png", path_entity + "VampireRun_1.png",
                 path_entity + "VampireRun_2.png", path_entity + "VampireRun_3.png",
                 path_entity + "VampireRun_4.png", path_entity + "VampireRun_5.png",
                 path_entity + "VampireRun_2.png", path_entity + "VampireRun_1.png"], "PlayerRun", 8, 8)
    sprite_load(path_entity + "VampireDead_0.png", "PlayerDead", 8, 8)
    sprite_load(path_entity + "SolidierWalk_2.png", "SoldierIdle", 8, 8)
    sprite_load([path_entity + "SolidierWalk_0.png", path_entity + "SolidierWalk_1.png",
                 path_entity + "SolidierWalk_2.png", path_entity + "SolidierWalk_3.png",
                 path_entity + "SolidierWalk_4.png", path_entity + "SolidierWalk_5.png",
                 path_entity + "SolidierWalk_2.png", path_entity + "SolidierWalk_1.png"], "SoldierRun", 8, 8)

    framework.run(game)
    framework.game_end()
