import sys
import pathlib
import pytest

# Если нужно, добавьте корень проекта в sys.path (на случай нестандартной конфигурации запуска)
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.api_client import ApiClient


@pytest.fixture(scope="session")
def api():
    # Указываем базовый URL согласно документации
    return ApiClient(base_url="https://stellarburgers.education-services.ru/")


@pytest.fixture()
def ingredients(api):
    r = api.get("/ingredients")
    assert r.status_code == 200, f"GET /ingredients failed: {r.status_code} {r.text}"
    data = r.json().get("data") or []
    assert data, f"Ingredients data is empty: {r.text}"
    return [item["_id"] for item in data]