# 쿠팡 파트너스 자동화 - Phase 1

API 발급 전(누적 실적 15만 원 달성 전) 단계용 반자동화 파이프라인.

## 실행 환경

Phase 1은 **Windows PC + PC 카카오톡 앱**이 실제로 켜져 있어야 동작한다
(`pywinauto`, `pyautogui`가 실제 Windows GUI 세션을 제어하기 때문).
리눅스/클라우드 환경에서는 코드 작성·정적 검토만 가능하고 실행/디버깅은
Windows PC에서 진행해야 한다.

## 설치

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
copy .env.example .env
```

`.env`에 다음 값을 채운다.

- `SOURCE_KAKAO_ROOMS`: 핫딜을 읽어올 카카오톡 방 이름 2개 (쉼표 구분, PC 카톡 창 제목과 정확히 일치해야 함)
- `TARGET_KAKAO_ROOM`: 발송할 본인 운영 오픈채팅방 이름

## 최초 1회: 쿠팡 파트너스 로그인 세션 저장

```bash
python -m phase1.login_setup
```

브라우저 창이 뜨면 직접 로그인(캡차 포함)하고, 완료 후 터미널에서 Enter를 누른다.
이후 `phase1/rpa_link.py`는 저장된 세션(`storage_state.json`)을 재사용하므로
매번 로그인/캡차를 다시 겪지 않는다.

## 실행

```bash
python -m phase1.main_phase1
```

- 모드 1: `SOURCE_KAKAO_ROOMS`에 설정한 카톡방을 주기적으로 읽어 새 핫딜(쿠팡 링크가 포함된 메시지)을 자동 처리
- 모드 2: 크롤링/파싱이 안 될 때 터미널에서 상품명·URL·가격을 직접 입력

## 알려진 한계 및 유지보수 포인트

1. **pywinauto 컨트롤 트리는 카카오톡 버전에 따라 달라질 수 있다.**
   `kakao_reader.py`, `kakao_sender.py`의 `child_window(control_type=...)` 검색이
   실패하면 Windows SDK의 `inspect.exe`로 실제 컨트롤 트리를 확인해 이름을 맞춘다.
2. **`rpa_link.py`의 selector는 자리표시자다.** 쿠팡 파트너스 '간편 링크 만들기'
   페이지의 실제 input/button selector를 브라우저 개발자도구로 확인 후 교체해야 한다.
3. **캡차(CAPTCHA) 대처**: Phase 1은 완전 자동 로그인을 시도하지 않는다.
   `login_setup.py`를 `headless=False`로 열어 사람이 직접 캡차를 풀고, 세션만
   저장해 재사용하는 구조로 우회한다. 세션이 만료되면 `login_setup.py`를 다시 실행한다.
4. 카톡방 자동 발송/소싱은 쿠팡 파트너스 및 카카오 이용약관상 매크로 사용 제한과
   충돌할 수 있으니, 본인 계정 정지 리스크를 감안해 사용 빈도를 조절할 것.
