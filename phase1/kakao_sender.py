"""
클립보드를 통해 한글 깨짐 없이 PC 카카오톡 특정 방에 메시지를 전송한다.
pyautogui의 typewrite는 한글을 지원하지 않으므로 pyperclip 복사 + Ctrl+V 방식만 사용한다.
"""

import time

import pyperclip
from pywinauto import Application
from pywinauto.keyboard import send_keys


def send_kakao_message(room_title: str, text: str, retry: int = 3) -> bool:
    if not room_title:
        print("[kakao_sender] TARGET_KAKAO_ROOM이 설정되지 않았습니다.")
        return False

    for attempt in range(1, retry + 1):
        try:
            app = Application(backend="uia").connect(title=room_title)
            win = app.window(title=room_title)
            win.set_focus()
            time.sleep(0.3)

            pyperclip.copy(text)
            edit_ctrl = win.child_window(control_type="Edit")
            edit_ctrl.set_focus()
            send_keys("^v")
            time.sleep(0.2)
            send_keys("{ENTER}")
            return True
        except Exception as e:
            print(f"[kakao_sender] {attempt}회차 전송 실패 ({room_title}): {e}")
            time.sleep(1)

    return False
