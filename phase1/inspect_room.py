"""
카카오톡 방 창의 내부 컨트롤 구조를 파일로 뽑아내는 진단 도구.

사용법:
  1. 대상 카톡방을 열어둔다.
  2. python -m phase1.inspect_room
  3. 방 이름을 입력한다.
  4. 같은 폴더에 생기는 'kakao_tree.txt' 파일을 개발자에게 전달한다.
"""

from collections import Counter

from pywinauto import Desktop

OUT_FILE = "kakao_tree.txt"


def main() -> None:
    room = input("카톡방 이름을 입력하세요 (창 제목과 동일하게): ").strip()
    if not room:
        print("방 이름이 비어있습니다.")
        return

    print(f"\n'{room}' 창 구조를 분석하는 중...\n")

    try:
        win = Desktop(backend="uia").window(title=room)
        win.wait("exists", timeout=5)
    except Exception as e:
        print(f"[실패] 창을 찾지 못했습니다: {e}")
        return

    type_counter: Counter = Counter()
    text_samples = []
    lines = []

    for el in win.descendants():
        try:
            ct = el.element_info.control_type
            cls = el.element_info.class_name
            name = el.window_text()
        except Exception as e:
            lines.append(f"(읽기 오류: {e})")
            continue

        type_counter[ct] += 1
        lines.append(f"[{ct}] class={cls!r} name={name!r}")
        if ct in ("Text", "Edit", "Document") and name.strip():
            text_samples.append((ct, name.strip()))

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 카톡방: {room}\n")
        f.write(f"# 전체 컨트롤 개수: {len(lines)}\n\n")
        f.write("## 컨트롤 종류별 개수\n")
        for ct, cnt in type_counter.most_common():
            f.write(f"  {ct}: {cnt}\n")
        f.write("\n## 전체 컨트롤 목록\n")
        f.write("\n".join(lines))

    print(f"[완료] '{OUT_FILE}' 파일이 생성되었습니다.")
    print(f"       전체 컨트롤 {len(lines)}개\n")
    print("컨트롤 종류별 개수:")
    for ct, cnt in type_counter.most_common():
        print(f"  {ct}: {cnt}")

    print("\n글자가 들어있는 컨트롤 미리보기 (최근 20개):")
    for ct, txt in text_samples[-20:]:
        preview = txt[:60].replace("\n", " ")
        print(f"  [{ct}] {preview}")

    print(f"\n=> 생성된 '{OUT_FILE}' 파일을 개발자에게 전달하세요.")


if __name__ == "__main__":
    main()
