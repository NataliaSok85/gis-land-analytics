import requests
import pandas as pd
import re
from bs4 import BeautifulSoup


# Карточка открытого набора данных ГИС Торги
OPENDATA_CARD_URL = (
    "https://torgi.gov.ru/new/public/opendata/"
    "7710568760-notice"
)


def get_latest_data_url():
    """
    Получает из карточки ГИС Торги ссылку
    на актуальную машиночитаемую выгрузку.
    """

    response = requests.get(
        OPENDATA_CARD_URL,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    html = response.text

    # Ищем ссылки на JSON-файлы выгрузки
    urls = re.findall(
        r'https?://[^"\']+data-[^"\']+\.json',
        html
    )

    if not urls:
        # Иногда ссылка может быть относительной
        relative_urls = re.findall(
            r'["\']([^"\']*data-[^"\']+\.json)["\']',
            html
        )

        urls = [
            "https://torgi.gov.ru" + url
            if url.startswith("/")
            else url
            for url in relative_urls
        ]

    if not urls:
        raise RuntimeError(
            "Не удалось найти актуальную JSON-выгрузку "
            "ГИС Торги в карточке открытых данных."
        )

    # Убираем дубли
    urls = list(dict.fromkeys(urls))

    return urls[0]


def load_torgi_data():
    """
    Загружает актуальные открытые данные ГИС Торги.
    """

    data_url = get_latest_data_url()

    response = requests.get(
        data_url,
        timeout=120,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    return response.json()


def find_cadastral(value):
    """
    Проверяет наличие кадастрового номера
    или кадастрового квартала в тексте.
    """

    if not value:
        return None

    pattern = r"\d{2}:\d{2}:\d{7,}\b"

    match = re.search(pattern, str(value))

    if match:
        return match.group(0)

    return None


def search_cadastral_quarter(
    cadastral_quarter,
    data
):
    """
    Ищет записи по кадастровому кварталу.
    """

    results = []

    if not data:
        return results

    # В зависимости от структуры выгрузки
    # данные могут находиться в разных полях.
    # Поэтому сначала превращаем запись в текст.
    for item in data:

        text = str(item)

        if cadastral_quarter in text:

            results.append(item)

    return results


def normalize_results(results):
    """
    Превращает найденные записи в таблицу.
    """

    if not results:
        return pd.DataFrame()

    rows = []

    for item in results:

        if isinstance(item, dict):

            row = {}

            for key, value in item.items():

                if isinstance(value, (dict, list)):
                    value = str(value)

                row[key] = value

            rows.append(row)

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)
