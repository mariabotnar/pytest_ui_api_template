import requests
import pytest

# Константы
BASE_URL = "https://api.kinopoisk.dev/v1.4"
API_KEY = "PZ8GKY7-G1K47DC-JQRT1R0-5J750R2"

# Фикстура для заголовков
@pytest.fixture
def headers():
    return {
        "X-API-KEY": API_KEY
    }

# Параметризация для теста
@pytest.mark.parametrize("rating, expected_status_code, expected_total", [
    (-5, 400, 0)  # Ожидаем, что сервер вернет 400 для некорректного рейтинга
])
def test_search_movie_with_negative_rating(rating, expected_status_code, expected_total, headers):
    # Параметры запроса
    params = {
        "type": "tv-series",
        "status": "",
        "rating.kp": rating
    }

    try:
        # Выполнение GET-запроса
        response = requests.get(f"{BASE_URL}/movie", headers=headers, params=params)

        # Проверка статус-кода ответа
        assert response.status_code == expected_status_code, (
            f"Ожидался статус-код {expected_status_code}, но получен {response.status_code}"
        )

        # Если статус-код 400, проверяем, что ответ содержит сообщение об ошибке
        if response.status_code == 400:
            data = response.json()
            assert "message" in data, "Ответ не содержит ключа 'message'"
            print(f"Сообщение об ошибке: {data['message']}")  # Для отладки

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка при выполнении запроса: {e}")
    except ValueError as e:
        pytest.fail(f"Ошибка при парсинге JSON: {e}")
    except Exception as e:
        pytest.fail(f"Неожиданная ошибка: {e}")