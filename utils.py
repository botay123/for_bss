import json
from typing import List

import requests

from config import Buddie, settings, RequestData


def get_contacts_from_json() -> List[Buddie]:
    """Получаем список контактов"""
    with open('contacts.json', 'r') as f:
        text = f.read()

    data = json.loads(text)

    # список контактов
    buddies = []

    for group in data.get('response').get('data').get('events')[0].get('eventData').get('groups'):
        for buddie in group.get('buddies'):
            # if buddie.get('aimId') == '682401373@chat.agent':
            #     print(1)

            if buddie.get('userType') == 'sms' or buddie.get('aimId') is None:
                continue

            buddies.append(Buddie(aimId=buddie.get('aimId'),
                                  userType=buddie.get('userType'),
                                  chatType=buddie.get('chatType'),
                                  friendly=buddie.get('friendly')
                                  )
                           )
            # print(buddie.get('aimId'), buddie.get('friendly'), buddie.get('userType'), buddie.get('chatType'))

    return buddies


def get_contacts(session: requests.Session, cookies: dict):
    """ работает только сразу после входа, хз почему"""
    headers = {
        'Content-Type': 'application/json'
    }

    url = '''https://u.icq.net/api/v92/bos/nicq-b020k/aim/fetchEvents?aimsid=010.1999577206.2194057066:749204815&first=1&rnd=1718455575.206798&timeout=500&supportedSuggestTypes=text-smartreply%2Csticker-smartreply'''
    r = session.get(url,
                    cookies=cookies
                    )

    print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    j = r.json()
    print(1)


def getChatInfo(session: requests.Session,
                # chatId: str
                ):
    chatId = '688828654@chat.agent'
    url = 'https://u.icq.net/api/v92/rapi/getChatInfo'
    payload = '{"reqId":"' + settings.request_data.reqId + '","aimsid":"' + settings.request_data.aimsid + '","params":{"sn":"' + chatId + '","memberLimit":50}}'

    headers = {
        'Content-Type': 'application/json'
    }
    r = session.post(url,
                     data=payload,
                     headers=headers,
                     cookies=settings.cookies
                     )

    j = r.json()
    print(json.dumps(r.json(), indent=4, ensure_ascii=False))


def getEntryGallery(session: requests.Session, aimId: str) -> str:
    url = 'https://u.icq.net/api/v92/rapi/getEntryGallery'
    # sn = '740975219'
    payload = '{"reqId":"' + settings.request_data.reqId + '","aimsid":"' + settings.request_data.aimsid + '","params":{"sn":"' + aimId + '","entriesInPatch":true,"subreqs":[{"subreqId":"older","fromEntryId":"max","entryCount":-6,"urlType":["video","image"]}]}}'

    r = session.post(url,
                     data=payload,
                     headers=settings.headers,
                     cookies=settings.cookies
                     )

    # j = r.json()
    # print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    lastEntryId = r.json().get('results').get('galleryState').get('lastEntryId').get('mid')
    # print(lastEntryId)
    return lastEntryId


def get(url: str, session: requests.Session, cookies: dict):
    r = session.get(url, cookies=cookies)

    # print(json.dumps(r.json(), indent=4))

    info = r.json().get('result').get('info')
    dlink = info.get('dlink')
    file_name = info.get('file_name')

    data = session.get(dlink)
    with open(file_name, 'wb+') as f:
        f.write(data.content)


def getHistory(session: requests.Session, cookies: dict, request_data: RequestData):
    headers = {
        'Content-Type': 'application/json'
    }

    url = 'https://u.icq.net/api/v92/rapi/getHistory'
    payload = '{"reqId":"' + request_data.reqId + '","aimsid":"' + request_data.aimsid + '","params":{"sn":"740975219","fromMsgId":"-1","count":-20,"lang":"ru","mentions":{"resolve":false},"patchVersion":"7362531439583167349"}}'

    r = session.post(url,
                     data=payload,
                     headers=headers,
                     cookies=cookies
                     )

    # print(json.dumps(r.json(), indent=4))
    j = r.json()
    # i = r.json().get('results').get('messages')
    for msg in r.json().get('results').get('messages'):

        files = msg.get('filesharing')
        if files:
            for f in files:
                file_id = f.get('id')
                mime = f.get('mime')
                return file_id
        else:
            file_id = None
            mime = None
        # print(msg.get('msgId'), msg.get('text'), file_id, mime)

# if __name__ == '__main__':
#     with requests.Session() as sess:
#         # # контакты из файла
#         # for buddie in get_contacts_from_json():
#         #
#         #     # получить id последнего сообщения
#         #     lastEntryId = getEntryGallery(sess, buddie.aimId)
#
#         #
#         # getChatInfo(sess)
#
#         # post (получить историю сообщений)
#         img = getHistory(sess, settings.cookies, settings.request_data)
#
#         # # get (получить ссылку на картинку, взять id и подставить после info)
#         # # url = 'https://u.icq.net/api/v92/files/info/06F1Q000ZV9X7BYmfhZMub6666f0221bg/?aimsid=006.3180876220.2071638319%3A749204815&previews=192%2C600%2C800%2Cxlarge'
#         # url = f'https://u.icq.net/api/v92/files/info/{img}/?aimsid=006.3180876220.2071638319%3A749204815&previews=192%2C600%2C800%2Cxlarge'
#         # get(url, sess, settings.cookies)
