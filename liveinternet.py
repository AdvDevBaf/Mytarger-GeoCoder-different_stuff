import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import urllib
from itertools import groupby
from tkinter import filedialog
from os import path
import time
import requests

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
html_doc = opener.open('https://www.liveinternet.ru/rating/ru/media/today.tsv?page='+str(1))



#tetst = request('https://reestr.rublacklist.net/')
#html_doc = urlopen(tetst).read() #Получаем главную страницу сайта
print(html_doc)
soup = BeautifulSoup(html_doc, "lxml")
#k = soup.find('div', 'pagination').find('b').text
#count = int(k[2:]) #Получаем количество страниц, которое нам необходимо вытащить
#print(count)
count = 200


def collectdata(i):  #Получает страницы, отбрасывает все столбцы кроме столбца доменов
    #time.sleep(5)
    while True:
        print('da')
        print(i)
        url = 'https://www.liveinternet.ru/rating/ru/media/today.tsv?page='+str(i)
        header = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
        }
        r = requests.get(url, headers=header)
        print(r.text)
        data = r.text.split('\n')
        new_data = []
        print(data)
        for j in range(len(data)):
            if data[j] is not '':
                print(data[j].split('\t')[1])
                new_data.append(data[j].split('\t')[1])
        new_data = new_data[1:]
        print(new_data)
        tables = pd.DataFrame(data=new_data,columns=['Домены'])
        print(tables)
        tab = tables
        print('Страница '+str(i)+' готова')
        break
    return tab


def get_channel_name(ch): #Получает channelId
    if('\"') in ch:
        ch=ch.split('\"')[1]
    try:
        opener = AppURLopener()
        html_doc = opener.open('https://www.'+ ch)
        #html_doc = urllib.request.urlopen('https://www.'+ ch) #Получаем страницу сайта
        soup = BeautifulSoup(html_doc)
        soup_list = soup.findAll('meta')
        content_list=[]
        channel_id=''
        for content in soup_list:
            if('channelId' in str(content)):
                channel_id=str(content)
                channel_id=str(channel_id).split('\"')[1]
                break
    except:
        channel_id=''
    return channel_id


conca =[collectdata(i) for i in range(1,count+1)]  # Заход в функцию
tables=pd.concat(conca)
tables = tables.dropna(axis=0,how='any')  # Убирает все лишние пробелы

"""
Убирает все http и https
"""

tables['Домены'].replace(['http://'],[''],regex = True,inplace=True)
tables['Домены'].replace(['https://'],[''],regex = True,inplace=True)

table=[] #Создает пустой список table
table_for_youtube=[] #Создает список для youtube

tables['Домены'].replace(['\*.'],[''],regex = True,inplace=True) #удаляет все все *

for site in tables['Домены']:
    #Разбиваем список на два подсписка: для пиратских сайтов и для youtube
    site = site.split('/')[0]
    table.append(site)
    table = [el for el, _ in groupby(table)]

"""
Заносим список в соответствующий dataframe
"""
tables = pd.DataFrame(table,columns=['Домены'])

"""
Удаляем все www.
"""
tables['Домены'].replace(['www.'],[''],regex = True,inplace=True)

"""
Создаем новый список для фильтрации повторяющихся элементов
"""
new_table=[]

"""
Удаляет из списка повторяющиеся значения
"""
for equal_site in tables['Домены']:
    if (equal_site not in new_table):
        new_table.append(equal_site)

tables = pd.DataFrame(new_table,columns=['Домены'])

"""
Записывает получившийся список в csv
"""

path_to_sites = path.realpath('sites_'+str(datetime.today().strftime("%Y-%m-%d-%H.%M"))+'.csv')

if (path.exists(path_to_sites)==False):
    root= filedialog.Tk()
    dirs = filedialog.askdirectory()
    path_to_sites=dirs+'\\'+'liveinternet_'+str(datetime.today().strftime("%Y-%m-%d-%H.%M"))+'.csv'
    path_to_sites = path_to_sites.replace('/','\\\\')
    root.destroy()

path_to_sites = path_to_sites.replace('\\','\\\\')

tables.to_csv(str(path_to_sites),header=False,index = False,encoding='cp1251')
print('Готово')
