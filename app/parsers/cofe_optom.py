import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.parsers.base import ProductOffer
from app.parsers.utils import clean_text, extract_package_quantity, fetch_html, parse_price


SUPPLIER = "cofe_optom"
URL = "https://www.cofe-optom.ru/catalog/kofe-v-meshkax-204/"
BASE_URL = "https://www.cofe-optom.ru"
COFFEE_WORD = "\u043a\u043e\u0444\u0435"
GRAIN_WORD = "\u0437\u0435\u0440\u043d\u043e"
RUBLE_LETTER = "\u0440"
ZA = "\u0437\u0430"
SHT = "\u0448\u0442"


def _warn(message: str) -> None:
    print(f"Warning: {SUPPLIER}: {message}")


def _direct_cell_texts(row) -> list[str]:
    return [clean_text(cell.get_text(" ", strip=True)) for cell in row.find_all("td", recursive=False)]


def _extract_price_raw(cells: list[str]) -> str | None:
    for cell in reversed(cells):
        if parse_price(cell) is None:
            continue
        match = re.search(
            rf"\d[\d\s]*(?:[.,]\s*\d{{1,2}})?\s*{RUBLE_LETTER}\.?\s*{ZA}\s*{SHT}\.?:?",
            cell,
            flags=re.IGNORECASE,
        )
        return clean_text(match.group(0)) if match else cell
    return None


def _extract_package_raw(cells: list[str]) -> str | None:
    for cell in cells:
        quantity = extract_package_quantity(cell)
        if quantity:
            return quantity
    return None


def _product_name_from_row(row, cells: list[str]) -> str | None:
    link_el = row.select_one('a[href*="/product/"]')
    name = clean_text(link_el.get_text(" ", strip=True)) if link_el else ""
    if not name:
        name = next((cell for cell in cells if COFFEE_WORD in cell.lower()), "")

    if not name:
        return None

    if GRAIN_WORD not in name.lower():
        name = f"{name} {GRAIN_WORD}"
    return name


def parse_cofe_optom() -> ProductOffer | None:
    html = fetch_html(URL)
    if html is None:
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")
        for row in soup.select("tr"):
            cells = _direct_cell_texts(row)
            if len(cells) < 5:
                continue

            row_text = clean_text(row.get_text(" ", strip=True))
            lowered_row = row_text.lower()
            if COFFEE_WORD not in lowered_row or GRAIN_WORD not in lowered_row:
                continue

            product_name = _product_name_from_row(row, cells)
            price_raw = _extract_price_raw(cells)
            package_quantity_raw = _extract_package_raw(cells)
            price = parse_price(price_raw or "")
            package_quantity = extract_package_quantity(package_quantity_raw or "")

            if product_name is None or price is None or package_quantity is None:
                continue

            link_el = row.select_one('a[href*="/product/"]')
            product_url = urljoin(BASE_URL, link_el["href"]) if link_el and link_el.has_attr("href") else URL

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
