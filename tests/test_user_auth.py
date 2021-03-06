import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Authorization cases")
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
        url_auth = "/user/login"
        with allure.step(f'Auth to account {data["email"]}'):
            response = MyRequests.post(url_auth, data=data)

        self.auth_sid = self.get_cookie(response, "auth_sid")
        self.token = self.get_header(response, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response, "user_id")

    @allure.description("This test successfully authorize user by email and password")
    @allure.title("Test authorization user vinkotov@example.com")
    @allure.link('https://github.com', name='git')
    @allure.issue('140', name='Bug tracker link')
    @allure.testcase('https://jira.lucky.com', name='Test case title')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Story 1")
    def test_auth_user(self):
        url_auth_check = "/user/auth"

        with allure.step('Check authorization to account'):
            response = MyRequests.get(
                url_auth_check,
                headers={"x-csrf-token": self.token},
                cookies={"auth_sid": self.auth_sid}
            )
        with allure.step('Assertion that authorization to correct user'):
            Assertions.assert_json_value_by_name(
                response,
                "user_id",
                self.user_id_from_auth_method,
                "User id from auth method is not equal to user id from check method"
            )

    @allure.description("This test checks authorization status w/o sending auth cookie")
    @allure.title("Negative test authorization with {condition}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('condition', exclude_params)
    @allure.story("Story 2")
    @allure.feature('Feature')
    def test_negative_auth_check(self, condition):
        url_auth_check = "/user/auth"
        if condition == "no_cookie":
            response = MyRequests.get(url_auth_check, headers={"x-csrf-token": self.token})
        else:
            response = MyRequests.get(url_auth_check, cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
