import pandas as pd
import requests

data = []

ids = []
name = []
link = []
for pr in range(len(data)):
    response = requests.get("https://data.42matters.com/api/v2.0/android/apps/search.json?q="+str(data[pr])+"&country=RU&limit=10&access_token=a2b63504c4186ac1c9d57cd2ad1d4ebbbaa0c763")
    print(response.json())

    page = response.json()['num_pages']

    print(response.json())
    print(page)
    for i in range(1, page + 1):
        print(ids)
        print(name)
        print(i)
        response = requests.get("https://data.42matters.com/api/v2.0/android/apps/search.json?q="+str(data[pr])+"&country=RU&limit=10&access_token=a2b63504c4186ac1c9d57cd2ad1d4ebbbaa0c763&page="+str(i))
        print(response.json())
        print(response.json()['results'])
        for j in range(0, len(response.json()['results'])):
            print(ids)
            print(name)
            print(response.json()['results'][j]['package_name'])
            print(response.json()['results'][j]['title'])
            ids.append(response.json()['results'][j]['package_name'])
            name.append(response.json()['results'][j]['title'])
            print(ids)
            print(name)


table = pd.DataFrame({'id': ids, 'Название': name})
table.to_csv(str("C:\\Users\AMasanov\\Desktop\\") + '/' + str("Имена") + '.csv', sep=';', index=False, encoding='utf-8-sig')
print('ok')