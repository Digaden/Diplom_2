import requests

class ApiClient:
    def __init__(self, base_url="https://stellarburgers.education-services.ru/"):
        self.base_url = base_url.rstrip("/")

    def _url(self, path):
        if path.startswith("/"):
            path = path[1:]
        return f"{self.base_url}/{path}"

    def get(self, path, params=None, headers=None):
        return requests.get(self._url(path), params=params, headers=headers)

    def post(self, path, json=None, headers=None):
        return requests.post(self._url(path), json=json, headers=headers)

    def delete(self, path, headers=None):
        return requests.delete(self._url(path), headers=headers)