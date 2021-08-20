import requests

method = ["GET", "POST", "DELETE", "PUT"]

print("Сценарий 1: без метода")
response1 = requests.get("https://playground.learnqa.ru/api/compare_query_type")
print(response1.text)
# Ответ Wrong method provided

print("Сценарий 2: Head - не из списка")
response2 = requests.head("https://playground.learnqa.ru/api/compare_query_type", params={"method": method[0]})
print(response2.text)
# Ответ пустой

print("Сценарий 3: корректный запрос относительно метода")
response3 = requests.get("https://playground.learnqa.ru/api/compare_query_type", params={"method": method[0]})
print(response3.text)
# Ответ {"success":"!"}

print("Сценарий 4: перебор")
for x in method:
    for y in method:
        payload = {"method": x}
        if y == "GET":
            response4 = getattr(requests, y.lower())("https://playground.learnqa.ru/api/compare_query_type", params=payload)
            print(f"Get {y} with params {x} and answer: {response4.text}")
        else:
            response4 = getattr(requests, y.lower())("https://playground.learnqa.ru/api/compare_query_type", data=payload)
            print(f"Get {y} with params {x} and answer: {response4.text}")

# Delete send with params GET and answer: {"success":"!"}
