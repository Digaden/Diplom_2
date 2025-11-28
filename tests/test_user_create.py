import allure
import pytest
from utils.data_generator import generate_user
from utils.api_client import ApiClient
from utils.urls import BASE_URL

@allure.feature("Создание пользователя")
class TestUserCreate:

    @allure.story("Уникальный пользователь")
    @allure.title("Проверка статус-кода и тела ответа при создании нового пользователя")
    def test_status_create_unique_user(self):
        """Проверка статус-кода и тела ответа при создании нового пользователя (200/201)."""
        api = ApiClient(base_url=BASE_URL)  # Создаем ApiClient здесь
        user = generate_user()

        with allure.step("Отправка запроса на создание нового пользователя"):
            r = api.post("/auth/register", user)

        with allure.step("Проверка статус-кода"):
            assert r.status_code in (200, 201), f"Expected 200/201, got {r.status_code}"

        with allure.step("Проверка тела ответа"):
            body = r.json()
            assert body.get("user", {}).get("email") == user["email"], f"Expected {user['email']}, got {body}"

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.story("Отсутствие обязательного поля")
    @allure.title("Проверка статус-кода и тела ответа при отсутствии обязательного поля")
    def test_status_create_user_missing_field(self, missing_field):
        """Проверка статус-кода и тела ответа при отсутствии обязательного поля (400/403)."""
        api = ApiClient(base_url=BASE_URL)  # Создаем ApiClient здесь
        user = generate_user()
        user.pop(missing_field)

        with allure.step("Отправка запроса на создание пользователя с отсутствующим полем"):
            r = api.post("/auth/register", user)

        with allure.step("Проверка статус-кода"):
            assert r.status_code in (400, 403), f"Expected 400/403, got {r.status_code}"

        with allure.step("Проверка тела ответа"):
            body = r.json()
            assert body.get("success") is False, f"Expected success=False for missing {missing_field}, got {body}"