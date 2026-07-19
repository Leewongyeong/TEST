from phase1.models import Product


def manual_input_product() -> Product:
    """크롤링/카톡 파싱이 실패했을 때 수동으로 상품 정보를 입력받는다."""
    name = input("상품명: ").strip()
    original_url = input("쿠팡 원본 URL: ").strip()
    price_raw = input("가격(숫자만, 예: 29900): ").strip()
    price = int(price_raw.replace(",", "")) if price_raw else 0
    return Product(name=name, original_url=original_url, price=price)
