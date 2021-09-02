import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ('no_token')
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        url_auth = "https://playground.learnqa.ru/api/user/login"

        response1 = requests.post(url_auth, data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_auth_user(self):
        url_auth_check = "https://playground.learnqa.ru/api/user/auth"
        response2 = requests.get(
            url_auth_check,
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        url_auth_check = "https://playground.learnqa.ru/api/user/auth"
        if condition == "no_cookie":
            response2 = requests.get(url_auth_check, headers={"x-csrf-token": self.token})
        else:
            response2 = requests.get(url_auth_check, cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
