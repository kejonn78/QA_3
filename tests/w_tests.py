import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    print("Инициализация драйвера Chrome...")
    driver = webdriver.Chrome()
    yield driver
    print("Закрытие браузера...")
    driver.quit()

@pytest.fixture
def wait(driver):
    print("Создание объекта ожидания (таймаут 10 с)...")
    return WebDriverWait(driver, 10)

# Тест 1: Проверка успешного сценария покупки товара
def test_successful_purchase(driver, wait):
    """
    Сценарий: полный цикл покупки от авторизации до подтверждения заказа.
    Ожидаемый результат: появление сообщения «Thank you for your order!».
    """

    print("\n=== ТЕСТ 1: Успешная покупка ===")

    # Шаг 1: Авторизация с валидными учётными данными
    print("Шаг 1: Открываем страницу авторизации...")
    driver.get("https://www.saucedemo.com")

    print("Ожидание поля ввода логина...")
    username_input = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    print("Ввод учётных данных...")
    username_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    print("Нажатие кнопки входа...")
    login_button.click()

    # Шаг 2: Выбор товара и добавление в корзину
    print("Шаг 2: Ожидание кнопки добавления товара в корзину...")
    add_to_cart_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".inventory_item:first-child .btn_primary"))
    )
    print("Добавление первого товара в корзину...")
    add_to_cart_button.click()

    # Шаг 3: Переход в корзину и оформление покупки
    print("Шаг 3: Переход в корзину...")
    cart_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
    cart_link.click()

    print("Нажатие кнопки Checkout...")
    checkout_button = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
    checkout_button.click()

    # Шаг 4: Заполнение данных для оформления заказа
    print("Шаг 4: Ожидание поля ввода имени...")
    first_name_input = wait.until(EC.presence_of_element_located((By.ID, "first-name")))
    last_name_input = driver.find_element(By.ID, "last-name")
    postal_code_input = driver.find_element(By.ID, "postal-code")
    continue_button = driver.find_element(By.ID, "continue")

    print("Заполнение данных заказа...")
    first_name_input.send_keys("Test")
    last_name_input.send_keys("User")
    postal_code_input.send_keys("12345")
    print("Продолжение оформления заказа...")
    continue_button.click()

    # Шаг 5: Подтверждение заказа
    print("Шаг 5: Ожидание кнопки завершения заказа...")
    finish_button = wait.until(EC.element_to_be_clickable((By.ID, "finish")))
    print("Подтверждение заказа...")
    finish_button.click()

    # Шаг 6: Проверка успешного завершения
    print("Шаг 6: Ожидание сообщения об успешном заказе...")
    success_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))
    print(f"Получено сообщение: '{success_message.text}'")
    assert "Thank you for your order!" in success_message.text
    print("ТЕСТ 1 ПРОЙДЕН: заказ успешно оформлен!")

# Тест 2: Проверка очистки корзины от товаров
def test_clear_cart(driver, wait):
    """
    Сценарий: добавление нескольких товаров в корзину, их удаление и проверка пустого состояния корзины.
    Ожидаемый результат: корзина пуста, пользователь возвращается на страницу каталога.
    """

    print("\n=== ТЕСТ 2: Очистка корзины ===")

    # Шаг 1: Авторизация
    print("Шаг 1: Открываем страницу авторизации...")
    driver.get("https://www.saucedemo.com")

    username_input = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    print("Ввод учётных данных...")
    username_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    print("Нажатие кнопки входа...")
    login_button.click()

    # Шаг 2: Добавление товаров в корзину
    print("Шаг 2: Ожидание кнопок добавления товаров...")
    add_to_cart_buttons = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".btn_primary"))
    )
    print("Добавление первых двух товаров в корзину...")
    for button in add_to_cart_buttons[:2]:
        button.click()

    # Шаг 3: Открытие корзины
    print("Шаг 3: Переход в корзину...")
    cart_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
    cart_link.click()

    # Шаг 4: Удаление товаров из корзины
    print("Шаг 4: Поиск кнопок удаления товаров...")
    remove_buttons = driver.find_elements(By.CSS_SELECTOR, ".cart_button")
    print(f"Найдено кнопок удаления: {len(remove_buttons)}")
    for i, button in enumerate(remove_buttons, 1):
        print(f"Удаление товара {i} из корзины...")
        button.click()

    # Шаг 5: Проверка, что корзина пуста
    print("Шаг 5: Ожидание исчезновения товаров из корзины...")
    empty_cart_indicator = wait.until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "cart_item"))
    )
    assert empty_cart_indicator is True
    print("Корзина успешно очищена!")

    # Шаг 6: Проверка возврата на страницу выбора товаров
    print("Шаг 6: Возврат на страницу каталога...")
    continue_shopping_button = wait.until(
        EC.element_to_be_clickable((By.ID, "continue-shopping"))
    )
    continue_shopping_button.click()
    current_url = driver.current_url
    print(f"Текущий URL: {current_url}")
    assert "inventory" in current_url
    print("ТЕСТ 2 ПРОЙДЕН: пользователь вернулся на страницу каталога!")

# Тест 3: Проверка обработки ошибки при авторизации
def test_failed_login(driver, wait):
    """
    Сценарий: попытка входа с неверными учётными данными.
    Ожидаемый результат: отображение сообщения об ошибке с текстом «Epic sadface...».
    """

    print("\n=== ТЕСТ 3: Неуспешная авторизация ===")

    # Шаг 1: Попытка входа с неправильными данными
    print("Шаг 1: Открываем страницу авторизации...")
    driver.get("https://www.saucedemo.com")

    username_input = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    print("Ввод неверных учётных данных...")
    username_input.send_keys("invalid_user")
    password_input.send_keys("wrong_password")
    print("Нажатие кнопки входа...")
    login_button.click()

    # Шаг 2: Проверка появления сообщения об ошибке
    print("Шаг 2: Ожидание сообщения об ошибке...")
    error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message-container")))
    expected_error = "Epic sadface: Username and password do not match any user in this service"
    print(f"Получено сообщение об ошибке: '{error_message.text}'")
    assert expected_error in error_message.text
    print("ТЕСТ 3 ПРОЙДЕН: корректно отображено сообщение об ошибке!")