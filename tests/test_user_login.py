import allure
from utils.data_generator import generate_user
from utils.api_client import ApiClient
from utils.urls import BASE_URL

@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.story("Успешный логин")
    def test_status_login_valid(self):
        """Проверка статус-кода при корректном логине (200)."""
        api = ApiClient(base_url=BASE_URL)
        user = generate_user()
        api.post("/auth/register", user)
        r = api.post("/auth/login", {"email": user["email"], "password": user["password"]})
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"

    @allure.story("Успешный логин")
    def test_body_login_valid(self):
        """Проверка тела ответа при корректном логине."""
        api = ApiClient(base_url=BASE_URL)
        user = generate_user()
        api.post("/auth/register", user)
        r = api.post("/auth/login", {"email": user["email"], "password": user["password"]})
        body = r.json()
        assert body.get("accessToken"), "No accessToken found"
        assert body.get("user", {}).get("email") == user["email"], f"Expected {user['email']}, got {body}"

    @allure.story("Логин с неверными данными")
    def test_status_login_invalid(self):
        """Проверка статус-кода при неверных учетных данных (401/403)."""
        api = ApiClient(base_url=BASE_URL)
        r = api.post("/auth/login", {"email": "wrong@example.com", "password": "wrongpass"})
        assert r.status_code in (401, 403), f"Expected 401/403, got {r.status_code}"

    @allure.story("Логин с неверными данными")
    def test_body_login_invalid(self):
        """Проверка тела ответа при неверных учетных данных."""
        api = ApiClient(base_url=BASE_URL)
        r = api.post("/auth/login", {"email": "wrong@example.com", "password": "wrongpass"})
        body = r.json()
        assert body.get("success") is False, f"Expected success=False, got {body}"