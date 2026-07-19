from dataclasses import dataclass


@dataclass
class Product:
    name: str
    original_url: str
    price: int
    partners_url: str = ""
