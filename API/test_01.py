import requests
import pytest

baseURL = "https://api.kinopoisk.dev/v1.4"
api_key = "PZ8GKY7-G1K47DC-JQRT1R0-5J750R2"


@pytest.mark.parametrize("movie_title, expected_movie_id", [("Брат 2", 41520)])
def test_01_movie_search_by_title(movie_title, expected_movie_id):
    headers = {
        "X-API-KEY": api_key
    }
    params = {
        "page": 1,
        "limit": 5,
        "query": movie_title
    }

    try:
        # Выполнение GET-запроса
        response = requests.get(f"{baseURL}/movie/search", headers=headers, params=params)

        # Проверка, что запрос выполнен успешно
        assert response.status_code == 200, f"Ошибка: {response.status_code}"

        # Проверка, что ответ содержит JSON
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, "Ответ не является JSON"

        # Парсинг JSON-ответа
        data = response.json()

        # Проверка, что в ответе есть хотя бы один фильм
        assert data.get("docs"), "Нет результатов поиска"

        # Проверка, что первый фильм в результатах имеет ожидаемый ID
        first_movie = data["docs"][0]
        assert first_movie["id"] == expected_movie_id, f"Ожидался фильм с ID {expected_movie_id}, но получен {first_movie['id']}"

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка при выполнении запроса: {e}")
    except ValueError as e:
        pytest.fail(f"Ошибка при парсинге JSON: {e}")
    except Exception as e:
        pytest.fail(f"Неожиданная ошибка: {e}")