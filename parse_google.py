import pandas as pd
import requests

data = pd.read_csv("C:\\Users\AMasanov\\Desktop\\oneboy.csv", header=None,sep=';', names=['name', 'link'], encoding="ISO-8859-1")
link = data['link'].values.tolist()
link = link[1:]
print(len(link))

new_link = []
names = []

for i in range(1,len(link)):
    if "/store/apps/details?id" in str(link[i]):
        if str("https://play.google.com"+str(link[i])) not in new_link:
            print("https://play.google.com"+str(link[i]))
            new_link.append("https://play.google.com"+str(link[i]))

print(len(new_link))
links = []

for i in range(0, len(new_link)):
    links.append(new_link[i])

ids = [x.replace('https://play.google.com/store/apps/details?id=', '') for x in links]

for i in range(0, len(ids)):
    print(i)
    print(ids[i])
    response = requests.get("https://data.42matters.com/api/v3.0/android/apps/topics.json?p="+str(ids[i])+"&access_token=3b985ca59ecfdb01d6aa3c5a5ece22430937adc4")
    print(response.json())
    print(response.json()['title'])
    names.append(str(response.json()['title']))
    print(names)

adv = []

print(len(names))

for i in range(0, len(ids)):
    page = requests.get('https://play.google.com/store/apps/details?id='+str(ids[i]))
    if 'Contains Ads' in page.text:
        print('yes')
        adv.append('yes')
    else:
        print('no')
        adv.append('no')

print(adv)

table = pd.DataFrame({'id': ids, 'Название': names, 'Ссылка': links, 'Реклама в приложении':adv})
table.to_csv(str("C:\\Users\AMasanov\\Desktop\\") + '/' + str("games for 14 years old boys") + '.csv', sep=';', index=False,
             encoding='utf-8-sig')
print('ok')
