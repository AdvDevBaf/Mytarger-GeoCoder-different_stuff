import pandas as pd
import requests

response = requests.get("https://data.42matters.com/api/v2.0/android/apps/search.json?q=Harry Potter&country=RU"
                        "&limit=10&access_token=60a41c83c1ff851132b362a80aa5fbf67885c490")
print(response.json())

page = response.json()['num_pages']

print(response.json())
print(page)
ids = []
name = []
link = []
for i in range(1, page+1):
    print(i)
    response = requests.get("https://data.42matters.com/api/v2.0/android/apps/search.json?q=Harry Potter&country=RU"
                            "&limit=10&access_token=60a41c83c1ff851132b362a80aa5fbf67885c490&page="+str(i))
    print(response.json())
    print(response.json()['results'])
    for j in range(0, len(response.json()['results'])):
        print(response.json()['results'][j]['package_name'])
        print(response.json()['results'][j]['title'])
        print(response.json()['results'][j]['market_url'])
        ids.append(response.json()['results'][j]['package_name'])
        name.append(response.json()['results'][j]['title'])
        link.append(response.json()['results'][j]['market_url'])


table = pd.DataFrame({'id': ids, 'Название': name, 'Ссылка': link})
table.to_csv(str("C:\\Users\AMasanov\\Desktop\\") + '/' + str("Harry Potter") + '.csv', sep=';',
             index=False, encoding='utf-8-sig')
print('ok')