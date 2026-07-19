import os

from dotenv import load_dotenv

load_dotenv()

COUPANG_STORAGE_STATE_PATH = os.getenv("COUPANG_STORAGE_STATE_PATH", "storage_state.json")

SOURCE_KAKAO_ROOMS = [r.strip() for r in os.getenv("SOURCE_KAKAO_ROOMS", "").split(",") if r.strip()]
TARGET_KAKAO_ROOM = os.getenv("TARGET_KAKAO_ROOM", "")

POLL_INTERVAL_SEC = int(os.getenv("POLL_INTERVAL_SEC", "30"))
