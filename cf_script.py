import requests
import json

ZOHO_AUTH_URL = 'https://accounts.zoho.eu/oauth/v2/token'
ZOHO_REST_URL = 'https://www.zohoapis.eu/crm/v2'
AUTH_HEADERS = {'accept': '*/*'}
HEADERS = {"Authorization": "Bearer token"}
PARAMS = {'grant_type': 'refresh_token',
          'client_id': '1000.AVNMGUJD7V5EVQM42QA60VFKKQ1USR',
          'client_secret': '4baab5f4c79b4e433986ed37e9802a368b82646e67'}

REFRESH_TOKEN = '1000.70778b815d0eca890b6b8678ae310301.513ed1a3df61052a620dd1808c3e8282'

PARAMS['refresh_token'] = REFRESH_TOKEN
# response = requests.post(headers=HEADERS, params=PARAMS, url=ZOHO_AUTH_URL)

# print(json.loads(response.text)['access_token'])


def get_refresh_token():
    response = requests.post(headers=AUTH_HEADERS,
                             params=PARAMS,
                             url=ZOHO_AUTH_URL)
    json_response = json.loads(response.text)
    if 'access_token' in json_response.keys():
        token = json.loads(response.text)['access_token']
        HEADERS['Authorization'] = 'Bearer {}'.format(token)
        return True
    else:
        return False


def get_accounts():
    URL = ZOHO_REST_URL + '/Accounts'
    updated = get_refresh_token()
    if updated:
        response = requests.get(headers=HEADERS, url=URL)
        print(response.text)
    else:
        print('Fail')


get_accounts()
