import allure
from utils.data_generator import generate_user
from utils.api_client import ApiClient
from utils.urls import BASE_URL

@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.story("Вход под существующим пользователем")
    @allure.title("Успешный вход под существующим пользователем")
    def test_login_valid(self):
        user = generate_user()

        api = ApiClient(base_url=BASE_URL)

        with allure.step("Регистрация пользователя"):
            reg = api.post("/auth/register", user)
            assert reg.status_code in (200, 201), f"Register failed: {reg.status_code} {reg.text}"

        with allure.step("Попытка входа с корректными учетными данными"):
            login_response = api.post("/auth/login", {"email": user["email"], "password": user["password"]})
            assert login_response.status_code == 200, f"Login failed for valid user: {login_response.status_code} {login_response.text}"

            body = login_response.json()
            assert body.get("accessToken") is not None, f"No accessToken in login response: {body}"
            assert body.get("user", {}).get("email") == user["email"], f"Expected email {user['email']} in login response, got: {body}"

    @allure.story("Вход с неверным логином и паролем")
    @allure.title("Попытка входа с неверными учетными данными")
    def test_login_invalid(self):
        api = ApiClient(base_url=BASE_URL)

        with allure.step("Попытка входа с неверными учетными данными"):
            response = api.post("/auth/login", {"email": "wrong@example.com", "password": "wrongpass"})
            assert response.status_code in (401, 403), f"Expected auth error for wrong credentials, got {response.status_code}: {response.text}"

            body = response.json()
            assert body.get("success") is False, f"Expected success False for invalid login, got: {body}"