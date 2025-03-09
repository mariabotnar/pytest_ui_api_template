import requests
import pytest


base_URL = "https://api.kinopoisk.dev"
token = "PZ8GKY7-G1K47DC-JQRT1R0-5J750R2"

class ApiPage:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token

    #def get_search_by_id(self, ):

