import pytest
import allure
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

@allure.suite("Тестирование функционала интернет магазина")
class TestShopFunctionality:

    @allure.title("Тест 1: Успешная покупка товара")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("epic", "Покупка товара")
    @allure.label("feature", "Оформление заказа")
    def test_successful_purchase(self, driver, wait):
        """
        Сценарий: полный цикл покупки от авторизации до подтверждения заказа.
        Ожидаемый результат: появление сообщения «Thank you for your order!».
        """

        @allure.step("Шаг 1: Авторизация с валидными учётными данными")
        def login_step():
            print("Открываем страницу авторизации...")
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
        login_step()

        @allure.step("Шаг 2: Выбор товара и добавление в корзину")
        def add_to_cart_step():
            print("Ожидание кнопки добавления товара в корзину...")
            add_to_cart_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".inventory_item:first-child .btn_primary"))
            )
            print("Добавление первого товара в корзину...")
            add_to_cart_button.click()
        add_to_cart_step()

        @allure.step("Шаг 3: Переход в корзину и оформление покупки")
        def checkout_step():
            print("Переход в корзину...")
            cart_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
            cart_link.click()

            print("Нажатие кнопки Checkout...")
            checkout_button = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
            checkout_button.click()
        checkout_step()

        @allure.step("Шаг 4: Заполнение данных для оформления заказа")
        def fill_order_data_step():
            print("Ожидание поля ввода имени...")
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
        fill_order_data_step()

        @allure.step("Шаг 5: Подтверждение заказа")
        def confirm_order_step():
            print("Ожидание кнопки завершения заказа...")
            finish_button = wait.until(EC.element_to_be_clickable((By.ID, "finish")))
            print("Подтверждение заказа...")
            finish_button.click()
        confirm_order_step()

        @allure.step("Шаг 6: Проверка успешного завершения")
        def verify_success_step():
            print("Ожидание сообщения об успешном заказе...")
            success_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))
            print(f"Получено сообщение: '{success_message.text}'")
            assert "Thank you for your order!" in success_message.text
            print("ТЕСТ 1 ПРОЙДЕН: заказ успешно оформлен!")
        verify_success_step()

    @allure.title("Тест 2: Очистка корзины от товаров")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("epic", "Управление корзиной")
    @allure.label("feature", "Удаление товаров")
    def test_clear_cart(self, driver, wait):
        # Аналогично добавляем @allure.step для каждого шага теста 2
        pass

    @allure.title("Тест 3: Проверка обработки ошибки при авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("epic", "Авторизация")
    @allure.label("feature", "Обработка ошибок")
    def test_failed_login(self, driver, wait):
        # Аналогично добавляем @allure.step для каждого шага теста 3
        pass
