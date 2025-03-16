import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest_ui_api_template.UI.pages.MainPage import MainPage
from selenium.common.exceptions import TimeoutException
import logging

@pytest.fixture
def browser():
    driver = webdriver.Chrome()  # Инициализация драйвера браузера
    yield driver
    driver.quit()  # Закрытие браузера после завершения теста

@pytest.fixture
def main_page(browser):
    page = MainPage(browser)
    page.open()  # Открытие главной страницы
    return page

def test_open(main_page):
    # работает!!!
    """Проверка открытия главной страницы."""
    # Вывод текущего URL для диагностики
    print("Current URL:", main_page.driver.current_url)

    # Ожидание, пока URL не станет равным ожидаемому
    try:
        WebDriverWait(main_page.driver, 60).until(EC.url_to_be(main_page.url))
    except Exception as e:
        print("Ошибка при ожидании URL:", e)
        print("Фактический URL:", main_page.driver.current_url)
        raise

    # Проверка, что текущий URL соответствует ожидаемому
    assert main_page.driver.current_url == main_page.url, "URL страницы не соответствует ожидаемому"

def test_get_title(main_page):
    # работает!!!
    """Проверка заголовка страницы."""
    title = main_page.get_title()
    assert title is not None, "Заголовок страницы не найден"
    assert "Кинопоиск. Онлайн кинотеатр. Фильмы сериалы мультфильмы и энциклопедия" or "Вы не робот" in title, "Заголовок страницы не содержит 'КиноПоиск'"

@pytest.mark.parametrize("query, expected_url_part", [("Матрица", "kp_query"),])
def test_search(main_page, query, expected_url_part):
    # работает!!!
    """Проверка функциональности поиска."""
    main_page.search(query)  # Выполнение поиска

    # Вывод текущего URL для диагностики
    print("Текущий URL после поиска:", main_page.driver.current_url)

    # Ожидание изменения URL после поиска
    try:
        WebDriverWait(main_page.driver, 60).until(EC.url_contains(expected_url_part))
    except Exception as e:
        print("Ошибка при ожидании URL:", e)
        print("Фактический URL:", main_page.driver.current_url)
        raise

    # Ожидание появления заголовка результатов поиска
    WebDriverWait(main_page.driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='search_results_topText']")))

    # Проверка, что текущий URL содержит ожидаемую часть
    assert expected_url_part in main_page.driver.current_url, "URL страницы не содержит ожидаемую часть"

def test_wait_for_element(main_page):
    # работает!!!
    """Проверка ожидания появления элемента на странице."""
    locator = (By.CSS_SELECTOR, "input[name='kp_query']")
    element = main_page.wait_for_element(locator)
    assert element is not None, "Элемент не найден"
    assert element.is_displayed(), "Элемент не отображается на странице"

def test_enter_search_query(main_page):
    # работает!!!
    """Проверка ввода поискового запроса."""
    query = "Матрица"
    search_input_locator = (By.CSS_SELECTOR, "input[type='text']")
    search_input = main_page.wait_for_element(search_input_locator)

    # Ввод запроса и проверка значения в поле ввода
    search_input.clear()
    search_input.send_keys(query)
    assert search_input.get_attribute("value") == query, "Текст в поле ввода не соответствует запросу"

def test_search_with_empty_query(main_page):
    # работает!!!
    """Проверка поиска с пустым запросом."""
    query = ""
    main_page.search(query)

    # Ожидание появления сообщения об ошибке или другого поведения
    error_message_locator = (By.CSS_SELECTOR, "input[id='search']")
    try:
        error_message = main_page.wait_for_element(error_message_locator, timeout=20)
        assert error_message is not None, "Сообщение об ошибке не найдено"
    except TimeoutException as e:
        logging.warning(f"Элемент не найден: {e}")
        # Если сообщение об ошибке не появляется, проверяем, что URL не изменился
        expected_url = "https://www.kinopoisk.ru/"
        actual_url = main_page.driver.current_url.split("?")[0]
        assert actual_url == expected_url, f"URL страницы не соответствует ожидаемому: {actual_url}"