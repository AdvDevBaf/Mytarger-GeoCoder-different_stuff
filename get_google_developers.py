import requests
from bs4 import BeautifulSoup
import time
# https://play.google.com/store/apps/dev?id=  или /store/apps/dev?id=  ищем эту ссылку
# перейдя по ней ищем по https://play.google.com/store/apps/collection/cluster?clp=ig   /store/apps/collection/cluster?clp=

devs = []

for link in links:
    time.sleep(3)
    try:
        sas = requests.get(link, headers={'Accept-Language': 'ru-RU,ru;q=0.8'}).text
        soup = BeautifulSoup(sas)
        soup_list = soup.findAll('a',href=True)
        print(soup_list)
        for a in soup.find_all('a', href=True):
            if '/store/apps/dev?' in a['href']:
                print("Found the URL:", a['href'])
                if 'https://play.google.com'+ str(a['href']) not in devs:
                    print('dev link found')
                    devs.append('https://play.google.com' + a['href'])
    except:
        print('error')
print(devs)

dev_links = []

for dev in devs:
    time.sleep(3)
    try:
        sas = requests.get(dev, headers={'Accept-Language': 'ru-RU,ru;q=0.8'}).text
        soup = BeautifulSoup(sas)
        soup_list = soup.findAll('a',href=True)
        print(soup_list)
        for a in soup.find_all('a', href=True):
            if '/store/apps/collection/cluster?' in a['href']:
                print("Found the URL:", a['href'])
                if 'https://play.google.com'+ str(a['href']) not in dev_links:
                    print('dev link cluster found')
                    dev_links.append('https://play.google.com' + a['href'])
    except:
        print('error')
print(dev_links)


new_id__dev_links = []

for dev_link in dev_links:
    time.sleep(3)
    try:
        sas = requests.get(dev_link, headers={'Accept-Language': 'ru-RU,ru;q=0.8'}).text
        soup = BeautifulSoup(sas)
        soup_list = soup.findAll('a', href=True)
        print(soup_list)
        for a in soup.find_all('a', href=True):
            if '/store/apps/details?id=' in a['href']:
                print("Found the IDS:", a['href'])
                if '/store/apps/details?id=' + str(a['href']) not in dev_link:
                    print('new dev link')
                    new_id__dev_links.append('https://play.google.com' + a['href'])
    except:
        print('error')

print(new_id__dev_links)

for new_ids in new_id__dev_links:
    if new_ids not in links:
        links.append(str(new_ids))
    if str(new_ids).replace('https://play.google.com/store/apps/details?id=', '') not in ids:
        ids.append(str(new_ids).replace('https://play.google.com/store/apps/details?id=', ''))
