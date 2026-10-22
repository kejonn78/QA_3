from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def demo_login():
    # Запуск драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")

    print("\n===== ЛОКАТОРЫ НА SAUCEDEMO =====")

    # 1. По ID — поле username
    username = driver.find_element(By.ID, "user-name")
    username.send_keys("standard_user")
    print("✅ По ID: поле username найдено")

    # 2. По ID — поле password
    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")
    print("✅ По ID: поле password найдено")

    # 3. По ID — кнопка Login
    login_btn = driver.find_element(By.ID, "login-button")
    print(f"✅ По ID: кнопка '{login_btn.get_attribute('value')}' найдена")

    # Нажимаем кнопку Login
    login_btn.click()
    time.sleep(2)  # ждём загрузки страницы товаров

    # 10. Альтернативный вариант — через XPath (правильный синтаксис)
    # Находим кнопку у первого элемента с классом inventory_item
    add_btn_xpath = driver.find_element(By.XPATH, "(//div[@class='inventory_item'])[1]//button")
    print(f"✅ По XPath (правильный): кнопка '{add_btn_xpath.text}'")

    # Добавить первый товар в корзину
    add_to_cart = driver.find_element(By.XPATH, '//button[text()="Add to cart"]')
    add_to_cart.click()

    # Получить текст цены первого товара
    price_text = driver.find_element(
        By.XPATH,
        "//div[contains(@class, 'inventory_item_price')][1]"
    ).text
    print(f"Цена первого товара: {price_text}")


    # Небольшая пауза, чтобы увидеть результат
    time.sleep(3)
    driver.quit()

if __name__ == "__main__":
    demo_login()