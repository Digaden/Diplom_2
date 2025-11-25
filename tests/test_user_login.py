import allure
from utils.data_generator import generate_user

@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.story("Вход под существующим пользователем")
    def test_login_valid(self, api):
        user = generate_user()
        # сначала регистрируем
        reg = api.post("/auth/register", user)
        assert reg.status_code in (200, 201), f"Register failed: {reg.status_code} {reg.text}"

        r = api.post("/auth/login", {"email": user["email"], "password": user["password"]})
        assert r.status_code == 200, f"Login failed for valid user: {r.status_code} {r.text}"
        body = r.json()
        assert body.get("success") is True, f"Expected success True on login, got: {body}"
        assert "accessToken" in body and body["accessToken"], f"No accessToken in login response: {body}"

    @allure.story("Вход с неверным логином и паролем")
    def test_login_invalid(self, api):
        r = api.post("/auth/login", {"email": "wrong@example.com", "password": "wrongpass"})
        # По документации ожидается 401
        assert r.status_code in (401, 403), f"Expected auth error for wrong credentials, got {r.status_code}: {r.text}"
        body = r.json()
        assert body.get("success") is False, f"Expected success False for invalid login, got: {body}"