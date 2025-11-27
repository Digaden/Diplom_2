import allure
import pytest
from utils.api_client import ApiClient
from utils.urls import BASE_URL

@allure.feature("Создание заказа")
class TestOrderCreate:

    @pytest.fixture
    def api(self):
        return ApiClient(base_url=BASE_URL)

    @allure.story("С авторизацией")
    def test_status_create_order_with_auth(self, api, ingredients, auth_headers):
        """Проверка статус-кода при создании заказа с авторизацией (200/201 по документации)."""
        payload = {"ingredients": ingredients[:2]}
        r = api.post("/orders", payload, headers=auth_headers)
        assert r.status_code in (200, 201), f"Expected status 200/201, got {r.status_code}"

    @allure.story("С авторизацией")
    def test_body_create_order_with_auth(self, api, ingredients, auth_headers):
        """Проверка тела ответа при создании заказа с авторизацией."""
        payload = {"ingredients": ingredients[:2]}
        r = api.post("/orders", payload, headers=auth_headers)
        body = r.json()
        assert "order" in body, f"Expected 'order' key in response, got {body}"
        assert isinstance(body["order"], dict), "Order should be a dict"
        assert "name" in body["order"], "'name' key not found in order"

    @allure.story("Без ингредиентов (негатив)")
    def test_status_create_order_without_ingredients(self, api):
        """Проверка статус-кода при попытке создать заказ без ингредиентов (400)."""
        r = api.post("/orders", {"ingredients": []})
        assert r.status_code == 400, f"Expected 400, got {r.status_code}"

    @allure.story("Без ингредиентов (негатив)")
    def test_body_create_order_without_ingredients(self, api):
        """Проверка тела ответа при заказе без ингредиентов."""
        r = api.post("/orders", {"ingredients": []})
        body = r.json()
        assert body.get("success") is False, f"Expected success=False, got {body}"