import re

def parse_price(value) -> float | None:
    """
    Достает число цены из строки или возвращает число, если оно уже число.

    Примеры:
    1451.48 -> 1451.48
    "от 1 451.48 руб." -> 1451.48
    "170 .63 ₽" -> 170.63
    "1150 р. за шт." -> 1150.0
    """

    if value is None:
        return None

    if isinstance(value, int | float):
        return float(value)

    text = str(value)

    # Убираем пробел между целой и дробной частью: "170 .63" -> "170.63"
    text = re.sub(r"(\d)\s+\.(\d)", r"\1.\2", text)

    # Убираем пробелы внутри больших чисел: "1 451.48" -> "1451.48"
    text = re.sub(r"(?<=\d)\s+(?=\d)", "", text)

    # Меняем запятую на точку: "1451,48" -> "1451.48"
    text = text.replace(",", ".")

    match = re.search(r"\d+(?:\.\d+)?", text)

    if not match:
        return None

    return float(match.group())


def parse_package_quantity_grams(value) -> int | None:
    """
    Достает количество продукта и приводит его к граммам.

    Примеры:
    "1000 г" -> 1000
    "100 гр, 1 шт в упаковке" -> 100
    "за 1 кг" -> 1000
    "1 кг" -> 1000
    """

    if value is None:
        return None

    text = str(value).lower()
    text = text.replace(",", ".")

    # Ищем число + единицу измерения
    # Например: "1000 г", "100 гр", "1 кг"
    match = re.search(r"(\d+(?:\.\d+)?)\s*(кг|килограмм|килограмма|г|гр|грамм|грамма)", text)

    if not match:
        return None

    number = float(match.group(1))
    unit = match.group(2)

    if unit in ["кг", "килограмм", "килограмма"]:
        return int(number * 1000)

    if unit in ["г", "гр", "грамм", "грамма"]:
        return int(number)

    return None



