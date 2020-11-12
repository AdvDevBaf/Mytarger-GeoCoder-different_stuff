import pandas as pd
import requests
import time
import urllib
from bs4 import BeautifulSoup


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

data = pd.read_excel("C:\\Users\AMasanov\\Desktop\\app_20191219_112501_659194930_2751059812.xlsx", header=None, sep=';', names=['app', 'pot','uq'], encoding="ISO-8859-1")
links = data['app'].values.tolist()
links = links[1:]
sort_links = []
for lin in links:
    if "Android" in str(lin):
        print(lin)
        word = lin.replace("(", "").replace(")", "")
        temp = word.index(str('Android'))
        wordEndIndex = temp + word[temp:].index(' ') - 1
        sort_links.append(str('/store/apps/details?id=') +str(word[wordEndIndex + 1:].replace(" ","")))
    else:
        print(str('No Android in ') + str(lin))

print(len(sort_links))

table = pd.DataFrame({'Ссылка': sort_links},
                     columns=["Ссылка"])

table.to_csv(str("C:\\Users\AMasanov\\Desktop\\") + '/' + str("Ссылки_андроид") + '.csv', sep=';', index=False,
             encoding='utf-8-sig')
