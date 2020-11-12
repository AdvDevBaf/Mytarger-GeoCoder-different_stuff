import requests
import pandas as pd
import time
from tkinter import *
from tkinter.filedialog import askopenfilename
import openpyxl
import json
#1545 1555

data = pd.read_excel("C:\\Users\AMasanov\\Desktop\\data_vk.xlsx", header=None, sep=';', usecols=[0,1,2], names=['hren','campaign','ads'], encoding="ISO-8859-1")
campaign = data['campaign'].values.tolist()
ads = data['ads'].values.tolist()
ads = ads[1:]
campaign = campaign[1:]
print(len(ads))
print(len(campaign))
print(campaign[0])
print(ads[0])
#https://oauth.vk.com/blank.html#access_token=6b1461e432b63a95183103e4f2a7ca7d4d19484758f2e93c0803c566870439b3eeac769dac0b8e95331f7&expires_in=86400&user_id=288422846&state=123456

token = '6b1461e432b63a95183103e4f2a7ca7d4d19484758f2e93c0803c566870439b3eeac769dac0b8e95331f7'
method = 'https://api.vk.com/method/ads.updateAds'


for ad in ads:
    if ad != '':
        time.sleep(5)
        data = [{'ad_id': ad, 'age_from':15, 'age_to':54}]
        params = {
        "account_id": 1900013999,
        "data": json.dumps(data),
        "access_token": token,
        "v": '5.73'
    }
        response = requests.post(method, params=params)
        print(response.json())
    else:
        print(str('ad is ') + str(ad))
