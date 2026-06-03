import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.parsers.base import ProductOffer
from app.parsers.utils import clean_text, extract_package_quantity, fetch_html, parse_price


SUPPLIER = "napolke"
URL = "https://napolke.ru/catalog/chay_kofe_kakao/zernovoy_kofe"
BASE_URL = "https://napolke.ru"
COFFEE_WORD = "\u043a\u043e\u0444\u0435"
GRAIN_PREFIX = "\u0437\u0435\u0440"
RUBLE_SIGN = "\u20bd"
RUBLE_WORD = "\u0440\u0443\u0431"
RUBLE_LETTER = "\u0440"


def _warn(message: str) -> None:
    print(f"Warning: {SUPPLIER}: {message}")


def _extract_price_raw(card) -> str | None:
    int_price = card.select_one(".int-price")
    common_price = card.select_one(".common-price")
    if int_price and common_price:
        return clean_text(
            f"{int_price.get_text(' ', strip=True)} {common_price.get_text(' ', strip=True)}"
        )

    price_area = card.select_one(".desktop-product-card-bottom") or card
    text = clean_text(price_area.get_text(" ", strip=True))
    number = r"\d[\d\s]*(?:[.,]\s*\d{1,2})?"
    match = re.search(
        rf"{number}\s*(?:{RUBLE_SIGN}|{RUBLE_WORD}\.?|{RUBLE_LETTER}\.?)",
        text,
        flags=re.IGNORECASE,
    )
    return clean_text(match.group(0)) if match else text


def _combine_quantities(product_name: str, unit_raw: str | None) -> tuple[str | None, str | None]:
    quantities: list[str] = []
    for candidate in (product_name, unit_raw or ""):
        quantity = extract_package_quantity(candidate)
        if quantity and quantity not in quantities:
            quantities.append(quantity)

    if not quantities:
        return None, None

    value = ", ".join(quantities)
    return value, value


def parse_napolke() -> ProductOffer | None:
    html = fetch_html(URL)
    if html is None:
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")
        for card in soup.select(".desktop-product-card-root"):
            title_el = card.select_one(".product-title")
            if title_el is None:
                continue

            product_name = clean_text(title_el.get_text(" ", strip=True))
            lowered_name = product_name.lower()
            if COFFEE_WORD not in lowered_name or GRAIN_PREFIX not in lowered_name:
                continue

            price_raw = _extract_price_raw(card)
            price = parse_price(price_raw or "")

            unit_el = card.select_one(".wdio-card-unit")
            unit_raw = clean_text(unit_el.get_text(" ", strip=True)) if unit_el else None
            package_quantity, package_quantity_raw = _combine_quantities(product_name, unit_raw)

            if price is None or package_quantity is None:
                continue

            product_url = URL
            if title_el.has_attr("href"):
                product_url = urljoin(BASE_URL, title_el["href"])

            return ProductOffer(
                supplier=SUPPLIER,
                product_name=product_name,
                price=price,
                price_raw=price_raw,
                package_quantity=package_quantity,
                package_quantity_raw=package_quantity_raw,
                url=product_url,
            )
    except Exception as exc:
        _warn(f"failed to parse page: {exc}")
        return None

    _warn("no grain coffee product with price and package quantity was found")
    return None
