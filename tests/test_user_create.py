import allure
import pytest
from utils.data_generator import generate_user

@allure.feature("Создание пользователя")
class TestUserCreate:

    @allure.story("Уникальный пользователь")
    def test_status_create_unique_user(self, api):
        """Проверка статус-кода при создании нового пользователя (200/201)."""
        user = generate_user()
        r = api.post("/auth/register", user)
        assert r.status_code in (200, 201), f"Expected 200/201, got {r.status_code}"

    @allure.story("Уникальный пользователь")
    def test_body_create_unique_user(self, api):
        """Проверка тела ответа при создании нового пользователя."""
        user = generate_user()
        r = api.post("/auth/register", user)
        body = r.json()
        assert body.get("user", {}).get("email") == user["email"], f"Expected {user['email']}, got {body}"

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_status_create_user_missing_field(self, api, missing_field):
        """Проверка статус-кода при отсутствии обязательного поля (400/403)."""
        user = generate_user()
        user.pop(missing_field)
        r = api.post("/auth/register", user)
        assert r.status_code in (400, 403), f"Expected 400/403, got {r.status_code}"

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_body_create_user_missing_field(self, api, missing_field):
        """Проверка тела ответа при отсутствии обязательного поля."""
        user = generate_user()
        user.pop(missing_field)
        r = api.post("/auth/register", user)
        body = r.json()
        assert body.get("success") is False, f"Expected success=False for missing {missing_field}, got {body}"