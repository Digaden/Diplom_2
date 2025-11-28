import allure
from utils.data_generator import generate_user
from utils.api_client import ApiClient
from utils.urls import BASE_URL

@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.story("Успешный логин")
    @allure.title("Проверка статус-кода и тела ответа при корректном логине")
    def test_status_login_valid(self):
        """Проверка статус-кода и тела ответа при корректном логине (200)."""
        api = ApiClient(base_url=BASE_URL)  # Создаем ApiClient здесь
        user = generate_user()
        api.post("/auth/register", user)

        with allure.step("Отправка запроса на логин"):
            r = api.post("/auth/login", {"email": user["email"], "password": user["password"]})

        with allure.step("Проверка статус-кода"):
            assert r.status_code == 200, f"Expected 200, got {r.status_code}"

        with allure.step("Проверка тела ответа"):
            body = r.json()
            assert body.get("accessToken"), "No accessToken found"
            assert body.get("user", {}).get("email") == user["email"], f"Expected {user['email']}, got {body}"

    @allure.story("Логин с неверными данными")
    @allure.title("Проверка статус-кода и тела ответа при неверных учетных данных")
    def test_status_login_invalid(self):
        """Проверка статус-кода и тела ответа при неверных учетных данных (401/403)."""
        api = ApiClient(base_url=BASE_URL)  # Создаем ApiClient здесь

        with allure.step("Отправка запроса на логин с неверными данными"):
            r = api.post("/auth/login", {"email": "wrong@example.com", "password": "wrongpass"})

        with allure.step("Проверка статус-кода"):
            assert r.status_code in (401, 403), f"Expected 401/403, got {r.status_code}"

        with allure.step("Проверка тела ответа"):
            body = r.json()
            assert body.get("success") is False, f"Expected success=False, got {body}"