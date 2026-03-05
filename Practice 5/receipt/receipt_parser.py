import re
import json
import sys
from typing import Any, Dict, List, Optional

MONEY_RE = r"\d{1,3}(?: \d{3})*,\d{2}"


def normalize_spaces(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def money_to_float(value: str) -> float:
    value = value.replace(" ", "").replace(",", ".")
    return float(value)


def money_to_int_if_possible(value: float):
    return int(value) if value.is_integer() else value


def parse_datetime(text: str) -> Optional[str]:
    m = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text, re.I)
    if not m:
        return None
    return f"{m.group(1)} {m.group(2)}"


def parse_payment_method(text: str) -> Optional[str]:
    patterns = [
        r"(Банковская карта)\s*:\s*" + MONEY_RE,
        r"(Наличные)\s*:\s*" + MONEY_RE,
        r"(Kaspi Gold|Kaspi QR|QR|Apple Pay|Google Pay)\s*:\s*" + MONEY_RE,
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            return m.group(1)
    return None


def parse_total(text: str) -> Optional[float]:
    m = re.search(r"ИТОГО:\s*(" + MONEY_RE + r")", text, re.I)
    return money_to_float(m.group(1)) if m else None


def extract_all_prices(text: str) -> List[float]:
    prices: List[float] = []
    for m in re.finditer(MONEY_RE, text):
        start, end = m.span()
        after = text[end:end + 5]
        # Skip quantities like "2,000 x 154,00".
        if re.match(r"\s*x(?:\s|$)", after):
            continue
        prices.append(money_to_float(m.group(0)))
    return prices


def extract_item_blocks(text: str) -> List[str]:
    lines = [line.strip() for line in text.split("\n")]
    blocks: List[str] = []
    current: List[str] = []
    in_items = False

    for line in lines:
        if re.match(r"^1\.\s*$", line):
            in_items = True
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            current.append(line)
            continue

        if in_items and re.match(r"^\d+\.\s*$", line):
            if current:
                blocks.append("\n".join(current).strip())
            current = [line]
            continue

        if in_items and re.match(r"^(Банковская карта|Наличные|ИТОГО:)", line, re.I):
            if current:
                blocks.append("\n".join(current).strip())
            break

        if in_items:
            current.append(line)

    return [b for b in blocks if b.strip()]


def parse_item_block(block: str) -> Optional[Dict[str, Any]]:
    lines = [line.strip() for line in block.split("\n") if line.strip()]
    if not lines:
        return None

    if re.match(r"^\d+\.$", lines[0]):
        lines = lines[1:]

    if not lines:
        return None

    qty_price_idx = None
    qty_price_match = None

    for idx, line in enumerate(lines):
        m = re.search(r"(\d+[,.]\d{3})\s*x\s*(" + MONEY_RE + r")", line)
        if m:
            qty_price_idx = idx
            qty_price_match = m
            break

    if qty_price_idx is None or qty_price_match is None:
        return None

    name_lines = lines[:qty_price_idx]
    product_name = " ".join(name_lines).strip()
    product_name = re.sub(r"\s+", " ", product_name)

    quantity = float(qty_price_match.group(1).replace(",", "."))
    unit_price = money_to_float(qty_price_match.group(2))

    item_total = None
    for follow in lines[qty_price_idx + 1:]:
        if re.fullmatch(MONEY_RE, follow):
            item_total = money_to_float(follow)
            break

    if item_total is None:
        item_total = round(quantity * unit_price, 2)

    return {
        "name": product_name,
        "quantity": quantity,
        "unit_price": money_to_int_if_possible(unit_price),
        "line_total": money_to_int_if_possible(item_total),
    }


def parse_receipt(text: str) -> Dict[str, Any]:
    text = normalize_spaces(text)
    items = []
    for block in extract_item_blocks(text):
        parsed = parse_item_block(block)
        if parsed:
            items.append(parsed)

    item_names = [item["name"] for item in items]
    item_sum = round(sum(float(item["line_total"]) for item in items), 2)
    total = parse_total(text)

    all_prices: List[float] = []
    for item in items:
        all_prices.append(float(item["unit_price"]))
        all_prices.append(float(item["line_total"]))
    if total is not None:
        all_prices.append(total)
    vat_match = re.search(r"в т\.ч\. НДС\s*12%:\s*(" + MONEY_RE + r")", text, re.I)
    if vat_match:
        all_prices.append(money_to_float(vat_match.group(1)))

    result: Dict[str, Any] = {
        "store": None,
        "receipt_number": None,
        "date_time": parse_datetime(text),
        "payment_method": parse_payment_method(text),
        "all_prices": [money_to_int_if_possible(v) for v in all_prices],
        "products": item_names,
        "items": items,
        "calculated_total": money_to_int_if_possible(item_sum),
        "receipt_total": money_to_int_if_possible(total) if total is not None else None,
        "totals_match": (abs(item_sum - total) < 0.01) if total is not None else None,
    }

    store_match = re.search(r"Филиал\s+ТОО\s+(.+)", text)
    if store_match:
        result["store"] = store_match.group(1).strip()

    receipt_match = re.search(r"Чек\s*№\s*(\d+)", text)
    if receipt_match:
        result["receipt_number"] = receipt_match.group(1)

    return result


SAMPLE_RECEIPT = """ДУБЛИКАТ
Филиал ТОО EUROPHARMA Астана
БИН 080841000762
НДС Серия 58002
 № 0014371
Касса 300-190
Смена 10
Порядковый номер чека №61
Чек №2331180266
Кассир Аптека 17-1
ПРОДАЖА
1.
Натрия хлорид 0,9%, 200 мл, фл
2,000 x 154,00
308,00
Стоимость
308,00
2.
Борный спирт 3%, 20 мл, фл.
1,000 x 51,00
51,00
Стоимость
51,00
3.
Шприц 2 мл, 3-х комп. (Bioject)
2,000 x 16,00
32,00
Стоимость
32,00
4.
Система для инфузии Vogt Medical
2,000 x 60,00
120,00
Стоимость
120,00
5.
Шприц 5 мл, 3-х комп.
1,000 x 310,00
310,00
Стоимость
310,00
6.
AURA Ватные диски №150
1,000 x 461,00
461,00
Стоимость
461,00
7.
Чистая линия скраб мягкий 50 мл
1,000 x 381,00
381,00
Стоимость
381,00
8.
Чистая линия  скраб очищающийабрикос 50 мл
1,000 x 386,00
386,00
Стоимость
386,00
9.
Чистая линия скраб мягкий 50 мл
1,000 x 381,00
381,00
Стоимость
381,00
10.
Nivea шампунь 3в1мужской  400 мл
1,000 x 414,00
414,00
Стоимость
414,00
11.
Pro Series Шампунь яркий цвет 500мл
1,000 x 841,00
841,00
Стоимость
841,00
12.
Pro Series бальзам-ополаскивательдля длител ухода за окрашеннымиволосами Яркий цвет 500мл
1,000 x 841,00
841,00
Стоимость
841,00
13.
Clear шампунь Актив спорт 2в1мужской  400 мл
1,000 x 1 200,00
1 200,00
Стоимость
1 200,00
14.
Bio World (HYDRO THERAPY)Мицеллярная вода 5в1, 445мл
1,000 x 1 152,00
1 152,00
Стоимость
1 152,00
15.
Bio World (HYDRO THERAPY) Гель-муссдля умывания с гиалуроновойкислотой, 250мл
1,000 x 1 152,00
1 152,00
Стоимость
1 152,00
16.
[RX]-Натрия хлорид 0,9%, 100 мл, фл.
1,000 x 168,00
168,00
Стоимость
168,00
17.
[RX]-Дисоль р-р 400 мл, фл.
1,000 x 163,00
163,00
Стоимость
163,00
18.
Тагансорбент с иономи серебра №30,пор.
1,000 x 1 526,00
1 526,00
Стоимость
1 526,00
19.
[RX]-Церукал 2%, 2 мл, №10, амп.
2,000 x 396,00
792,00
Стоимость
792,00
20.
[RX]-Андазол 200 мг, №40, табл.
1,000 x 7 330,00
7 330,00
Стоимость
7 330,00
Банковская карта:
18 009,00
ИТОГО:
18 009,00
в т.ч. НДС 12%:
0,00
Фискальный признак:
2331180266
Время: 18.04.2019 11:13:58
г. Нур-султан,Казахстан, Мангилик Ел,19, нп-5
Оператор фискальных данных: АО"Казахтелеком"Для проверки чека зайдите на сайт:consumer.oofd.kz
ФИСКАЛЬНЫЙ ЧЕК
ФП
ИНК ОФД: 311559
Код ККМ КГД (РНМ): 620300145311
ЗНМ: SWK00034965
WEBKASSA.KZ"""


def main() -> None:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            receipt_text = f.read()
    else:
        receipt_text = SAMPLE_RECEIPT

    parsed = parse_receipt(receipt_text)
    print(json.dumps(parsed, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
