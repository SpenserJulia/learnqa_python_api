from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User delete cases")
class TestUserDelete(BaseCase):

    @allure.description("Delete user with id=2 who is forbidden to delete")
    def test_delete_user_with_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        url_auth = "/user/login"
        response = MyRequests.post(url_auth, data=data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        user_id = 2
        payload = {"user_id": 2}
        url_delete = f"/user/{user_id}"

        response = MyRequests.delete(
            url_delete,
            data=payload,
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_answer_text(response, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')

    @allure.description("This test successfully delete new created user")
    def test_delete_user(self):
        # REGISTER
        url_register = "/user/"
        url_auth = "/user/login"

        register_data = self.prepare_registration_data()
        response_reg = MyRequests.post(url_register, data=register_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_key(response_reg, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_reg, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_log = MyRequests.post(url_auth, data=login_data)
        auth_sid = self.get_cookie(response_log, "auth_sid")
        token = self.get_header(response_log, "x-csrf-token")

        # DELETE
        url_delete = f"/user/{user_id}"

        response_delete = MyRequests.delete(
            url_delete,
            data={"user_id": user_id},
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_delete, 200)

        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_get, 404)
        Assertions.assert_answer_text(response_get, 'User not found')

    @allure.description("Delete user without autorization user")
    def test_delete_user_without_auth(self):
        # REGISTER
        url_register = "/user/"
        url_auth = "/user/login"

        register_data = self.prepare_registration_data()
        response_reg = MyRequests.post(url_register, data=register_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_key(response_reg, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_reg, "id")

        new_user = int(user_id) - 1

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_log = MyRequests.post(url_auth, data=login_data)
        auth_sid = self.get_cookie(response_log, "auth_sid")
        token = self.get_header(response_log, "x-csrf-token")

        # DELETE
        url_delete = f"/user/{new_user}"

        response_delete = MyRequests.delete(
            url_delete,
            data={"user_id": user_id},
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Должно быть сообщение об ошибке, что удаление возможно только для текущего юзера
        Assertions.assert_code_status(response_delete, 200)

        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Должно быть сообщение об успехе, юзера не удалили и он на месте и возвращает 200 код
        Assertions.assert_code_status(response_get, 404)
        Assertions.assert_answer_text(response_get, 'User not found')



