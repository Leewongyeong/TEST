"""
쿠팡 핫딜 카카오톡 오픈채팅방(소싱용) 메시지를 읽어 상품 정보를 추출한다.

주의: PC 카카오톡의 UI Automation 트리 구조는 버전에 따라 바뀔 수 있다.
child_window 검색이 실패하면 Windows의 inspect.exe(Windows SDK 포함)로
실제 컨트롤 트리를 확인해 control_type/class_name을 맞춰야 한다.
"""

import json
import re
from pathlib import Path

from pywinauto import Desktop

COUPANG_URL_PATTERN = re.compile(
    r"(https?://(?:www\.coupang\.com/vp/products/\d+[^\s]*|link\.coupang\.com/[^\s]+|coupa\.ng/[^\s]+))"
)
PRICE_PATTERN = re.compile(r"(\d{1,3}(?:,\d{3})+|\d{4,})\s*원")

STATE_FILE = Path(__file__).parent / "kakao_seen_state.json"


def _load_seen_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def _save_seen_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_room_messages(room_title: str) -> list[str]:
    win = Desktop(backend="uia").window(title=room_title, class_name="EVA_Window")
    win.set_focus()
    list_ctrl = win.child_window(control_type="List")
    items = list_ctrl.children(control_type="ListItem")
    return [item.window_text() for item in items if item.window_text().strip()]


def parse_hotdeal_message(text: str) -> dict | None:
    url_match = COUPANG_URL_PATTERN.search(text)
    if not url_match:
        return None
    price_match = PRICE_PATTERN.search(text)
    price = int(price_match.group(1).replace(",", "")) if price_match else 0
    name_line = text.strip().split("\n")[0].strip()
    return {"name": name_line[:80], "original_url": url_match.group(1), "price": price}


def poll_new_hotdeals(room_titles: list[str]) -> list[dict]:
    """각 방에서 마지막으로 읽은 이후 새로 올라온 메시지만 파싱해 반환한다."""
    state = _load_seen_state()
    new_products = []

    for room in room_titles:
        try:
            messages = _read_room_messages(room)
        except Exception as e:
            print(f"[kakao_reader] '{room}' 방 읽기 실패: {e}")
            continue

        seen_count = state.get(room, 0)
        for msg in messages[seen_count:]:
            parsed = parse_hotdeal_message(msg)
            if parsed:
                new_products.append(parsed)
        state[room] = len(messages)

    _save_seen_state(state)
    return new_products
