"""
Playwright로 쿠팡 파트너스 로그인 세션(storage_state.json)을 재사용해
'간편 링크 만들기' 폼에 원본 URL을 입력하고 생성된 단축 링크를 가져온다.

주의: 아래 selector(input[name="url"] 등)는 실제 파트너스 페이지 구조를
Chrome 개발자도구로 확인한 뒤 맞춰야 하는 자리표시자다. 페이지 개편 시
가장 먼저 깨지는 부분이므로, 동작하지 않으면 이 파일의 selector부터 점검한다.
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

from phase1 import config

PARTNERS_LINK_PAGE = "https://partners.coupang.com/#affiliate/ws/link/generate"


def create_partners_link(original_url: str, headless: bool = True) -> str:
    storage_state_path = config.COUPANG_STORAGE_STATE_PATH
    if not Path(storage_state_path).exists():
        raise RuntimeError(
            "저장된 로그인 세션이 없습니다. 먼저 `python -m phase1.login_setup`을 실행하세요."
        )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(storage_state=storage_state_path)
        page = context.new_page()

        page.goto(PARTNERS_LINK_PAGE)
        page.fill('input[name="url"]', original_url)
        page.click('button:has-text("링크 생성")')
        page.wait_for_selector(".generated-link-result")
        short_link = page.inner_text(".generated-link-result").strip()

        context.storage_state(path=storage_state_path)
        browser.close()
        return short_link
