from json.decoder import JSONDecodeError
import requests
import json
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

try:
    answer = json.loads(response.text)
except JSONDecodeError:
    print("Response is not a Json format")

if "token" in answer and "seconds" in answer:
    token = answer["token"]
    second = answer["seconds"]
else:
    print("Ключей 'token' или 'seconds' в JSON не оказалось")


print(f"token: {token} seconds: {second}")

# Обращаемся пока задача ещё не готова
payload = {"token": token}
response_with_token = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)
try:
    answer = json.loads(response_with_token.text)
except JSONDecodeError:
    print("Response is not a Json format")

if "status" in answer:
    status = answer["status"]
else:
    print("Ключа 'status' в JSON не оказалось")

print(f"Текущий статус: {status}")

# Засыпаем на время выполнения задачи
time.sleep(second)

# Запрос по готовности задачи
response_with_token = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)

try:
    answer = json.loads(response_with_token.text)
except JSONDecodeError:
    print("Response is not a Json format")

if "result" in answer:
    result = answer["result"]
else:
    print("Ключа 'result' в JSON не оказалось")

print(f"Результат: {result}")

