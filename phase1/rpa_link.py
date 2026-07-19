"""
Playwright로 쿠팡 파트너스 로그인 세션(storage_state.json)을 재사용해
'간편 링크 만들기' 폼에 원본 URL을 입력하고 생성된 단축 링크를 가져온다.

selector는 쿠팡 파트너스 '간편 링크 만들기' 페이지(Ant Design 기반)의 실제 값으로 맞춰져 있다.
- URL 입력: id="url"
- 링크 생성 버튼: 텍스트 "링크 생성"
- 결과 링크: class "tracking-url-input"
페이지가 개편되면 가장 먼저 깨지는 부분이므로, 동작하지 않으면 이 파일의 selector부터 점검한다.
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
        page.wait_for_selector("#url")
        page.fill("#url", original_url)
        page.click('button:has-text("링크 생성")')

        # 결과 영역(.tracking-url-input)이 새 단축 링크로 채워질 때까지 대기한다.
        # 이전 값이 남아있을 수 있으므로 link.coupang.com 이 나타나는지 확인한다.
        page.wait_for_function(
            """() => {
                const el = document.querySelector('.tracking-url-input');
                return el && el.textContent.includes('link.coupang.com');
            }"""
        )
        short_link = page.inner_text(".tracking-url-input").strip()

        context.storage_state(path=storage_state_path)
        browser.close()
        return short_link
