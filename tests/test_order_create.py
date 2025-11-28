import sys
import pathlib
import allure
import pytest
from utils.urls import BASE_URL
from utils.api_client import ApiClient

# Если нужно, добавьте корень проекта в sys.path (на случай нестандартной конфигурации запуска)
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.story("С авторизацией")
    @allure.title("Проверка статус-кода и тела ответа при создании заказа с авторизацией")
    def test_status_create_order_with_auth(self, ingredients, auth_headers):
        """Проверка статус-кода и тела ответа при создании заказа с авторизацией (200/201 по документации)."""
        api = ApiClient(base_url=BASE_URL)  # Создаем ApiClient здесь
        payload = {"ingredients": ingredients[:2]}

        with allure.step("Отправка запроса на создание заказа"):
            r = api.post("/orders", payload, headers=auth_headers)

        with allure.step("Проверка статус-кода"):
            assert r.status_code in (200, 201), f"Expected status 200/201, got {r.status_code}"

        with allure.step("Проверка тела ответа"):
            body = r.json()
            assert "order" in body, f"Expected 'order' key in response, got {body}"
            assert isinstance(body["order"], dict), "Order should be a dict"
            assert "name" in body["order"], "'name' key not found in order"

    @allure.story("Без ингредиентов (негатив)")
    @allure.title("Проверка статус-кода и тела ответа при попытке создать заказ без ингредиентов")
    def test_status_create_order_without_ingredients(self):
        """Проверка статус-кода и тела ответа при попытке создать заказ без ингредиентов (400)."""
        api = ApiClient(base_url=BASE_URL)  # Создаем ApiClient здесь

        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            r = api.post("/orders", {"ingredients": []})

        with allure.step("Проверка статус-кода"):
            assert r.status_code == 400, f"Expected 400, got {r.status_code}"

        with allure.step("Проверка тела ответа"):
            body = r.json()
            assert body.get("success") is False, f"Expected success=False, got {body}"