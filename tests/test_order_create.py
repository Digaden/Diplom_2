import allure
from utils.api_client import ApiClient
from utils.data_generator import generate_user

@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.story("С авторизацией")
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, ingredients, auth_headers):
        api = ApiClient(base_url=BASE_URL)
        payload = {"ingredients": ingredients[:2]}
        with allure.step("Отправка запроса на создание заказа с авторизацией"):
            r = api.post("/orders", payload, headers=auth_headers)
        
        assert r.status_code in (200, 201), f"Create order with auth failed: {r.status_code} {r.text}"
        body = r.json()
        assert "order" in body or "name" in body.get("order", {}), f"Unexpected order structure: {body}"

    @allure.story("Без авторизации")
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, ingredients):
        api = ApiClient(base_url=BASE_URL)
        payload = {"ingredients": ingredients[:2]}
        with allure.step("Отправка запроса на создание заказа без авторизации"):
            r = api.post("/orders", payload)
        
        assert r.status_code in (200, 201, 401, 403), f"Unexpected status for unauth order: {r.status_code} {r.text}"
        body = r.json()
        assert (r.status_code in (200, 201) and body.get("order")) or body.get("success") is False, f"Unexpected response body: {body}"

    @allure.story("С ингредиентами (позитивный)")
    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, ingredients):
        api = ApiClient(base_url=BASE_URL)
        payload = {"ingredients": ingredients[:2]}
        with allure.step("Отправка запроса на создание заказа с ингредиентами"):
            r = api.post("/orders", payload)
        
        assert r.status_code in (200, 201), f"Create order failed: {r.status_code} {r.text}"
        body = r.json()
        assert body.get("order"), f"Expected order response, got: {body}"

    @allure.story("Без ингредиентов (негативный)")
    @allure.title("Попытка создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self, api):
        api = ApiClient(base_url=BASE_URL)
        payload = {"ingredients": []}
        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            r = api.post("/orders", payload)
        
        assert r.status_code == 400, f"Expected 400 for empty ingredients, got {r.status_code}: {r.text}"
        body = r.json()
        assert body.get("success") is False, f"Expected success False for empty ingredients, got: {body}"

    @allure.story("С неверным хешем ингредиентов (негативный)")
    @allure.title("Попытка создать заказ с неверным ID ингредиента")
    def test_create_order_invalid_hash(self, api):
        api = ApiClient(base_url=BASE_URL)
        payload = {"ingredients": ["invalid_id_12345"]}
        with allure.step("Отправка запроса на создание заказа с неверным ID ингредиента"):
            r = api.post("/orders", payload)

        assert r.status_code in (400, 422, 500), f"Unexpected status for invalid ingredient hash: {r.status_code}: {r.text}"
        body = r.json()
        assert body.get("success") is False, f"Expected success False for invalid ingredient ID, got: {body}"