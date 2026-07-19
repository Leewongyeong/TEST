"""
카카오톡 방 읽기가 가능한지 확인하는 테스트 스크립트.

사용법:
  1. 읽고 싶은 카카오톡 방을 화면에 열어둔다.
  2. 아래 명령을 실행한다.

      python -m phase1.test_reader

  3. 방 이름을 물어보면 카톡 창 제목과 똑같이 입력한다.
  4. 글자들이 쭉 나오면 성공, 아무것도 안 나오면 읽기 불가.
"""

from phase1.kakao_reader import _read_room_messages, parse_hotdeal_message


def main() -> None:
    print("=" * 50)
    print(" 카카오톡 방 읽기 테스트")
    print("=" * 50)
    room = input("\n읽을 카톡방 이름을 입력하세요 (카톡 창 제목과 동일하게): ").strip()

    if not room:
        print("방 이름이 비어있습니다. 다시 실행해 주세요.")
        return

    print(f"\n'{room}' 방을 읽는 중...\n")

    try:
        messages = _read_room_messages(room)
    except Exception as e:
        print("[실패] 방을 찾지 못했거나 읽는 중 오류가 발생했습니다.")
        print(f"       오류 내용: {e}")
        print("\n확인할 점:")
        print("  - 카톡방 이름이 창 제목과 정확히 같은가요? (띄어쓰기 포함)")
        print("  - 해당 카톡방 창이 열려 있나요?")
        return

    print(f"[결과] 읽어온 텍스트 조각: {len(messages)}개\n")

    if not messages:
        print("아무 텍스트도 읽지 못했습니다.")
        print("=> 이 방은 UI 자동화로 메시지를 읽을 수 없습니다.")
        print("   (수동 입력 모드 사용을 권장합니다.)")
        return

    print("-" * 50)
    for i, msg in enumerate(messages[-30:], 1):  # 최근 30개만 미리보기
        print(f"{i:>3}. {msg}")
    print("-" * 50)

    # 쿠팡 링크가 들어있는 메시지가 몇 개나 인식되는지 확인
    parsed = [parse_hotdeal_message(m) for m in messages]
    hotdeals = [p for p in parsed if p]

    print(f"\n쿠팡 링크가 인식된 항목: {len(hotdeals)}개")
    for p in hotdeals[:10]:
        print(f"  - {p['name']} | {p['price']:,}원 | {p['original_url']}")

    print("\n=> 위에 상품/링크가 제대로 보이면 읽기 성공입니다!")


if __name__ == "__main__":
    main()
