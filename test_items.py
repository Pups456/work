# Задание: запуск автотестов для разных языков интерфейса
# https://stepik.org/lesson/237240/step/10?unit=209628

# использует - conftest.py — конфигурация тестов


### Запуск позитивных тестов, осуществляется проверка названия кнопки
# pytest --language=fr test_items.py
# pytest --language=es test_items.py
# pytest --language=de test_items.py
# pytest --language=ru test_items.py

### Запуск негативных тестов, название кнопки НЕ совпадает с условием
# pytest --language=it test_items.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def test_language_parameter(browser, language):
    link = "http://selenium1py.pythonanywhere.com/"+language+"/"
    browser.get(link)
    time.sleep(1)
    browser.get("http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/")
    time.sleep(3)

    # Если кнопка "Добавить в корзину" присутствует
    button_add_to_basket = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#add_to_basket_form > button")))

    # Сравниваем, что фидбек для --language=fr полностью совпадает с "Ajouter au panier!"
    if language == 'fr':
        assert button_add_to_basket.text == "Ajouter au panier", f"{button_add_to_basket.text}"
    elif language == 'es':
        assert button_add_to_basket.text == "Añadir al carrito", f"{button_add_to_basket.text}"
    elif language == 'de':
        assert button_add_to_basket.text == "In Warenkorb legen", f"{button_add_to_basket.text}"
    elif language == 'ru':
        assert button_add_to_basket.text == "Добавить в корзину", f"{button_add_to_basket.text}"
    else:
        assert button_add_to_basket.text == "Добавить в корзину", f"Для языка: '{language}' кнопка " \
                                                                  f"называется: '{button_add_to_basket.text}'"
