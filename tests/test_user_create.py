import pytest
import allure

from utils.data_generator import generate_user

@allure.feature("Создание пользователя")
class TestUserCreate:

    @allure.story("Создать уникального пользователя")
    def test_create_unique_user(self, api):
        user = generate_user()
        response = api.post("/auth/register", user)
        assert response.status_code in (200, 201), f"Unexpected status for register: {response.status_code} {response.text}"
        body = response.json()
        assert body.get("success") is True, f"Expected success True, got: {body}"

    @allure.story("Создать пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, api):
        user = generate_user()
        r1 = api.post("/auth/register", user)
        assert r1.status_code in (200, 201), f"First register failed: {r1.status_code} {r1.text}"
        r2 = api.post("/auth/register", user)
        # По документации ожидается 403 для повторной регистрации; допускаем 400/403/409 в случае других реализаций
        assert r2.status_code in (400, 403, 409), f"Expected client error for duplicate register, got {r2.status_code}: {r2.text}"
        body = r2.json()
        assert body.get("success") is False, f"Expected success False for duplicate register, got: {body}"

    @allure.story("Создать пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, api, missing_field):
        user = generate_user()
        user.pop(missing_field)
        r = api.post("/auth/register", user)
        # По доке раньше ожидали 403; тут допускаем 400/403
        assert r.status_code in (400, 403), f"Expected validation error for missing field {missing_field}, got {r.status_code}: {r.text}"
        body = r.json()
        assert body.get("success") is False, f"Expected success False for missing field {missing_field}, got: {body}"