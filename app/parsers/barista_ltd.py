from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.parsers.base import ProductOffer
from app.parsers.utils import clean_text, extract_package_quantity, fetch_html, parse_price


SUPPLIER = "barista_ltd"
URL = "https://www.barista-ltd.ru/magazin/produkti/cofe/kofe-dlya-vendinga.html"
BASE_URL = "https://www.barista-ltd.ru"
COFFEE_WORD = "\u043a\u043e\u0444\u0435"
GRAIN_PREFIX = "\u0437\u0435\u0440"


def _warn(message: str) -> None:
    print(f"Warning: {SUPPLIER}: {message}")


def parse_barista_ltd() -> ProductOffer | None:
    html = fetch_html(URL)
    if html is None:
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")
        for card in soup.select(".product_grid_item"):
            price_el = card.select_one(".jshop_price")
            title_el = card.select_one(".result-title a, .result-title, .name a, .name")
            if price_el is None or title_el is None:
                continue

            product_name = clean_text(title_el.get_text(" ", strip=True))
            lowered_name = product_name.lower()
            if COFFEE_WORD not in lowered_name or GRAIN_PREFIX not in lowered_name:
                continue

            price_raw = clean_text(price_el.get_text(" ", strip=True))
            price = parse_price(price_raw)
            package_quantity = extract_package_quantity(product_name)
            if package_quantity is None:
                package_quantity = extract_package_quantity(card.get_text(" ", strip=True))

            if price is None or package_quantity is None:
                continue

            link_el = title_el if title_el.name == "a" else card.select_one("a[href]")
            product_url = urljoin(BASE_URL, link_el["href"]) if link_el and link_el.has_attr("href") else URL

            return ProductOffer(
                supplier=SUPPLIER,
                product_name=product_name,
                price=price,
                price_raw=price_raw,
                package_quantity=package_quantity,
                package_quantity_raw=package_quantity,
                url=product_url,
            )
    except Exception as exc:
        _warn(f"failed to parse page: {exc}")
        return None

    _warn("no grain coffee product with price and package quantity was found")
    return None
