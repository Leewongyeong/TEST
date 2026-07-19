from phase1.models import Product

DISCLOSURE = "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."


def build_kakao_message(product: Product) -> str:
    return (
        f"🛰 핫딜 실시간 캐치\n"
        f"🚨 {product.name}\n"
        f"🔻 {product.price:,}원\n"
        f"🔗 {product.partners_url}\n\n"
        f"{DISCLOSURE}"
    )


def build_thread_message(product: Product) -> str:
    return (
        f"{product.name} 지금 {product.price:,}원임 ㄷㄷ\n"
        f"이 가격 오래 안 갈 듯\n"
        f"실시간 최저가 링크는 프로필 카톡방 참조"
    )
