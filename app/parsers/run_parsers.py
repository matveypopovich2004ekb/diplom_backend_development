import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Callable

from app.parsers.barista_ltd import parse_barista_ltd
from app.parsers.base import ProductOffer
from app.parsers.cofe_optom import parse_cofe_optom
from app.parsers.napolke import parse_napolke
from app.parsers.utils import save_to_json
from app.parsers.re_filters import parse_price, parse_package_quantity_grams

ParserFunc = Callable[[], ProductOffer | None]


def _get_parser_functions() -> list[ParserFunc]:
    return [
        parse_barista_ltd,
        parse_napolke,
        parse_cofe_optom,
    ]


def parse_all_coffee_offers() -> list[ProductOffer]:
    """Запускает все парсеры кофе и возвращает список найденных предложений."""

    offers: list[ProductOffer] = []

    for parser_func in _get_parser_functions():
        try:
            offer = parser_func()
        except Exception as exc:
            print(f"Warning: {parser_func.__name__}: unexpected error: {exc}")
            continue

        if offer is not None:
            offer.price = parse_price(offer.price)
            offer.package_quantity = parse_package_quantity_grams(offer.package_quantity)
            offer.product_name = "Зерна кофе"
            offers.append(offer)

    return offers


def _print_result(data: list[dict]) -> None:
    try:
        sys.stdout.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    except UnicodeEncodeError:
        sys.stdout.write(json.dumps(data, ensure_ascii=True, indent=2) + "\n")


def main() -> None:
    offers = parse_all_coffee_offers()

    data = [asdict(offer) for offer in offers]

    _print_result(data)

    output_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "parsed_coffee_products.json"
    )

    save_to_json(data, output_path)

    print(f"Saved {len(data)} product(s) to {output_path}")


if __name__ == "__main__":
    main()


