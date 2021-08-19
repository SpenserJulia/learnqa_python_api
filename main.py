import requests


response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

history = response.history

for x in history:
    print(x.url)






