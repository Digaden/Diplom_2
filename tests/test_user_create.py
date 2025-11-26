import allure
import pytest
from utils.api_client import ApiClient
from utils.data_generator import generate_user

@allure.feature("Создание пользователя")
class TestUserCreate:

    @allure.story("Создать уникального пользователя")
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, api):
        user = generate_user()
        with allure.step("Отправка запроса на создание уникального пользователя"):
            response = api.post("/auth/register", user)
            
        assert response.status_code in (200, 201), f"Unexpected status for register: {response.status_code} {response.text}"
        body = response.json()
        assert body.get("user", {}).get("email") == user["email"], f"Expected email {user['email']}, got: {body}"

    @allure.story("Создать пользователя, который уже зарегистрирован")
    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self, api):
        user = generate_user()
        with allure.step("Регистрация первого пользователя"):
            r1 = api.post("/auth/register", user)
            assert r1.status_code in (200, 201), f"First register failed: {r1.status_code} {r1.text}"
        
        with allure.step("Попытка зарегистрировать второго пользователя с теми же данными"):
            r2 = api.post("/auth/register", user)
            assert r2.status_code in (400, 403, 409), f"Expected client error for duplicate register, got {r2.status_code}: {r2.text}"
            body = r2.json()
            assert body.get("success") is False, f"Expected success False for duplicate register, got: {body}"

    @allure.story("Создать пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_missing_field(self, api, missing_field):
        user = generate_user()
        user.pop(missing_field)
        with allure.step(f"Попытка регистрации пользователя без поля {missing_field}"):
            r = api.post("/auth/register", user)
            
        assert r.status_code in (400, 403), f"Expected validation error for missing field {missing_field}, got {r.status_code}: {r.text}"
        body = r.json()
        assert body.get("success") is False, f"Expected success False for missing field {missing_field}, got: {body}"
