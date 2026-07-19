"""
최초 1회 실행: 쿠팡 파트너스에 수동으로 로그인(캡차 포함)한 뒤
세션을 storage_state.json으로 저장한다. rpa_link.py는 이 파일을 재사용해
매번 로그인하지 않고 세션을 유지한다.

    python -m phase1.login_setup
"""

from playwright.sync_api import sync_playwright

from phase1 import config


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://partners.coupang.com/")
        input("브라우저에서 로그인(캡차 포함)을 완료한 뒤 이 창으로 돌아와 Enter를 누르세요...")
        context.storage_state(path=config.COUPANG_STORAGE_STATE_PATH)
        browser.close()
        print(f"세션 저장 완료: {config.COUPANG_STORAGE_STATE_PATH}")


if __name__ == "__main__":
    main()
