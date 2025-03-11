import requests
import pytest

baseURL = "https://api.kinopoisk.dev/v1.4"
api_key = "PZ8GKY7-G1K47DC-JQRT1R0-5J750R2"

# Параметры для авторизации
headers = {
    "X-API-KEY": api_key,
    "Content-Type": "application/json"
}

# Параметризация: список id, которые находятся вне диапазона
test_ids = [-1]

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

    try:
        # Выполнение GET-запроса
        response = requests.get(f"{baseURL}/movie", headers=headers, params=params)

        # Проверка статус-кода ответа
        assert response.status_code == 400, (
            f"Ожидался статус-код 400 для некорректного movie_id={movie_id}, "
            f"но получен {response.status_code}"
        )

        # Парсинг JSON-ответа (если нужно)
        response_data = response.json()
        print(f"Ответ сервера: {response_data}")  # Для отладки

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка при выполнении запроса: {e}")
    except ValueError as e:
        pytest.fail(f"Ошибка при парсинге JSON: {e}")
    except Exception as e:
        pytest.fail(f"Неожиданная ошибка: {e}")