import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        url_auth = "https://playground.learnqa.ru/api/user/login"

        response = requests.post(url_auth, data=data)

        self.auth_sid = self.get_cookie(response, "auth_sid")
        self.token = self.get_header(response, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response, "user_id")

    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        response = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id_from_auth_method}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response, expected_fields)

    def test_get_user_details_auth_another_user(self):
        another_user = self.user_id_from_auth_method - 1
        response = requests.get(
            f"https://playground.learnqa.ru/api/user/{another_user}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_has_key(response, "username")

        expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response,expected_fields)
