from pico2d import *
from functions import *

import framework
#import begin
import game

"""
        수정 사항:
            1. pico2d.py 의 open_canvas 함수 수정 (창 핸들 반환)
            2. pico2d.py 의 image 클래스 수정 (중심점 설정: xoffset, yoffset), 설정 함수 추가
            3. pico2d.py 의 printfps 함수 실행부 삭제
"""

hwnd = open_canvas(screen_width, screen_height, true)
SDL_SetWindowTitle(hwnd, "Vampire Exodus".encode("UTF-8"))
#icon = load_texture(path_image + "icon.png")
#SDL_SetWindowIcon(hwnd, icon)
# SDL_SetWindowSize(hwnd, screen_width * screen_scale, screen_height * screen_scale)
# SDL_SetWindowFullscreen(self.hwnd, ctypes.c_uint32(1))
hide_cursor()
hide_lattice()
framework.run(game)
close_canvas()
