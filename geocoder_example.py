import requests

response = requests.get("https://geocode-maps.yandex.ru/1.x/"
                        "?apikey=55080292-108d-4b98-b077-fb1c2af3affd&format=json&geocode=" + str("Москва, тверская")).json()
print(response)