from re import search

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://www.kinopoisk.ru/'
        self.search_input_locator = (By.CSS_SELECTOR, "input[name='kp_query']")
        self.get_search_result_locator = (By.CSS_SELECTOR,  "a[data-url='/film/41520']")

    def open(self):
        try:
            self.driver.get(self.url)
        except Exception as e:
            print(f"Ошибка при открытии страницы: {e}")

    def get_title(self):
        try:
            return self.driver.title
        except Exception as e:
            print(f"Ошибка при открытии страницы: {e}")


    def wait_for_element(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            print(f"Элемент не найден: {e}")
            raise

    def enter_search_query(self, query):
        try:
            search_input = self.wait_for_element(self.search_input_locator)
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"Ошибка при вводе запроса: {e}")

    def search(self, query):
        try:
            self.enter_search_query(query)
        except Exception as e:
            print(f"Ошибка при выполнении поиска: {e}")

    def get_search_result(self):
        search_result = self.wait_for_element(self.get_search_result_locator)
        return search_result.get_attribute("value")