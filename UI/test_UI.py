import pytest
from selenium import webdriver
from pytest_ui_api_template.UI.pages.MainPage import MainPage
from selenium.webdriver.common.by import By


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_search(driver):
    main_page = MainPage(driver)
    main_page.open()
    main_page.search("Брат 2")
    print(main_page.get_search_result())


def test_open_main_page(driver):
    main_page = MainPage(driver)
    main_page.open()

    # Проверка заголовка страницы
    assert "КиноПоиск" in driver.title, "Заголовок страницы не соответствует ожидаемому"


def test_search_input_is_displayed(driver):
    main_page = MainPage(driver)
    main_page.open()

    # Проверка, что поле поиска отображается
    search_input = main_page.wait_for_element(main_page.search_input_locator)
    assert search_input.is_displayed(), "Поле поиска не отображается"


def test_enter_search_query(driver):
    main_page = MainPage(driver)
    main_page.open()

    # Ввод текста в поле поиска
    test_query = "Брат 2"
    main_page.enter_search_query(test_query)

    # Проверка, что текст введен корректно
    search_input = main_page.wait_for_element(main_page.search_input_locator)
    assert search_input.get_attribute("value") == test_query, "Текст в поле поиска не соответствует ожидаемому"


def test_clear_search_input(driver):
    main_page = MainPage(driver)
    main_page.open()

    # Ввод текста и очистка поля
    main_page.enter_search_query("Брат 2")
    search_input = main_page.wait_for_element(main_page.search_input_locator)
    search_input.clear()

    # Проверка, что поле пустое
    assert search_input.get_attribute("value") == "", "Поле поиска не очищено"


def test_search_results(driver):
    main_page = MainPage(driver)
    main_page.open()

    # Ввод текста и выполнение поиска
    test_query = "Брат 2"
    main_page.search(test_query)

    # Ожидание появления результатов поиска
    results_locator = (By.CSS_SELECTOR, "div.search_results")  # Пример локатора для результатов поиска
    results = main_page.wait_for_element(results_locator)

    # Проверка, что результаты поиска отображаются
    assert results.is_displayed(), "Результаты поиска не отображаются"


def test_search_results_content(driver):
    main_page = MainPage(driver)
    main_page.open()

    # Ввод текста и выполнение поиска
    test_query = "Брат 2"
    main_page.search(test_query)

    # Ожидание появления результатов поиска
    results_locator = (By.CSS_SELECTOR, "div.search_results")  # Пример локатора для результатов поиска
    results = main_page.wait_for_element(results_locator)

    # Проверка, что результаты содержат искомый запрос
    assert test_query in results.text, "Результаты поиска не содержат искомый запрос"


def test_invalid_search_query(driver):
    main_page = MainPage(driver)
    main_page.open()

    # Ввод недопустимого запроса
    invalid_query = "!@#$%^&*()"
    main_page.enter_search_query(invalid_query)

    # Проверка, что поле поиска содержит введенный текст
    search_input = main_page.wait_for_element(main_page.search_input_locator)
    assert search_input.get_attribute("value") == invalid_query, "Недопустимый запрос не был введен"


def test_empty_search_query(driver):
    main_page = MainPage(driver)
    main_page.open()

    # Ввод пустого запроса
    main_page.enter_search_query("")

    # Проверка, что поле поиска пустое
    search_input = main_page.wait_for_element(main_page.search_input_locator)
    assert search_input.get_attribute("value") == "", "Поле поиска не пустое"


def test_long_search_query(driver):
    main_page = MainPage(driver)
    main_page.open()

    # Ввод длинного запроса
    # long_query = "гринч" *