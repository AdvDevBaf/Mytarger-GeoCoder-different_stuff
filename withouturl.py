import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import urllib
from itertools import groupby
from tkinter import filedialog
from os import path
import time
import json
import requests
'''
token = '84d26773170602a56a3572e77705e5e321d4e9b5e89e04c04e5b5ea2b2001e0f802b512f3a262f0d62a38'
method = 'https://api.vk.com/method/groups.search'
params = {
                "q": 'Кулинария',
                "access_token": token,
                'offset': 0,
                'count': 1000,
                "v": '5.73'
            }
response = requests.post(method, params=params)
search = []
print(response.json())
print(((response.json()['response']['count'])//1000)+1)
for i in range(((response.json()['response']['count'])//1000)+1):
    params = {
        "q": 'Кулинария',
        "access_token": token,
        'offset': i*100,
        'count': 1000,
        "v": '5.73'
    }
    response = requests.post(method, params=params)
    for j in range(len(response.json()['response']['items'])):
        search.append('https://vk.com/' + str(response.json()['response']['items'][j]['screen_name']))
        print(response.json()['response']['items'][j]['screen_name'])

tables = pd.DataFrame(data=search,columns=['Домены'])

path_to_sites = path.realpath('vk_search_'+str(datetime.today().strftime("%Y-%m-%d-%H.%M"))+'.csv')

if (path.exists(path_to_sites)==False):
    root= filedialog.Tk()
    dirs = filedialog.askdirectory()
    path_to_sites=dirs+'\\'+'vk_search_'+str(datetime.today().strftime("%Y-%m-%d-%H.%M"))+'.csv'
    path_to_sites = path_to_sites.replace('/','\\\\')
    root.destroy()

path_to_sites = path_to_sites.replace('\\','\\\\')

tables.to_csv(str(path_to_sites),header=False,index = False,encoding='cp1251')
print('Готово')
'''
'''
header = {'Host':'target.my.com','Content-Type':'application/json','Accept-Encoding':'gzip,deflate,compress',
          'Authorization':'Bearer XowoCgn8Vkp58R4AUeeJfDPbNAncYUoKhM5Rs0niaMngNjaDSn4VbEpjMgBWWKkWaPC1hjJKR4BFVeC6ENHptHKzAqR1iQtIgD5V1VHUonT70TL9mdPqzClPJRSRKpq5hjrx8qTwCBxhRMHeQhMrNPashNgifnDPjvVWHFyzxkGEpMaKwjYpBPFUD8NcateOYGCJgeHvk8U5cGoDTM8PgVOePgeJOdsobfcvT'}



r = requests.get('https://target.my.com/api/v1/campaigns.json', headers = header)

print(len(r.json()))


for i in range(len(r.json())):
    print(str(r.json()[i]['id']) + ' - '+ str(r.json()[i]['name']))
    print('id - ' + str(r.json()[i]['name']))
    print(r.json()[i]['id'])
    data = {'price': 50}
    edit_coms = requests.post('https://target.my.com/api/v1/campaigns/' + str(r.json()[i]['id']) + '.json',
                              data=json.dumps(data), headers=header)
    print(r.json()[i]['price'])
    print(edit_coms.json())
'''
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
#html_doc = opener.open('https://reestr.rublacklist.net/pages/1/include/0')



#tetst = request('https://reestr.rublacklist.net/')
#html_doc = urlopen(tetst).read() #Получаем главную страницу сайта
#print(html_doc)
count = int(1081) # Получаем количество страниц, которое нам необходимо вытащить
print(count)

def collectdata(i):  #Получает страницы, отбрасывает все столбцы кроме столбца доменов
    while True:
        try:
            print('da')
            url = 'https://reestr.rublacklist.net/pages/'+str(i)+'/include/0'
            header = {
                "User-Agent": "Chrome/50.0.2661.75",
                "X-Requested-With": "XMLHttpRequest"
            }
            r = requests.get(url)
            tables = pd.read_html(r.text, header=0)[0].iloc[:,1:].rename(columns={'Unnamed: 1':'1','Unnamed: 2':'Домены',
                                                                            'Unnamed: 3':'3','Unnamed: 0':'0','Unnamed: 4':'Причина'})
            #print(tables)
            tab = tables.drop(['1','3','Количество доменов, блокируемых заодно'], axis=1)
            print('Страница '+str(i)+' готова')
            break
        except:
            time.sleep(1)
            print('daska')
            continue
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
                print('youtube channels')
                channel_id=str(content)
                channel_id=str(channel_id).split('\"')[1]
                break
    except:
        channel_id=''
    return channel_id

conca =[collectdata(i) for i in range(1,count+1)] #Заход в функцию
tables=pd.concat(conca)
tables = tables.dropna(axis=0,how='any') #Убирает все лишние пробелы

url_response = []
print(tables)
print(list(tables['Домены']))
print(list(tables['Причина']))


tables['Домены'].replace(['http://'],[''],regex = True,inplace=True)
tables['Домены'].replace(['https://'],[''],regex = True,inplace=True)
print('http has been removed')

table=[] #Создает пустой список table
reason = []
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
            site = site.split('/')[0]
            table.append(site)
            table = [el for el, _ in groupby(table)]


for j in range(len(table)):
    print('j is ' + str(j))
    reason.append(list(tables['Причина'])[j])

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
            new_table.append(equal_site)

new_reason = []
for k in range(len(new_table)):
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
        new_user=get_channel_name(str(ch))
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
