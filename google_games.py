import pandas as pd
import requests
token ='0661dc6ebef8d109a26f72253c3cd3b64491cc9d'

response = requests.get("https://data.42matters.com/api/v2.0/android/apps/top_google_charts.json?list_name=topselling_free&cat_key=FAMILY_9_AND_UP&country=RU&limit=10&access_token=0661dc6ebef8d109a26f72253c3cd3b64491cc9d")
print(response.json())

page = response.json()['num_pages']

print(response.json())
print(page)
ids = []
name = []
link = []
for i in range(1,page-1):
    print(i)
    response = requests.get("https://data.42matters.com/api/v2.0/android/apps/top_google_charts.json?list_name=topselling_free&cat_key=FAMILY_9_AND_UP&country=RU&limit=10&access_token=0661dc6ebef8d109a26f72253c3cd3b64491cc9d&page="+str(i))
    print(response.json())
    for j in range(0, len(response.json()['app_list'])):
        print(response.json()['app_list'][j]['package_name'])
        print(response.json()['app_list'][j]['title'])
        print(response.json()['app_list'][j]['market_url'])
        ids.append(response.json()['app_list'][j]['package_name'])
        name.append(response.json()['app_list'][j]['title'])
        link.append(response.json()['app_list'][j]['market_url'])


table = pd.DataFrame({'id': ids, 'Название': name,'Ссылка': link})
table.to_csv(str("C:\\Users\AMasanov\\Desktop\\") + '/' + str("Age_9_and_up") + '.csv', sep=';', index=False, encoding='utf-8-sig')
print('ok')