import requests
from pytest_ui_api_template.API.BaseAPI import BaseAPI


class MovieAPI(BaseAPI):
    def search_movie_by_title(self, title, limit=5):
        params = {
            "page": 1,
            "limit": limit,
            "query": title
        }
        return self.get("movie/search", params=params)

    def get_random_movie(self, genres, countries, age_rating, limit=1):
        params = {
            "genres.name": genres,
            "countries.name": countries,
            "ageRating": age_rating,
            "limit": limit
        }
        return self.get("movie/random", params=params)

    def get_movie_by_id(self, movie_id):
        params = {
            "page": 1,
            "limit": 5,
            "id": movie_id,
            "type": "",
            "status": ""
        }
        response = requests.get(f"{self.base_url}/movie", headers=self.headers, params=params)
        return response

    def search_movie_by_rating(self, rating, type="tv-series", status=""):
        params = {
            "type": type,
            "status": status,
            "rating.kp": rating
        }
        return self.get("movie", params=params)