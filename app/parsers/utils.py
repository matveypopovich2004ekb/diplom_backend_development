import json
import re
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

import requests


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "coffee-parser-study/1.0"
)
REQUEST_TIMEOUT = 20

RUBLE_SIGN = "\u20bd"
RUBLE_WORD = "\u0440\u0443\u0431"
RUBLE_LETTER = "\u0440"
OPT_WORD = "\u043e\u043f\u0442"
FROM_WORD = "\u043e\u0442"

KG = "\u043a\u0433"
KILOGRAM = "\u043a\u0438\u043b\u043e\u0433\u0440\u0430\u043c\u043c"
GRAM = "\u0433"
GRAM_SHORT = "\u0433\u0440"
SHT = "\u0448\u0442"
KOR = "\u043a\u043e\u0440"
ZA = "\u0437\u0430"
V = "\u0432"
UPAKOVKE = "\u0443\u043f\u0430\u043a\u043e\u0432\u043a\u0435"


def fetch_html(url: str) -> str | None:
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Warning: failed to fetch {url}: {exc}")
        return None

    encoding = response.encoding or response.apparent_encoding or "utf-8"
    if encoding.lower().replace("_", "-") == "windows1251":
        encoding = "windows-1251"

    try:
        return response.content.decode(encoding, errors="replace")
    except LookupError:
        return response.content.decode("utf-8", errors="replace")


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\xa0", " ")).strip()


def _number_to_float(raw_number: str) -> float | None:
    normalized = re.sub(r"\s+", "", clean_text(raw_number)).replace(",", ".")
    try:
        return float(normalized)
    except ValueError:
        return None


def parse_price(text: str) -> float | None:
    cleaned = clean_text(text)
    if not cleaned:
        return None

    number = r"\d[\d\s]*(?:[.,]\s*\d{1,2})?"
    price_patterns = [
        rf"({number})\s*(?:{RUBLE_SIGN}|{RUBLE_WORD}\.?|{RUBLE_LETTER}\.?)",
        rf"(?:{OPT_WORD}\s+{FROM_WORD}|{FROM_WORD})\s*({number})",
        rf"({number})",
    ]

    for pattern in price_patterns:
        match = re.search(pattern, cleaned, flags=re.IGNORECASE)
        if match:
            parsed = _number_to_float(match.group(1))
            if parsed is not None:
                return parsed
    return None


def _normalize_quantity(value: str) -> str:
    normalized = clean_text(value).rstrip(".")
    normalized = re.sub(r"\s*/\s*", "/", normalized)
    normalized = re.sub(r"\s+,", ",", normalized)
    return normalized


def extract_package_quantity(text: str) -> str | None:
    cleaned = clean_text(text)
    if not cleaned:
        return None

    weight_unit = rf"(?:{KG}|kg|{KILOGRAM}(?:\u0430|\u043e\u0432)?|{GRAM_SHORT}\.?|{GRAM}\.?|g)"
    amount = r"\d+(?:[.,]\d+)?"
    patterns = [
        rf"\b{amount}\s*{weight_unit}\s*,?\s*\d+\s*{SHT}\s*/\s*{KOR}\b",
        rf"\b{ZA}\s*{amount}\s*{weight_unit}\b",
        rf"\b\d+\s*{SHT}\s+{V}\s+{UPAKOVKE}\b",
        rf"\b{amount}\s*{weight_unit}\b",
        rf"\b\d+\s*{SHT}\s*/\s*{KOR}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, cleaned, flags=re.IGNORECASE)
        if match:
            return _normalize_quantity(match.group(0))
    return None


def _to_jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: _to_jsonable(item) for key, item in value.items()}
    return value


def save_to_json(data, path):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(_to_jsonable(data), file, ensure_ascii=False, indent=2)


def _run_checks() -> None:
    price_cases = {
        "1 453.00": 1453.0,
        "\u041e\u043f\u0442 \u043e\u0442 1380.35": 1380.35,
        "1375.16 \u20bd/\u0448\u0442": 1375.16,
        "1150 \u0440. \u0437\u0430 \u0448\u0442.": 1150.0,
        "\u043e\u0442 2 304.74 \u0440\u0443\u0431.": 2304.74,
        "170 .63 \u20bd / \u0448\u0442": 170.63,
    }
    for raw, expected in price_cases.items():
        actual = parse_price(raw)
        assert actual == expected, f"parse_price({raw!r}) -> {actual!r}, expected {expected!r}"

    quantity_cases = {
        "1000 \u0433\u0440, 6\u0448\u0442/\u043a\u043e\u0440": "1000 \u0433\u0440, 6\u0448\u0442/\u043a\u043e\u0440",
        "1000 \u0433": "1000 \u0433",
        "1 \u043a\u0433": "1 \u043a\u0433",
        "1 \u0448\u0442 \u0432 \u0443\u043f\u0430\u043a\u043e\u0432\u043a\u0435": "1 \u0448\u0442 \u0432 \u0443\u043f\u0430\u043a\u043e\u0432\u043a\u0435",
        "3 \u0448\u0442 \u0432 \u0443\u043f\u0430\u043a\u043e\u0432\u043a\u0435": "3 \u0448\u0442 \u0432 \u0443\u043f\u0430\u043a\u043e\u0432\u043a\u0435",
        "\u0437\u0430 1 \u043a\u0433": "\u0437\u0430 1 \u043a\u0433",
        "6\u0448\u0442/\u043a\u043e\u0440": "6\u0448\u0442/\u043a\u043e\u0440",
    }
    for raw, expected in quantity_cases.items():
        actual = extract_package_quantity(raw)
        assert actual == expected, (
            f"extract_package_quantity({raw!r}) -> {actual!r}, expected {expected!r}"
        )

    print("All utils checks passed.")


if __name__ == "__main__":
    _run_checks()
