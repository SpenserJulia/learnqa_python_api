import requests


class TestHeaderCheck:
    def test_header_check(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")

        # Выводим значение заголовка
        print(f"{response.headers}")

        # Получаем значения всех параметров заголовка
        date = response.headers.get("Date")
        content_type = response.headers.get("Content-Type")
        content_length = response.headers.get("Content-Length")
        connection = response.headers.get("Connection")
        keep_alive = response.headers.get("Keep-Alive")
        server = response.headers.get("Server")
        x_secret_homework_header = response.headers.get("x-secret-homework-header")
        cache_control = response.headers.get("Cache-Control")
        expires = response.headers.get("Expires")

        # Наличие полей в заголовке
        assert "Date" in response.headers, "Header have no field 'Date'"
        assert "Content-Type" in response.headers,"Header have no field 'Content-Type'"
        assert "Content-Length" in response.headers, "Header have no field 'Content-Length'"
        assert "Connection" in response.headers, "Header have no field 'Connection'"
        assert "Keep-Alive" in response.headers, "Header have no field 'Keep-Alive'"
        assert "Server" in response.headers, "Header have no field 'Server'"
        assert "x-secret-homework-header" in response.headers, "Header have no field 'x-secret-homework-header'"
        assert "Cache-Control" in response.headers, "Header have no field 'Cache-Control'"
        assert "Expires" in response.headers, "Header have no field 'Expires'"

        # Проверки значений
        assert date == expires, "Header 'Date' not equal to header 'Expires'"
        assert content_type == 'application/json', "Header 'Content-Type not 'application/json'"
        assert content_length == "15", "Header 'Content-Length' not equal '15'"
        assert connection == 'keep-alive', "Header 'Connection' not equal 'keep-alive'"
        assert server == "Apache", "Header 'Server' not equal 'Apache'"
        assert x_secret_homework_header == 'Some secret value', "Header 'x-secret-homework-header' is not equal 'Some secret value'"
        assert cache_control == 'max-age=0', "Header 'Cache-Control' is not equal 'max-age=0'"
