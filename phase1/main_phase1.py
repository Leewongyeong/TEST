"""
Phase 1 실행 진입점.

    python -m phase1.main_phase1

사전 준비:
  1. `python -m phase1.login_setup` 로 쿠팡 파트너스 로그인 세션 저장
  2. .env 에 SOURCE_KAKAO_ROOMS / TARGET_KAKAO_ROOM 설정
"""

import time

from phase1 import config
from phase1.cli_input import manual_input_product
from phase1.kakao_reader import poll_new_hotdeals
from phase1.kakao_sender import send_kakao_message
from phase1.message_templates import build_kakao_message, build_thread_message
from phase1.models import Product
from phase1.rpa_link import create_partners_link


def process_product(product: Product) -> None:
    product.partners_url = create_partners_link(product.original_url)

    kakao_msg = build_kakao_message(product)
    thread_msg = build_thread_message(product)

    print("\n=== 스레드용 메시지 (수동 게시) ===")
    print(thread_msg)

    sent = send_kakao_message(config.TARGET_KAKAO_ROOM, kakao_msg)
    print("카톡 발송 성공" if sent else "카톡 발송 실패 - 수동 확인 필요")


def run_auto_mode() -> None:
    if not config.SOURCE_KAKAO_ROOMS:
        print("SOURCE_KAKAO_ROOMS가 설정되지 않았습니다. .env를 확인하세요.")
        return

    print(f"카톡방 모니터링 시작 ({', '.join(config.SOURCE_KAKAO_ROOMS)}) - Ctrl+C로 종료")
    while True:
        for raw in poll_new_hotdeals(config.SOURCE_KAKAO_ROOMS):
            process_product(Product(**raw))
        time.sleep(config.POLL_INTERVAL_SEC)


def run_manual_mode() -> None:
    process_product(manual_input_product())


if __name__ == "__main__":
    mode = input("모드 선택 (1: 카톡방 자동 모니터링, 2: 수동 입력): ").strip()
    if mode == "2":
        run_manual_mode()
    else:
        run_auto_mode()
