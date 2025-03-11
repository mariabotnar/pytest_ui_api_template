import requests
import pytest

baseURL = "https://api.kinopoisk.dev/v1.4"
api_key = "PZ8GKY7-G1K47DC-JQRT1R0-5J750R2"

# Параметры для теста
test_params = [
    {"genres": "комедия", "countries": "Россия", "ageRating": "12", "limit": 1},
    # Добавьте другие наборы параметров, если необходимо
]

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

    try:
        # Выполнение GET-запроса
        response = requests.get(f"{baseURL}/movie/random", headers=headers, params=query_params)

        # Проверка статус-кода ответа
        assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}"

        # Парсинг JSON-ответа
        movie_data = response.json()

        # Проверка, что ответ содержит данные о фильме
        assert isinstance(movie_data, dict), "Ответ не является словарем"
        assert "id" in movie_data, "Ответ не содержит ключа 'id'"
        assert "name" in movie_data, "Ответ не содержит ключа 'name'"
        assert "genres" in movie_data, "Ответ не содержит ключа 'genres'"
        assert "countries" in movie_data, "Ответ не содержит ключа 'countries'"

        # Дополнительные проверки, если необходимо
        assert movie_data["ageRating"] == int(params["ageRating"]), f"Возрастной рейтинг не соответствует ожидаемому: {movie_data['ageRating']}"
        assert any(genre["name"] == params["genres"] for genre in movie_data["genres"]), f"Жанр '{params['genres']}' не найден"
        assert any(country["name"] == params["countries"] for country in movie_data["countries"]), f"Страна '{params['countries']}' не найдена"

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка при выполнении запроса: {e}")
    except ValueError as e:
        pytest.fail(f"Ошибка при парсинге JSON: {e}")
    except Exception as e:
        pytest.fail(f"Неожиданная ошибка: {e}")