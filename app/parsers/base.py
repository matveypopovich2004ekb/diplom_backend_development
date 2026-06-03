from dataclasses import dataclass


@dataclass()
class ProductOffer:
    supplier: str
    product_name: str
    price: float | None | str
    price_raw: str | None
    package_quantity: str | None | int
    package_quantity_raw: str | None
    url: str | None














