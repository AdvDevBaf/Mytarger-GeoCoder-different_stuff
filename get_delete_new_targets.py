import pandas as pd
import requests
import json
import time
'''
r = requests.post('https://api.vk.com/method/ads.getTargetGroups',params={'account_id': 1900013999,
                                                                          'access_token': '770ccb3bf8095651170d3580c9d78b32ba04c865374815c7b7864c94bcee7fab338169b89358f7d3710d7',
                                                                          'client_id': 1605014088, 'v': '5.73'})
response = r.json()
print(response)
ids = []
name = []
# https://oauth.vk.com/blank.html#access_token=770ccb3bf8095651170d3580c9d78b32ba04c865374815c7b7864c94bcee7fab338169b89358f7d3710d7&expires_in=86400&user_id=288422846&state=123456
for i in range(len(response["response"])):
    print(response["response"][i]['id'])
    print(response["response"][i]['name'])
    ids.append(response["response"][i]['id'])
    name.append(response["response"][i]['name'])

table = pd.DataFrame({'id': ids, 'Название': name},
                     columns=["id", "Название"])

table.to_csv(str("C:\\Users\AMasanov\\Desktop\\") + '/' + str("Аудиторииs") + '.csv', sep=';', index=False,
             encoding='utf-8-sig')

'''
data = pd.read_excel("C:\\Users\AMasanov\\Desktop\\CBM.xlsx", header=None, sep=';', usecols=[1,2], names=['id','target'], encoding="utf-8-sig")
ids = data['target'].values.tolist()
target = [29420977,29420981,29589756,29919191,30285605,31002760,31102485,31508975]  
ids = ids[1:]
print(len(target))
print(len(ids))
print(ids)
print(target)

for i in range(len(ids)):
    time.sleep(2)
    print(ids[i])
    data = [{
                    "ad_id": ids[i], "retargeting_groups": 0,
    }]
    r = requests.post('https://api.vk.com/method/ads.updateAds',params={'account_id': 1900013999,
                                                                        'access_token': '770ccb3bf8095651170d3580c9d78b32ba04c865374815c7b7864c94bcee7fab338169b89358f7d3710d7',
                                                                        'data': json.dumps(data), 'v': '5.73'})
    print(r.json())


