import requests

class TestCookieCheck:
    def test_cookie_check(self):
        url_homework_cookie = "https://playground.learnqa.ru/api/homework_cookie"

        response = requests.get(url_homework_cookie)
        print(f"{dict(response.cookies)}")

        assert "HomeWork" in response.cookies, "There is no cookie 'HomeWork' in answer"

        cookie_homework = response.cookies.get("HomeWork")

        assert cookie_homework == "hw_value", "Value cookie 'HomeWork' not equal 'hw_value'"


