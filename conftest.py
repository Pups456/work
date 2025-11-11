import pytest
from selenium import webdriver

# Добавление опции --language в командную строку
def pytest_addoption(parser):
    parser.addoption('--language',
                     action='store',
                     default='en',
                     help="Choose language: es, fr, de, etc.")


# Фикстура для инициализации браузера с поддержкой разных языков
@pytest.fixture(scope="function")
def browser(request):
    language = request.config.getoption("language")
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': language})
    browser = webdriver.Chrome(options=options)

    yield browser
    browser.quit()

# Фикстура для получения выбранного языка
@pytest.fixture
def language(request):
    return request.config.getoption("language")
