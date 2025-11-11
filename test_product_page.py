import pytest
import time
import math
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By

# URL-адрес, на котором был найден баг, помечаем как ожидаемо падающий (xfail)
# На этом шаге нам нужно протестировать новый URL с промо-акцией.
# bugged_link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7" # Закомментируем старый баг
new_year_link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"

# Используем только один URL для этого задания
@pytest.mark.parametrize('link', [
    # Если вы хотите проверить, что код работает и на старом "багнутом" URL, 
    # его можно оставить, но тогда он должен быть XFAIL:
    # pytest.param(bugged_link, marks=pytest.mark.xfail(reason="Bug on offer7: alert math calculation fails")),
    new_year_link 
])
def test_guest_can_add_product_to_basket(browser, link):
    browser.get(link)
    
    # 1. Получаем название и цену товара со страницы
    product_name_on_page = browser.find_element(By.CSS_SELECTOR, ".product_main h1").text
    product_price_on_page = browser.find_element(By.CSS_SELECTOR, ".product_main .price_color").text

    print(f"\n[INFO] Checking product: {product_name_on_page}, Price: {product_price_on_page}")
    
    # 2. Найти и нажать кнопку "Добавить в корзину"
    add_button = browser.find_element(By.CSS_SELECTOR, ".btn-add-to-basket")
    add_button.click()
    
    # 3. Обработка всплывающего окна (alert)
    # На промо-страницах появляется alert с кодом для решения
    solve_quiz_and_get_code(browser)
    
    # 4. Проверка успешного добавления (независимо от данных)
    check_success_messages(browser, product_name_on_page, product_price_on_page)


def solve_quiz_and_get_code(browser):
    """
    Метод для решения математического примера в alert и его принятия.
    """
    try:
        alert = browser.switch_to.alert
        x = alert.text.split(" ")[2] # Извлекаем X из текста (например, "Please enter answer (X):")
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        print(f"[ALERT HANDLED] Solved math quiz.")
    except NoAlertPresentException:
        print("[INFO] No alert present.")
        pass # Если alert не появился, просто продолжаем


def check_success_messages(browser, expected_name, expected_price):
    """
    Метод, который вытаскивает название и цену из сообщений об успехе и сравнивает их 
    с ожидаемыми (полученными со страницы).
    """
    # 1. Проверяем, что название товара в сообщении совпадает с заголовком товара
    success_message_name = browser.find_element(
        By.CSS_SELECTOR, "#messages .alert-success:nth-child(1) strong"
    ).text
    
    assert expected_name == success_message_name, \
        f"FAILURE: Product name in success message is incorrect. Expected: '{expected_name}', Got: '{success_message_name}'"
    
    # 2. Проверяем, что цена в сообщении совпадает с ценой на странице
    success_message_price = browser.find_element(
        By.CSS_SELECTOR, "#messages .alert-info strong" # Второе сообщение об успехе содержит цену
    ).text
    
    assert expected_price == success_message_price, \
        f"FAILURE: Product price in success message is incorrect. Expected: '{expected_price}', Got: '{success_message_price}'"
        
    print("[SUCCESS] All product name and price checks passed.")
