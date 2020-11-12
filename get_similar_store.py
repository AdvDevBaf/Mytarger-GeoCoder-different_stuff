import pandas as pd
import requests
import time
import urllib
from bs4 import BeautifulSoup


link = 'https://play.google.com/store/apps/details?id=com.rockstargames.gtavc'
print(link)
sas = requests.get(link, headers={'Accept-Language': 'ru-RU,ru;q=0.8'}).text
soup = BeautifulSoup(sas)
soup_list = soup.findAll('a',href=True)
print(soup_list)
similar_link = []
for a in soup.find_all('a', href=True):
    if 'store/apps/collection/cluster?' in a['href']:
        print("Found the URL:", a['href'])
        if 'https://play.google.com'+ str(a['href']) not in similar_link:
            print('da')
            similar_link.append('https://play.google.com' + a['href'])
print(similar_link)

new_id_links = []

for similar in similar_link:
    soup = BeautifulSoup(sas)
    soup_list = soup.findAll('a', href=True)
    print(soup_list)
    for a in soup.find_all('a', href=True):
        if '/store/apps/details?id=' in a['href']:
            print("Found the URL:", a['href'])
            if '/store/apps/details?id=' + str(a['href']) not in similar_link:
                print('da')
                new_id_links.append('https://play.google.com' + a['href'])

print(new_id_links)

ids = []
links = []
for new_ids in ids:
    ids.append(str(new_ids).replace('https://play.google.com/store/apps/details?id=',''))
    links.append(str(new_ids))