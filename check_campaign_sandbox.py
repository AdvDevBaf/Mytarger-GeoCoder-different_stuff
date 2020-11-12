import requests
import json
import time


def update_tokens(accounts,refresh):
    tokens = []
    header = {'Host': 'target-sandbox.my.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    for ids in accounts:
        access_token_req = {
            "client_id": str(ids),
            "client_secret": str(accounts[ids]),
            "refresh_token": str(refresh[ids]),
            "grant_type": "refresh_token"
        }

        response = requests.post('https://target-sandbox.my.com/api/v2/oauth2/token.json', data=access_token_req, headers=header)
        print(response.json())
        print('lol')
        tokens.append(response.json()['access_token'])
    return tokens


accounts = {'XUhyi0INml0TpQN6': 'Vso2SvsKCBCifULfgz1NtPxLAAbbkQWLHVEfqmfIIWQNfCARICDOHtq34w4MresYO2moapMUhghvnpfBRWLAMaMJPq2z49UtEJmRDnuA9lzr6m9Ehg1VXWViFVSoD0rktFGI6Qxg8biGe86IFjvaxtcy3X5437L77ppdiXGwKlkRaZTE7RT6oQbdOHUrvj56QFyyLv6NQihRwzMKSKzEjTGXjU7x3ox3kuk7'}

refresh = {'XUhyi0INml0TpQN6': 'Z1DOCNe3pSElZngQsuWi38ijSdRow1QTysfz7BAlGbNBMykPUp5kzDhsIe5qijJGSccetBi9CedTAahyVSTNsSwOlNp4NH4g3sr1nrA6DFnv2AH4OrP1eZTOfx4rzVt6do1zT5kEjYTGEELzqoFPFd8vFavpHTNWkmLxLKjmDPvRnVRkG3Un5QDmypNEFreLEA9IVdbRfhoAIQz3PF1a4Ban3noQUg1J75qWD54bgZESixnG'}

accounts_tokens = update_tokens(accounts, refresh)

clients_accounts = {}
clients_refresh = {}
tokens = accounts_tokens


proxies = {
    'http': '154.117.191.114:60028',
    'https': '154.117.191.114:60028',
}


for token in tokens:
    campaigns = []
    campaignss = []
    header = {'Host': 'target-sandbox.my.com', 'Content-Type': 'application/json', 'Accept-Encoding': 'gzip, deflate, compress',
              'Authorization': 'Bearer '+str(token)}
    response = requests.get('https://target-sandbox.my.com/api/v1/campaigns.json', headers=header)
    for i in range(len(response.json())):
        if str(response.json()[i]['status']) == 'active':
            campaigns.append(str(response.json()[i]['id']))
            print('id')
            print(str(response.json()[i]))
            campaignss.append(str(response.json()[i]['name']))
    campaigns.reverse()
    print(campaigns)
    print(campaignss)
    for campaign in campaigns:
        print("sleeping")
        time.sleep(10)
        response = requests.get('https://target-sandbox.my.com/api/v1/campaigns/'+str(campaign)+'.json', headers=header)
        print(response.json())
        if str(response.json()['date_end']) == '' or str(response.json()['budget_limit']) == '' or str(response.json()['budget_limit']) == 0:
            data = {'name': str('ПРОВЕРИТЬ_')+str(response.json()['name']), 'status': 'blocked'}
            edit_coms = requests.post('https://target-sandbox.my.com/api/v1/campaigns/' + str(campaign) + '.json',
                                      data=json.dumps(data), headers=header)
            print(edit_coms.json())
            response = requests.post("https://api.telegram.org/bot759523145:AAEKxCONmNdMfsWBWAusKTvOsw_DB2Ok86M/sendMessage?chat_id=195831781&text="+str('ПРОВЕРИТЬ_')+str(response.json()['name']), proxies=proxies)
        else:
            print('campaign '+str(campaign)+' is OK')

