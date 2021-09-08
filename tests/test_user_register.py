from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserRegister(BaseCase):
    url_register = "/user/"
    exclude_params = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]

    def setup(self):
        self.base_part = "learnqa"
        self.domain = "example.com"
        self.random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{self.base_part}{self.random_part}@{self.domain}"

        self.data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
        }

    def test_create_user_successfully(self):
        self.data['email'] = self.email

        response = MyRequests.post(self.url_register, data=self.data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        self.data['email'] = email

        response = MyRequests.post(self.url_register, data=self.data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_answer_text(response, f"Users with email '{email}' already exists")

    def test_incorrect_email_without_at(self):
        email = f"{self.base_part}{self.random_part}{self.domain}"
        self.data['email'] = email

        response = MyRequests.post(self.url_register, data=self.data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_answer_text(response, "Invalid email format")

    @pytest.mark.parametrize('condition', exclude_params)
    def test_without_some_params(self, condition):
        self.data['email'] = self.email

        del self.data[condition]

        response = MyRequests.post(self.url_register, data=self.data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_answer_text(response, f"The following required params are missed: {condition}")

    def test_with_short_email(self):
        self.data['email'] = 'q'

        response = MyRequests.post(self.url_register, data=self.data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_answer_text(response, "The value of 'email' field is too short")

    def test_with_long_email(self):
        self.data['email'] = 'testtestlooooooooooooooooooooooooooooooooooooooooooooooongloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooongloooooooooooooooooooooooooooooooooooooooooooooongloooooooooooooooooooooooooooooooooooooooooooongloooooooooooooooooooong@email.com'

        response = MyRequests.post(self.url_register, data=self.data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_answer_text(response, "Invalid email format")
