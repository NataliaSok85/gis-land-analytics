import requests
import re
import pandas as pd


# Реестр открытых данных ГИС ТОРГИ
REGISTRY_URLS = [
    "https://torgi.gov.ru/new/opendata/list.json",
    "https://torgi.gov.ru/opendata/list.json",
]

# Набор данных извещений ГИС ТОРГИ
DATASET_ID = "7710568760-notice"


def request_json(url, timeout=20):
    """
    Получает JSON по указанному адресу.
    """

    response = requests.get(
        url,
        timeout=timeout,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    return response.json()


def get_registry():
    """
    Получает реестр открытых данных ГИС ТОРГИ.
    """

    errors = []

    for url in REGISTRY_URLS:

        try:

            data = request_json(url)

            return data

        except Exception as error:

            errors.append(
                f"{url}: {error}"
            )

    raise RuntimeError(
        "Не удалось получить реестр открытых данных ГИС ТОРГИ.\n"
        + "\n".join(errors)
    )


def find_dataset(registry):
    """
    Находит в реестре набор извещений ГИС ТОРГИ.
    """

    if isinstance(registry, list):

        items = registry

    elif isinstance(registry, dict):

        items = []

        for key in [
            "items",
            "datasets",
            "data",
            "result"
        ]:

            value = registry.get(key)

            if isinstance(value, list):
                items = value
                break

    else:

        items = []

    for item in items:

        text = str(item)

        if DATASET_ID in text:

            return item

        if (
            "notice" in text.lower()
            and "торг" in text.lower()
        ):

            return item

    return None


def get_meta_url(dataset):
    """
    Пытается найти meta.json в описании набора.
    """

    if not dataset:
        return None

    text = str(dataset)

    patterns = [
        r'https?://[^"\']+meta\.json',
        r'["\']([^"\']*meta\.json)["\']'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            url = match.group(1)

            if url.startswith("/"):

                url = (
                    "https://torgi.gov.ru"
                    + url
                )

            return url

    return None


def load_torgi_data():
    """
    На этом этапе НЕ скачивает большую базу.

    Проверяет:
    1. доступность реестра;
    2. наличие набора извещений;
    3. наличие meta.json.

    Возвращает диагностическую информацию.
    """

    registry = get_registry()

    dataset = find_dataset(registry)

    if not dataset:

        raise RuntimeError(
            "Набор 7710568760-notice "
            "не найден в реестре ГИС ТОРГИ."
        )

    meta_url = get_meta_url(dataset)

    return {
        "registry": registry,
        "dataset": dataset,
        "meta_url": meta_url
    }


def search_cadastral_quarter(
    cadastral_quarter,
    data
):
    """
    Пока возвращает пустой результат.

    Поиск по кадастру подключим после
    подтверждения рабочего источника данных.
    """

    return []


def normalize_results(results):
    """
    Преобразует результаты в таблицу.
    """

    if not results:

        return pd.DataFrame()

    return pd.DataFrame(results)




