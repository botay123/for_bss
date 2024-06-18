import json
from typing import List
import os

import requests

from config import Buddie, settings, RequestData
from scripts import get_contacts_from_json


def getHistory(session: requests.Session, sn, fromMsgId='-1', count='-50') -> list:
    url = 'https://u.icq.net/api/v92/rapi/getHistory'
    # payload = {"reqId": settings.request_data.reqId,
    #            "aimsid": settings.request_data.aimsid,
    #            "params": {
    #                "sn": sn,
    #                "fromMsgId": fromMsgId,
    #                "count": count,
    #                "lang": "ru",
    #                "mentions": {
    #                    "resolve": 'false'
    #                },
    #                "patchVersion": settings.patchVersion
    #            }
    #            }
    # data = json.dumps(payload)
    data = '{"reqId":"' + settings.request_data.reqId + '","aimsid":"' + settings.request_data.aimsid + '","params":{"sn":"' + sn + '","fromMsgId":"' + fromMsgId + '","count":' + count + ',"lang":"ru","mentions":{"resolve":false},"patchVersion":"' + settings.patchVersion + '"}}'
    r = session.post(url,
                     data=data,
                     headers=settings.headers,
                     cookies=settings.cookies
                     )

    if 'results' in r.json():
        return r.json().get('results').get('messages')
    else:
        return []


def getFolders(contact: Buddie) -> dict:
    if contact.friendly != '':
        name = contact.friendly
    else:
        name = contact.aimId

    if not os.path.exists(settings.directory):
        os.makedirs(settings.directory)

    contact_path = f'{settings.directory}/{name}'

    if not os.path.exists(contact_path):
        os.makedirs(contact_path)

    json_path = f'{contact_path}/json'

    if not os.path.exists(json_path):
        os.makedirs(json_path)

    return {'contact_path': contact_path,
            'json_path': json_path,
            'name': name}


if __name__ == '__main__':

    contacts = get_contacts_from_json()

    for contact in contacts:
        print(contact)
        folders = getFolders(contact)
        aimId = contact.aimId
        with requests.Session() as sess:

            data = getHistory(sess, aimId)
            count = 0
            while True:
                count += 1
                if len(data) > 0:
                    last_id = data[-1].get('msgId')
                    with open(f"{folders.get('json_path')}/data_{count}.json", 'a+') as f:
                        f.write(json.dumps(data, indent=4, ensure_ascii=False))

                    data = getHistory(sess, aimId, fromMsgId=last_id)

                else:
                    break
