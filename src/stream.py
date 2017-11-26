from module.constants import *

from module import framework

from module.sprite import *

"""
        비고:
            1. UI 와 테마 스프라이트 이름 앞에는 s 가 붙는다.
            2. 맵 데이터:
                1. 숫자는 지형이다. (숫자만 지형은 아니다)
                2. @ 는 플레이어이다.
                3.
            3. 프레임워크:
                1. hFontSml, hFont, hFontLrg 이외의 외부 폰트는 모두 소문자로 쓴다. (e.g. hfontsmall)

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

    # UI
    sprite_load(path_image + "logo.png", "sLogo", None, None)
    sprite_load(path_ui + "loading.png", "sLoading", None, None)
    sprite_load(path_ui + "heart.png", "sHeart", 16, 16)

    # Background
    sprite_load(path_background + "bgCastle.png", "bgCastle", 0, 0)
    sprite_load(path_background + "bgCave.png", "bgCave", 0, 0)
    sprite_load(path_background + "bgTemple.png", "bgTemple", 0, 0)
    sprite_load(path_background + "bgNight_0.png", "bgNight", 0, 0)

    # Theme
    sprite_load([path_theme + "wood_0.png", path_theme + "wood_1.png", path_theme + "wood_2.png",
                 path_theme + "wood_3.png"], "sWood", 0, 0)
    sprite_load([path_theme + "stonewall_0.png", path_theme + "stonewall_1.png", path_theme + "stonewall_2.png"],
                "sStonewall", 0, 0)

    sprite_load([path_theme + "brick_castle_0.png", path_theme + "brick_castle_1.png",
                 path_theme + "brick_castle_2.png", path_theme + "brick_castle_3.png"], "sCastleBrick", 0, 0)
    sprite_load([path_theme + "lush_0.png", path_theme + "lush_1.png"], "sLush", 0, 0)
    sprite_load([path_theme + "lush_down_0.png", path_theme + "lush_up_0.png", path_theme + "lush_updown_0.png"],
                "sLushDirectional", 0, 0)
    sprite_load([path_theme + "brick_mine_0.png", path_theme + "brick_mine_1.png"], "sDirtBrick", 0, 0)
    sprite_load([path_theme + "brick_mine_down_0.png", path_theme + "brick_mine_up_0.png",
                 path_theme + "brick_mine_updown_0.png"], "sDirtBrickDirectional", 0, 0)
    sprite_load([path_theme + "grave_0.png", path_theme + "grave_1.png", path_theme + "grave_2.png",
                 path_theme + "grave_3.png", path_theme + "grave_4.png", path_theme + "grave_5.png"],
                "Grave", 0, 0)
    sprite_load(path_theme + "grave_ash_0.png", "GraveAsh", 0, 0)

    sprite_load(path_theme + "elevator_0.png", "Elevator", 0, 0)

    # Doodads
    sprite_load(path_theme + "ladder_0.png", "Ladder", 0, 0)
    sprite_load([path_theme + "TikiTorch_0.png", path_theme + "TikiTorch_1.png", path_theme + "TikiTorch_2.png",
                 path_theme + "TikiTorch_3.png", path_theme + "TikiTorch_4.png", path_theme + "TikiTorch_1.png"],
                "sTorch", 8, 32)
    sprite_load([path_theme + "lush_top_0.png", path_theme + "lush_top_1.png", path_theme + "lush_top_2.png"],
                "sLushDoodad", 0, 0)
    sprite_load(path_theme + "flat_0.png", "FlatTop", 0, 0)

    # Entity
    sprite_load(path_entity + "vampire.png", "Player", 8, 8)
    sprite_load(path_entity + "VampireJump_0.png", "PlayerJump", 8, 8)
    sprite_load([path_entity + "VampireRun_0.png", path_entity + "VampireRun_1.png",
                 path_entity + "VampireRun_2.png", path_entity + "VampireRun_3.png",
                 path_entity + "VampireRun_4.png", path_entity + "VampireRun_5.png",
                 path_entity + "VampireRun_2.png", path_entity + "VampireRun_1.png"], "PlayerRun", 8, 8)
    sprite_load(path_entity + "VampireDead_0.png", "PlayerDead", 8, 8)
    sprite_load(path_entity + "Soldier.png", "SoldierIdle", 8, 8)
    sprite_load([path_entity + "SolidierWalk_0.png", path_entity + "SolidierWalk_1.png",
                 path_entity + "SolidierWalk_2.png", path_entity + "SolidierWalk_3.png",
                 path_entity + "SolidierWalk_4.png", path_entity + "SolidierWalk_5.png",
                 path_entity + "SolidierWalk_2.png", path_entity + "SolidierWalk_1.png"], "SoldierRun", 8, 8)

    sprite_load([path_entity + "SoldierStunned_0.png", path_entity + "SoldierStunned_1.png",
                 path_entity + "SoldierStunned_2.png", path_entity + "SoldierStunned_3.png",
                 path_entity + "SoldierStunned_4.png"], "SoldierStunned", 8, 8)
    sprite_load(path_entity + "SoldierDead.png", "SoldierDead", 8, 8)

    sprite_load(path_entity + "ManBeard_0.png", "ManBeardIdle", 8, 8)
    sprite_load([path_entity + "ManBeardWalk_0.png", path_entity + "ManBeardWalk_1.png",
                 path_entity + "ManBeardWalk_2.png", path_entity + "ManBeardWalk_3.png",
                 path_entity + "ManBeardWalk_4.png", path_entity + "ManBeardWalk_5.png",
                 path_entity + "ManBeardWalk_2.png", path_entity + "ManBeardWalk_1.png"], "ManBeardRun", 8, 8)

    sprite_load(path_entity + "Snake_0.png", "SnakeIdle", 8, 8)
    sprite_load([path_entity + "SnakeWalk_0.png", path_entity + "SnakeWalk_1.png",
                 path_entity + "SnakeWalk_2.png", path_entity + "SnakeWalk_3.png",
                 path_entity + "SnakeWalk_4.png", path_entity + "SnakeWalk_5.png"], "SnakeRun", 8, 8)
    sprite_load(path_entity + "Cobra_0.png", "CobraIdle", 8, 8)
    sprite_load([path_entity + "CobraWalk_0.png", path_entity + "CobraWalk_1.png",
                 path_entity + "CobraWalk_2.png", path_entity + "CobraWalk_3.png",
                 path_entity + "CobraWalk_4.png", path_entity + "CobraWalk_5.png"], "CobraRun", 8, 8)

    # Effect
    sprite_load([path_entity + "Blood_0.png", path_entity + "Blood_1.png",
                 path_entity + "Blood_2.png", path_entity + "Blood_2.png"], "Bloods", 4, 4)
    sprite_load([path_entity + "BloodTrail_0.png", path_entity + "BloodTrail_1.png",
                 path_entity + "BloodTrail_2.png", path_entity + "BloodTrail_3.png",
                 path_entity + "BloodTrail_4.png", path_entity + "BloodTrail_5.png",
                 path_entity + "BloodTrail_6.png"], "BloodTrails", 4, 4)
    sprite_load([path_effect + "stunned_0.png", path_effect + "stunned_1.png",
                 path_effect + "stunned_2.png", path_effect + "stunned_3.png", path_effect + "stunned_4.png"], "Stun",
                8, 8)

    from streams import main
    from streams import game
    from streams import begin

    framework.run(game)
    framework.game_end()
