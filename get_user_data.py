import json
import os
import re

import requests

from config import settings, RequestData, UserConfig, Settings
from utils import get_contacts_from_json


def parseHar():
    har_file = 'web.icq.com.har'
    if not os.path.exists(har_file):
        raise Exception(f'Не найден файл {har_file}')

    with open(har_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    # данные для запросов в icq
    reqId = None
    aimsid = None
    cookies = None
    patchVersion = None
    url_contacts = None

    for msg in data.get('log').get('entries'):
        reqId_text = msg.get('request', {}).get('postData', {}).get('text', '')
        if 'reqId' in reqId_text and 'patchVersion' in reqId_text:
            reqId = json.loads(reqId_text).get('reqId')
            patchVersion = json.loads(reqId_text).get('params').get('patchVersion')

        querys = msg.get('request', {}).get('queryString', [])
        for query in querys:
            if query.get('name', '') == 'aimsid':
                if '%' not in query.get('value'):
                    aimsid = query.get('value')

        headers = msg.get('request', {}).get('headers', [])
        for header in headers:
            if header.get('name', '') == 'Cookie':
                cookies = {i.split('=')[0].strip(): i.split('=')[1].strip() for i in header.get('value').split(';')}

        url_data = re.search(
            r'https://u\.icq\.net/api/v92/.*/fetchEvents.*first=.*timeout=500&supportedSuggestTypes=text-smartreply%2Csticker-smartreply$',
            msg.get('request', {}).get('url', ''))
        if url_data:
            url_contacts = url_data.group(0)

    request_data = RequestData(reqId=reqId, aimsid=aimsid)
    print(request_data, url_contacts)
    user_config = UserConfig(request_data=request_data, cookies=cookies, patchVersion=patchVersion,
                             url_contacts=url_contacts)

    if not os.path.exists(settings.user_data):
        os.makedirs(settings.user_data)

    if os.path.exists(settings.user_settings):
        print(f'Данные для пользователя уже получены {settings.user_settings}')

    else:
        with open(settings.user_settings, 'w+') as f:
            f.write(user_config.json())
            print(f'Данные для пользователя записаны {settings.user_settings}')

    getContacts(user_config)

    if os.path.exists(settings.uset_filter):
        print(f'Файл фильтра уже существует {settings.uset_filter}')
    else:
        contacts = get_contacts_from_json()
        data = [f'{i.aimId}|{i.userType}|{i.chatType}|{i.friendly}' for i in contacts]
        with open(settings.uset_filter, 'w+', encoding='utf-8') as f:
            f.write('\n'.join(data))
            print(f'Файл фильтра создан {settings.uset_filter}')

    return print('Done!')


def getContacts(user_config: UserConfig):
    r = requests.get(url=user_config.url_contacts, headers=user_config.headers, cookies=user_config.cookies)

    if os.path.exists(settings.uset_contacts):
        print(f'Контакты для пользователя уже получены {settings.uset_contacts}')

    else:
        with open(settings.uset_contacts, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(r.json(), indent=4, ensure_ascii=False))
            print(f'Контакты для пользователя записаны {settings.uset_contacts}')


if __name__ == '__main__':
    parseHar()
