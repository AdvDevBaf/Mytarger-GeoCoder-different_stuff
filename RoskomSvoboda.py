import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from itertools import groupby
import urllib
from tkinter import filedialog
from os import path
import requests
import json


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


class RosKomFreedom:

    @staticmethod
    def save_to_csv(tables, tables_for_youtube):

        """
        Записывает получившийся список в csv
        """

        path_to_sites = path.realpath('sites_' + str(datetime.today().strftime("%Y-%m-%d-%H.%M")) + '.csv')
        path_to_youtube = path.realpath('youtube_' + str(datetime.today().strftime("%Y-%m-%d-%H.%M")) + '.csv')

        if path.exists(path_to_sites) is False:
            root = filedialog.Tk()
            dirs = filedialog.askdirectory()
            path_to_sites = dirs + '\\' + 'sites_' + str(datetime.today().strftime("%Y-%m-%d-%H.%M")) + '.csv'
            path_to_youtube = dirs + '\\' + 'youtube_' + str(datetime.today().strftime("%Y-%m-%d-%H.%M")) + '.csv'
            path_to_sites = path_to_sites.replace('/', '\\\\')
            path_to_youtube = path_to_youtube.replace('/', '\\\\')
            root.destroy()

        path_to_sites = path_to_sites.replace('\\', '\\\\')
        path_to_youtube = path_to_youtube.replace('\\', '\\\\')

        tables.to_csv(str(path_to_sites), header=False, index=False, encoding='cp1251')
        tables_for_youtube.to_csv(str(path_to_youtube), header=False, index=False, encoding='cp1251')
        print('Готово')
        return 0

    @staticmethod
    def get_ch_name(ch):
        if '\"' in ch:
            ch = ch.split('\"')[1]
        try:
            opener = AppURLopener()
            html_doc = opener.open('https://www.' + ch)
            soup = BeautifulSoup(html_doc)
            soup_list = soup.findAll('meta')
            channel_id = ''
            for content in soup_list:
                if 'channelId' in str(content):
                    channel_id = str(content)
                    channel_id = str(channel_id).split('\"')[1]
                    break
        except:
            channel_id = ''
        return channel_id

    @staticmethod
    def get_json():
        respect = requests.get('https://api.reserve-rbl.ru/api/v2/current/json')
        dict_train = json.dumps(respect.json()["2019-09-24"])
        train = pd.read_json(dict_train, orient='column').rename(
            columns={'ip': 'ip', 'date': 'date', 'gos_organ': 'gos_organ',
                     'postanovlenie': 'postanovlenie',
                     'link': 'Домены', 'page': 'page'})
        tables = train.drop(['ip', 'date', 'gos_organ', 'postanovlenie', 'page'], axis=1)
        print(train)
        print(tables)
        tables = tables.dropna(axis=0, how='any')  # Убирает все лишние пробелы
        return tables

    def processing_data(self):
        tables = self.get_json()
        tables['Домены'].replace(['http://'], [''], regex=True, inplace=True)
        tables['Домены'].replace(['https://'], [''], regex=True, inplace=True)

        print('Убрано')

        table = []  # Создает пустой список table
        table_for_youtube = []  # Создает список для youtube

        tables['Домены'].replace(['\*.'], [''], regex=True, inplace=True)  # удаляет все все *

        for site in tables['Домены']:  # Разбиваем список на два подсписка: для пиратских сайтов и для youtube
            if 'ec2-' not in site:
                if 'www.youtube.com' in site or 'youtu.be' in site or site[0:11] == 'youtube.com':
                    table_for_youtube.append(site)  # Добавляет элемент в список
                    table_for_youtube = [el for el, _ in groupby(table_for_youtube)]
                else:
                    site = site.split('/')[0]
                    table.append(site)
                    table = [el for el, _ in groupby(table)]

        print('Разделено')

        """
        Заносим списки в соответствующие dataframe
        """

        tables = pd.DataFrame(table, columns=['Домены'])
        tables_for_youtube = pd.DataFrame(table_for_youtube, columns=['Домены'])

        print('Занесли')

        """
        Удаляем все www.
        """

        tables['Домены'].replace(['www.'], [''], regex=True, inplace=True)
        tables_for_youtube['Домены'].replace(['www.'], [''], regex=True, inplace=True)

        print('Удалили')

        """
        Создаем новые списки для фильтрации повторяющихся элементов
        """

        new_table = []
        new_table_for_youtube = []

        print('Создали')

        """
        Удаляет из списков повторяющиеся значения
        """

        for equal_site in tables['Домены']:
            if equal_site not in new_table:
                if 'HASH(' not in equal_site:
                    new_table.append(equal_site)

        tables = pd.DataFrame(new_table, columns=['Домены'])

        for equal_youtube_site in tables_for_youtube['Домены']:
            if '\"' in str(equal_youtube_site):
                equal_youtube_site = equal_youtube_site.split('\"')[1]
            if equal_youtube_site not in new_table_for_youtube:
                new_table_for_youtube.append(equal_youtube_site)

        print('Удалили')
        print('Получаем')

        for ch in tables_for_youtube['Домены']:  # Получим дискредитированные каналы
            if 'watch' in str(ch):
                new_user = self.get_ch_name(str(ch))
                if str(new_user) not in new_table_for_youtube and str(new_user) != '':
                    new_table_for_youtube.append('youtube.com/channel/' + new_user)

        tables_for_youtube = pd.DataFrame(new_table_for_youtube, columns=['Домены'])  # Заносим изменения в таблицу
        return self.save_to_csv(tables, tables_for_youtube)


start = RosKomFreedom()
start.processing_data()
