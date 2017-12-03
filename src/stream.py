from module import framework

from module.sprite import *
from module.audio import *

"""
        비고:
            1. UI 와 테마 스프라이트 이름 앞에는 s 가 붙는다.
            2. 맵 데이터:
                1. 
            3. 프레임워크:
                1. hFontSml, hFont, hFontLrg 이외의 폰트는 모두 소문자로 쓴다. (e.g. hfontsmall)
            4. 파일 별 설명:
                01. stream.py : 실행부
                02. streams\begin.py : 로고 표시
                03. streams\main.py : 메인 메뉴
                04. streams\game.py : 게임
                05. streams\game_pause.py : 게임 일시 정지
                06. streams\game_over.py : 게임 오버
                07. module\pico2d.py : 수정된 PICO2D 파일
                08. module\keycode.py : 수정된 키코드 파일
                09. module\functions.py : 모든 곳에서 공통적으로 사용하는 함수 모음
                    1. 계산 등
                10. module\constants.py : 모든 곳에서 공통적으로 사용하는 상수 모음
                    1. 전역 상수들 (색, 물리 상수 / 함수 등)
                    2.
                11. module\framework.py : 프레임워크
                    1. 유저 입출력 관리 객체 io
                    2. 카메라 객체 Camera
                    3. 기타 전역 변수들
                12. module\sprite.py : 스프라이트 관리 담당
                13. module\terrain.py : 지형 생성 담당
                14. module\game : 본 게임에 쓰이는 파일 모음
                15. data\map_template.json : 지도 틀
                16. data\option.json : 옵션 파일
                17. data\sprite.json : 불러올 스프라이트 목록 파일
                18. 
                19. 
                20. 
            5. 게임 실행 순서:
                1. stream.py -> framework.py
                2. begin.py
                3. main.py
                4. game.py -> game_executor.py -> game_container.py -> ...
                

        외부 파일 수정 사항:
            1. pico2d.py 의 open_canvas 함수 수정 (창 핸들 반환)
            2. pico2d.py 의 image 클래스 수정 (중심점 설정: xoffset, yoffset), 설정 함수 추가
            3. pico2d.py 의 printfps 함수 실행부 삭제
            4. sdl2.keycode.py 에 __all__ 추가 (확인 바람)
            5. pico2d.py 에 background_color, draw_color 와 그 set, get 메서드 추가
            6. pico2d.py 에 문자 정렬 추가
            7. rect.py 의 생성자에 int 변환 씌움
]
"""

# noinspection PyUnresolvedReferences
if __name__ == "__main__":
    framework.game_begin()
    sprite_json_loads()
    audio_json_loads()

    # from streams import main
    from streams import game
    from streams import begin
    framework.run(game)

    framework.game_end()
