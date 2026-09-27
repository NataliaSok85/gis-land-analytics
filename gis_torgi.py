import requests
import pandas as pd
import re


# Прямые открытые данные ГИС Торги.
# Используем несколько вариантов адресов,
# чтобы приложение могло попробовать другой источник,
# если один из них временно недоступен.

DATA_URLS = [
    "https://torgi.gov.ru/new/opendata/7710568760-notice/data-20260801T0000-",
    "https://torgi.gov.ru/new/opendata/7710568760-notice/data-20260701T0000-",
    "https://torgi.gov.ru/new/opendata/7710568760-notice/data-20260601T0000-",
]


def find_cadastral(value):
    """
    Ищет кадастровый номер в тексте.
    """

    if not value:
        return None

    pattern = r"\d{2}:\d{2}:\d{7,}"

    match = re.search(pattern, str(value))

    if match:
        return match.group(0)

    return None


def search_in_item(item, cadastral_quarter):
    """
    Проверяет всю запись ГИС Торги
    на наличие нужного кадастрового квартала.
    """

    text = str(item)

    return cadastral_quarter in text


def load_torgi_data():
    """
    Загружает открытые данные ГИС Торги.
    """

    last_error = None

    for url in DATA_URLS:

        try:

            response = requests.get(
                url,
                timeout=60,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            if response.status_code != 200:
                continue

            try:
                data = response.json()
                return data

            except Exception:

                # Иногда сервер может вернуть
                # большой JSON-файл как текст.
                return response.json()

        except Exception as error:

            last_error = error

    raise RuntimeError(
        "Не удалось загрузить открытые данные "
        "ГИС Торги. Последняя ошибка: "
        + str(last_error)
    )


def search_cadastral_quarter(
    cadastral_quarter,
    data
):
    """
    Ищет торги по кадастровому кварталу.
    """

    results = []

    if not data:
        return results

    # Если данные находятся внутри словаря
    if isinstance(data, dict):

        # Возможные варианты структуры
        possible_lists = [
            data.get("data"),
            data.get("items"),
            data.get("notices"),
            data.get("results")
        ]

        for value in possible_lists:

            if isinstance(value, list):
                data = value
                break

    if not isinstance(data, list):
        return results

    for item in data:

        if search_in_item(
            item,
            cadastral_quarter
        ):

            results.append(item)

    return results


def normalize_results(results):
    """
    Превращает найденные записи
    в таблицу pandas.
    """

    if not results:
        return pd.DataFrame()

    rows = []

    for item in results:

        if isinstance(item, dict):

            row = {}

            for key, value in item.items():

                if isinstance(
                    value,
                    (dict, list)
                ):

                    value = str(value)

                row[key] = value

            rows.append(row)

        else:

            rows.append({
                "Данные": str(item)
            })

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)













