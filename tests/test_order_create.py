import allure
from utils.data_generator import generate_user

@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.story("С авторизацией")
    def test_create_order_with_auth(self, api, ingredients, auth_headers):
        # ингредиенты берём из фикстуры
        payload = {"ingredients": ingredients[:2]}
        r = api.post("/orders", payload, headers=auth_headers)
        assert r.status_code in (200, 201), f"Create order with auth failed: {r.status_code} {r.text}"
        body = r.json()
        assert body.get("success") is True, f"Expected success True: {body}"
        # опциональная проверка на номер заказа/структуру
        assert "order" in body or "name" in body or "order" in body.get("order", {}), f"Unexpected order structure: {body}"

    @allure.story("Без авторизации")
    def test_create_order_without_auth(self, api, ingredients):
        payload = {"ingredients": ingredients[:2]}
        r = api.post("/orders", payload)
        # в некоторых реализациях заказ можно создать без авторизации -> 200, иначе 401/403
        assert r.status_code in (200, 201, 401, 403), f"Unexpected status for unauth order: {r.status_code} {r.text}"
        body = r.json()
        # если сервис поддерживает анонимный заказ — success True, иначе False
        if r.status_code in (200, 201):
            assert body.get("success") is True, f"Expected success True for unauth order (service allows): {body}"
        else:
            assert body.get("success") is False, f"Expected success False for unauth order (not allowed): {body}"

    @allure.story("С ингредиентами (позитивный)")
    def test_create_order_with_ingredients(self, api, ingredients):
        payload = {"ingredients": ingredients[:2]}
        r = api.post("/orders", payload)
        assert r.status_code in (200, 201), f"Create order failed: {r.status_code} {r.text}"
        body = r.json()
        assert body.get("success") is True, f"Expected success True: {body}"

    @allure.story("Без ингредиентов (негативный)")
    def test_create_order_without_ingredients(self, api):
        payload = {"ingredients": []}
        r = api.post("/orders", payload)
        # по доке ожидается 400
        assert r.status_code == 400, f"Expected 400 for empty ingredients, got {r.status_code}: {r.text}"
        body = r.json()
        assert body.get("success") is False, f"Expected success False for empty ingredients, got: {body}"

    @allure.story("С неверным хешем ингредиентов (негативный)")
    def test_create_order_invalid_hash(self, api):
        payload = {"ingredients": ["invalid_id_12345"]}
        r = api.post("/orders", payload)
        # сервер может вернуть 400 (validation) либо 500 (if backend fails) — отметим оба как ожидаемые клиентские/серверные ошибки
        assert r.status_code in (400, 422, 500), f"Unexpected status for invalid ingredient hash: {r.status_code}: {r.text}"
        body = r.json()
        # Если backend вернул success True при неверных id — это баг; требуем success False
        assert body.get("success") is False, f"Expected success False for invalid ingredient id, got: {body}"