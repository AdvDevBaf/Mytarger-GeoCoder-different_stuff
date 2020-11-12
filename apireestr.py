import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import urllib
from itertools import groupby
from tkinter import filedialog
from os import path
import requests

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()

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
                print('youtube channels')
                channel_id=str(content)
                channel_id=str(channel_id).split('\"')[1]
                break
    except:
        channel_id=''
    return channel_id


response = requests.get('https://reestr.rublacklist.net/api/v2/current/json')
reason = []
table = []
print(len(response.json()['2018-07-23']))

for i in range(len(response.json()['2018-07-19'])):
    if response.json()['2018-07-19'][i]['page'] != '':
        print(response.json()['2018-07-19'][i]['gos_organ'])
        print(response.json()['2018-07-19'][i]['page'])
        reason.append(response.json()['2018-07-19'][i]['gos_organ'])
        table.append(response.json()['2018-07-19'][i]['page'])
    else:
        print('NIET')

reason = pd.DataFrame(reason,columns=['Причина'])
tables = pd.DataFrame(table,columns=['Домены'])

print(tables)
print(list(tables['Домены']))
print(list(reason['Причина']))


tables['Домены'].replace(['http://'],[''],regex = True,inplace=True)
tables['Домены'].replace(['https://'],[''],regex = True,inplace=True)
print('http has been removed')

table=[] #Создает пустой список table
table_for_youtube=[] #Создает список для youtube

tables['Домены'].replace(['\*.'],[''],regex = True,inplace=True) #удаляет все все *

print('* has been removed')

for site in tables['Домены']: #Разбиваем список на два подсписка: для пиратских сайтов и для youtube
    if('ec2-' not in site):
        print(site)
        if ('www.youtube.com' in site or 'youtu.be' in site or site[0:11]=='youtube.com'):
            table_for_youtube.append(site)  # Добавляет элемент в список
            table_for_youtube = [el for el, _ in groupby(table_for_youtube)]
        else:
            print(site)
            site = site.split('/')[0]
            table.append(site)
            table = [el for el, _ in groupby(table)]


for j in range(len(table)):
    print('j is ' + str(j))
    reason.append(list(reason['Причина'])[j])

"""
Заносим списки в соответствующие dataframe
"""
print('das')
reason = pd.DataFrame(reason,columns=['Причина'])
table = pd.DataFrame(table,columns=['Домены'])
#tables = tables.Домены.replace(to_replace=list(tables['Домены']), value=table, inplace=True)
tables = pd.concat([table,reason],axis=1,ignore_index=True)
tables_for_youtube = pd.DataFrame(table_for_youtube,columns=['Домены'])
tables = tables.dropna(axis=0,how='any') #Убирает все лишние пробелы
tables.columns = ['Домены', 'Причина']
print(tables)


"""
Удаляем все www.
"""
tables['Домены'].replace(['www.'], [''], regex=True, inplace=True)
tables_for_youtube['Домены'].replace(['www.'],[''],regex = True,inplace=True)

"""
Создаем новые списки для фильтрации повторяющихся элементов
"""
new_table = []
new_table_for_youtube = []

"""
Удаляет из списков повторяющиеся значения
"""
for equal_site in tables['Домены']:
    if (equal_site not in new_table):
        if 'HASH(' not in equal_site:
            print(equal_site)
            new_table.append(equal_site)

new_reason = []
for k in range(len(new_table)):
    print('k is ' + str(k))
    new_reason.append(list(tables['Причина'])[k])

new_table = pd.DataFrame(new_table,columns=['Домены'])

new_reason = pd.DataFrame(new_reason,columns=['Причина'])
print(new_table)
print(new_reason)
tables = pd.concat([new_table, new_reason],axis=1,ignore_index=True)
tables = tables.dropna(axis=0,how='any') #Убирает все лишние пробелы
tables.columns = ['Домены', 'Причина']
print(tables)


for equal_youtube_site in tables_for_youtube['Домены']:
    if('\"' in str(equal_youtube_site)):
        equal_youtube_site=equal_youtube_site.split('\"')[1]
    if (equal_youtube_site not in new_table_for_youtube):
        new_table_for_youtube.append(equal_youtube_site)


for ch in tables_for_youtube['Домены']:  # Получим дискредитированные каналы
    if('watch' in str(ch)):
        new_user= get_channel_name(str(ch))
        if(str(new_user) not in new_table_for_youtube and str(new_user)!=''):
            new_table_for_youtube.append('youtube.com/channel/'+ new_user)


tables_for_youtube = pd.DataFrame(new_table_for_youtube,columns=['Домены'])  # Заносим изменения в таблицу

"""
Записывает получившийся список в csv
"""

path_to_sites = path.realpath('sites_'+str(datetime.today().strftime("%Y-%m-%d-%H.%M"))+'.csv')
path_to_youtube = path.realpath('youtube_'+str(datetime.today().strftime("%Y-%m-%d-%H.%M"))+'.csv')

if (path.exists(path_to_sites)==False):
    root= filedialog.Tk()
    dirs = filedialog.askdirectory()
    path_to_sites=dirs+'\\'+'sites_'+str(datetime.today().strftime("%Y-%m-%d-%H.%M"))+'.csv'
    path_to_youtube=dirs+'\\'+'youtube_'+str(datetime.today().strftime("%Y-%m-%d-%H.%M"))+'.csv'
    path_to_sites = path_to_sites.replace('/','\\\\')
    path_to_youtube = path_to_youtube.replace('/','\\\\')
    root.destroy()


path_to_sites = path_to_sites.replace('\\','\\\\')
path_to_youtube = path_to_youtube.replace('\\','\\\\')

tables.to_csv(str(path_to_sites),header=False,index = False,encoding='cp1251', sep=';')
tables_for_youtube.to_csv(str(path_to_youtube),header=False,index = False,encoding='cp1251')
print('Готово')
