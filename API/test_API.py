import requests
import pytest

# Базовый URL API
baseURL = "https://api.kinopoisk.dev/v1.4"

# API Key для авторизации
api_key = "PZ8GKY7-G1K47DC-JQRT1R0-5J750R2"

# Параметризация для тестирования разных названий фильмов
@pytest.mark.parametrize("movie_title, expected_movie_id", [
    ("Брат 2", 41520),  # Пример: Ожидаемый ID для фильма "Брат 2"
    ("Матрица", 301),  # Пример: Ожидаемый ID для фильма "Матрица"
])
def test_movie_search_by_title(movie_title, expected_movie_id):
    # Заголовки с API Key для авторизации
    headers = {
        "X-API-KEY": api_key
    }

    # Параметры запроса
    params = {
        "page": 1,
        "limit": 15,
        "query": movie_title
    }

    # Выполнение GET-запроса
    response = requests.get(f"{baseURL}/movie/search", headers=headers, params=params)

    # Проверка, что запрос выполнен успешно
    assert response.status_code == 200, f"Ошибка: {response.status_code}"

    # Парсинг JSON-ответа
    data = response.json()

    # Проверка, что в ответе есть хотя бы один фильм
    assert data.get("docs"), "Нет результатов поиска"

    # Проверка, что первый фильм в результатах имеет ожидаемый ID
    first_movie = data["docs"][0]
    assert first_movie["id"] == expected_movie_id, f"Ожидался фильм с ID {expected_movie_id}, но получен {first_movie['id']}"


import pytest
import requests

# Базовый URL API
baseURL = "https://api.kinopoisk.dev/v1.4/movie"


# Параметризация теста: список id фильмов и ожидаемых названий
@pytest.mark.parametrize("movie_id, expected_title", [
    (41520, "Брат"),
    (301, "Матрица"),
    (328, "Побег из Шоушенка"),
])
def test_get_movie_by_id(movie_id, expected_title):
    # Заголовок с API Key
    headers = {
        "X-API-KEY": "PZ8GKY7-G1K47DC-JQRT1R0-5J750R2"  # Замените на ваш API Key
    }

    # Выполнение GET-запроса
    response = requests.get(f"{baseURL}/{movie_id}", headers=headers)

    # Проверка статус-кода ответа
    assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}"

    # Парсинг JSON-ответа
    movie_data = response.json()

    # Проверка, что название фильма соответствует ожидаемому
    assert movie_data.get(
        "name") == expected_title, f"Ожидалось название '{expected_title}', но получено '{movie_data.get('name')}'"


import pytest
import requests

# Базовый URL API
baseURL = "https://api.kinopoisk.dev/v1.4"

# Параметры для теста
test_params = [
    {"genres": "комедия", "countries": "Россия", "ageRating": "12", "limit": 1},
    # Добавьте другие наборы параметров, если необходимо
]

# API Key для авторизации
api_key = "PZ8GKY7-G1K47DC-JQRT1R0-5J750R2"


@pytest.mark.parametrize("params", test_params)
def test_random_movie_selection(params):
    # Заголовки с API Key
    headers = {
        "X-API-KEY": api_key
    }

    # Параметры запроса
    query_params = {
        "genres.name": params["genres"],
        "countries.name": params["countries"],
        "ageRating": params["ageRating"],
        "limit": params["limit"]
    }

    # Выполнение GET-запроса
    response = requests.get(f"{baseURL}/movie/random", headers=headers, params=query_params)

    # Проверка статус-кода ответа
    assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}"

    # Проверка, что ответ содержит данные о фильме
    movie_data = response.json()
    assert "docs" in movie_data, "Ответ не содержит ключа 'docs'"
    assert len(movie_data["docs"]) > 0, "Список фильмов пуст"

    # Проверка, что фильм соответствует заданным параметрам
    movie = movie_data["docs"][0]
    assert params["genres"] in [genre["name"] for genre in
                                movie.get("genres", [])], "Жанр фильма не соответствует ожидаемому"
    assert params["countries"] in [country["name"] for country in
                                   movie.get("countries", [])], "Страна фильма не соответствует ожидаемой"
    assert movie.get("ageRating") == params["ageRating"], "Возрастной рейтинг фильма не соответствует ожидаемому"


import pytest
import requests

# Базовый URL API
baseURL = "https://your-api-domain.com/v1.4/movie"

# Параметры для авторизации
headers = {
    "Authorization": "Bearer YOUR_API_KEY",  # Замените YOUR_API_KEY на ваш API ключ
    "Content-Type": "application/json"
}

# Параметризация: список id, которые находятся вне диапазона
test_ids = [82361233225, 99999999999, 123456789012]

@pytest.mark.parametrize("movie_id", test_ids)
def test_search_movie_by_id_out_of_range(movie_id):
    # Параметры запроса
    params = {
        "page": 1,
        "limit": 5,
        "id": movie_id,
        "type": "",
        "status": ""
    }

    # Выполнение GET-запроса
    response = requests.get(baseURL, headers=headers, params=params)

    # Проверка статус-кода ответа
    assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}"

    # Проверка, что в ответе нет данных о фильме
    response_data = response.json()
    assert len(response_data.get("data", [])) == 0, f"Найден фильм с id {movie_id}, хотя не должен был быть найден"

# Запуск теста
if __name__ == "__main__":
    pytest.main()


import pytest
import requests

# Базовый URL API
baseURL = "https://api.kinopoisk.dev/v1.4/movie"

# Параметры для авторизации
headers = {
    "X-API-KEY": "your_api_key_here"  # Замените на ваш API Key
}

# Параметризация для теста
@pytest.mark.parametrize("rating, expected_status_code, expected_total", [
    (-1, 200, 0),  # Ожидаем, что фильмов с рейтингом -1 не будет
    (-2, 200, 0),  # Ожидаем, что фильмов с рейтингом -2 не будет
    (-5, 200, 0),  # Ожидаем, что фильмов с рейтингом -5 не будет
])
def test_search_movie_with_negative_rating(rating, expected_status_code, expected_total):
    # Параметры запроса
    params = {
        "type": "tv-series",
        "status": "",
        "rating.kp": rating
    }

    # Выполнение запроса
    response = requests.get(baseURL, headers=headers, params=params)

    # Проверка статус кода
    assert response.status_code == expected_status_code, f"Ожидался статус код {expected_status_code}, но получен {response.status_code}"

    # Проверка, что фильмов с таким рейтингом нет
    data = response.json()
    assert data.get("total") == expected_total, f"Ожидалось, что найдено {expected_total} фильмов, но найдено {data.get('total')}"
