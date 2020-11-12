import pandas as pd
import requests
import time
import urllib
from bs4 import BeautifulSoup


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


data = pd.read_excel("C:\\Users\AMasanov\\Desktop\\doki.xlsx", header=None, sep=';', names=['name', 'link'], encoding="ISO-8859-1")
link = data['link'].values.tolist()
link = link[1:]
print(len(link))

'''
Надо считать правый столбец, но вносить в список ток те ссылки, которых там еще нет, причем нужно вносить ток идшники
'''

print(link)
time.sleep(10)
new_link = []
names = []

for i in range(1,len(link)):
    print(i)
    if "/store/apps/details?id" in str(link[i]):
        print(str(link[i]))
        if str("https://play.google.com"+str(link[i])) not in new_link:
            print("https://play.google.com"+str(link[i]))
            new_link.append("https://play.google.com"+str(link[i]))
        else:
            print("https://play.google.com "+ str(link[i]) + " in new_link")
    else:
        print('no')
        print("/store/apps/details?id " + str(link[i]) + " not link")

print(len(new_link))
links = []
time.sleep(10)

for i in range(0, len(new_link)):
    links.append(new_link[i])

ids = [x.replace('https://play.google.com/store/apps/details?id=', '') for x in links]
print(ids)




for link in links:
    print(link)
    time.sleep(3)
    sas = requests.get(link, headers={'Accept-Language': 'ru-RU,ru;q=0.8'}).text
    soup = BeautifulSoup(sas)
    soup_list = soup.findAll('title')
    print(soup_list[0])
    print('da')
    names.append(str(soup_list[0]).replace('<title id="main-title">', '').replace('</title>', '').replace('Приложения в Google Play – ',''))

adv = []

print(len(names))

for i in range(0, len(ids)):
    time.sleep(5)
    try:
        page = requests.get('https://play.google.com/store/apps/details?id='+str(ids[i]))
        if 'Contains Ads' in page.text:
            print('yes')
            adv.append('yes')
        else:
            print('no')
            adv.append('no')
    except:
        print('Something happen')
        adv.append('no')
        time.sleep(20)

print(adv)

description = []

for i in range(0, len(ids)):
    time.sleep(5)
    try:
        page = requests.get('https://play.google.com/store/apps/details?id='+str(ids[i]), headers={'Accept-Language': 'ru-RU,ru;q=0.8'})
        soup = BeautifulSoup(page.text)
        soup_list = soup.find('meta', {'itemprop': "description"})
        print(str(soup_list).replace('<meta content="', '').replace('" itemprop="description"/>', ''))
        description.append(str(soup_list).replace('<meta content="', '').replace('" itemprop="description"/>', ''))
    except:
        print('Something happen')
        description.append('no')
        time.sleep(20)

table = pd.DataFrame({'id': ids, 'Название': names, 'Описание': description, 'Реклама в приложении':adv, 'Ссылка': links},
                     columns=["id", "Название", "Описание", "Реклама в приложении", "Ссылка"])

table.to_csv(str("C:\\Users\AMasanov\\Desktop\\") + '/' + str("Для всей семьи 1") + '.csv', sep=';', index=False,
             encoding='utf-8-sig')
print('ok')
