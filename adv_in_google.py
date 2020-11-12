import requests
import openpyxl
import pandas as pd


data = pd.read_csv("C:\\Users\AMasanov\\Desktop\\toddlers.csv", header=None,sep=';', names=['ids', 'name', 'link'],encoding="ISO-8859-1")
ids1 = data['ids'].values.tolist()
name1 = data['name'].values.tolist()
link1 = data['link'].values.tolist()
ids1 = ids1[1:]
name1 = name1[1:]
link1 = link1[1:]

data = pd.read_csv("C:\\Users\AMasanov\\Desktop\\toddlers2.csv", header=None,sep=';', names=['ids', 'name', 'link'],encoding="ISO-8859-1")
ids2 = data['ids'].values.tolist()
name2 = data['name'].values.tolist()
link2 = data['link'].values.tolist()
ids2 = ids2[1:]
name2 = name2[1:]
link2 = link2[1:]

#ids = []
#name = []
#link = []

for i in range(0,len(ids2)):
    if ids2[i] not in ids1:
        ids1.append(ids2[i])
        name1.append(name2[i])
        link1.append(link2[i])
    else:
        print("in ids")

ids = ids1
name = name1
link = link1

adv = []

print(len(ids))
print(len(name))
print(len(link))
for i in range(0,len(ids)):
    page = requests.get('https://play.google.com/store/apps/details?id='+str(ids[i]))
    if 'Contains Ads' in page.text:
        print('yes')
        adv.append('yes')
    else:
        print('no')
        adv.append('no')

print(adv)

table = pd.DataFrame({'id': ids, 'Название': name,'Ссылка': link,'Реклама в приложении':adv})
table.to_csv(str("C:\\Users\AMasanov\\Desktop\\") + '/' + str("Малыши") + '.csv', sep=';', index=False,
             encoding='utf-8-sig')
print('ok')
