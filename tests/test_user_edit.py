import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):

    def setup(self):
        # REGISTER
        url_register = "https://playground.learnqa.ru/api/user/"
        url_auth = "https://playground.learnqa.ru/api/user/login"
        register_data = self.prepare_registration_data()
        response_reg = requests.post(url_register, data=register_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_key(response_reg, "id")

        self.email = register_data['email']
        self.first_name = register_data['firstName']
        self.password = register_data['password']
        self.user_id = self.get_json_value(response_reg, "id")

        # LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }
        response_log = requests.post(url_auth, data=login_data)

        self.auth_sid = self.get_cookie(response_log, "auth_sid")
        self.token = self.get_header(response_log, "x-csrf-token")

    def test_edit_just_created_user(self):
        # EDIT
        new_name = "Change Name"
        response_update = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response_update, 200)

        # GET
        response_get = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(response_get, "firstName", new_name, "Wrong name of user after edit")

    def test_edit_firstname_on_short(self):
        # EDIT
        new_name = "A"
        response_update = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response_update, 400)
        Assertions.assert_answer_text_json(response_update, "error", "Too short value for field firstName")

        # GET
        response_get = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "firstName",
            self.first_name,
            f"First name in user's details change on 1 simbol '{new_name}'"
        )

    def test_edit_email_on_incorrect(self):
        # EDIT
        new_email = self.email.replace("@", "")

        response_update = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response_update, 400)
        Assertions.assert_answer_text(response_update, "Invalid email format")

        # GET
        response_get = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "email",
            self.email,
            f"Email change on '{new_email}' without @ "
        )

    def test_edit_without_auth(self):
        # EDIT
        new_name = "Change Name"
        response_update = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response_update, 400)
        Assertions.assert_answer_text(response_update, "Auth token not supplied")

        # GET
        response_get = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_not_name(response_get, "firstName", new_name, f"Firstname change without autorization on {new_name}")

    def test_edit_with_auth_another_user(self):
        # EDIT
        new_name = "Change Name"
        another_user = int(self.user_id) - 1

        response_update = requests.put(
            f"https://playground.learnqa.ru/api/user/{another_user}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )

        # На данный момент нет обработки ошибки, всегда 200
        Assertions.assert_code_status(response_update, 200)

        # GET
        response_get = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        name_final = response_get.json()["firstName"]
        print(name_final)

        #На данный момент проверка не проходит, так как даже обращаыясь к другому id операция PUT срабатывает
        Assertions.assert_json_value_by_name(response_get, "firstName", self.first_name, f"Wrong change firstname without auth for this login. Now firstname: '{name_final}'")







