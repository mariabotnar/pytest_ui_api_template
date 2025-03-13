import logging
import pytest
from pytest_ui_api_template.API.MovieAPI import MovieAPI
from pytest_ui_api_template.API.config import BASE_URL
from pytest_ui_api_template.API.config import API_KEY


@pytest.fixture
def movie_api():
    return MovieAPI(BASE_URL, API_KEY)

@pytest.mark.parametrize("movie_title, expected_movie_id", [("Брат 2", 41520)])
def test_01_movie_search_by_title(movie_title, expected_movie_id, movie_api):
    response = movie_api.search_movie_by_title(movie_title)
    data = response.json()
    assert data.get("docs"), "Нет результатов поиска"
    first_movie = data["docs"][0]
    assert first_movie["id"] == expected_movie_id, f"Ожидался фильм с ID {expected_movie_id}, но получен {first_movie['id']}"

@pytest.mark.parametrize("params", [{"genres": "комедия", "countries": "Россия", "ageRating": "12", "limit": 1}])
def test_random_movie_selection(params, movie_api):
    response = movie_api.get_random_movie(params["genres"], params["countries"], params["ageRating"], params["limit"])
    movie_data = response.json()
    assert isinstance(movie_data, dict), "Ответ не является словарем"
    assert "id" in movie_data, "Ответ не содержит ключа 'id'"
    assert "name" in movie_data, "Ответ не содержит ключа 'name'"
    assert "genres" in movie_data, "Ответ не содержит ключа 'genres'"
    assert "countries" in movie_data, "Ответ не содержит ключа 'countries'"
    assert movie_data["ageRating"] == int(params["ageRating"]), f"Возрастной рейтинг не соответствует ожидаемому: {movie_data['ageRating']}"
    assert any(genre["name"] == params["genres"] for genre in movie_data["genres"]), f"Жанр '{params['genres']}' не найден"
    assert any(country["name"] == params["countries"] for country in movie_data["countries"]), f"Страна '{params['countries']}' не найдена"

@pytest.mark.parametrize("movie_id", [-1])
def test_search_movie_by_id_out_of_range(movie_id, movie_api):
    response = movie_api.get_movie_by_id(movie_id)
    assert response.status_code == 400, f"Ожидался статус-код 400 для некорректного movie_id={movie_id}, "f"но получен {response.status_code}"
    data = response.json()
    assert "message" in data, "Ответ не содержит сообщения об ошибке"
    logging.debug(f"Сообщение об ошибке: {data['message']}")

@pytest.mark.parametrize("rating, expected_status_code", [(-5, 400)])
def test_search_movie_with_negative_rating(rating, expected_status_code, movie_api):
    response = movie_api.search_movie_by_rating(rating)
    assert response.status_code == expected_status_code, f"Ожидался статус-код {expected_status_code}, но получен {response.status_code}"

def test_search_movie_with_empty_title(movie_api):
    response = movie_api.search_movie_by_title("")
    assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}"
    data = response.json()
    assert data.get("docs"), "Нет результатов поиска"

def test_invalid_api_key(movie_api):
    invalid_api = MovieAPI(BASE_URL, "invalid_key")
    response = invalid_api.search_movie_by_title("Брат 2")
    assert response.status_code == 401, f"Ожидался статус-код 401, но получен {response.status_code}"
    data = response.json()
    assert "message" in data, "Ответ не содержит сообщения об ошибке"
    logging.debug(f"Сообщение об ошибке: {data['message']}")

@pytest.mark.parametrize("movie_title", ["НесуществующийФильм123"])
def test_search_movie_with_non_existent_title(movie_title, movie_api):
    response = movie_api.search_movie_by_title(movie_title)
    assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}"
    data = response.json()
    assert not data.get("docs"), "Ожидалось, что результатов поиска не будет"