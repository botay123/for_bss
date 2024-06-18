import json
from typing import List

import requests

from config import Buddie, settings, RequestData


def getHistory(session: requests.Session, sn='740975219', fromMsgId='-1', count='-20'):
    url = 'https://u.icq.net/api/v92/rapi/getHistory'
    payload = {"reqId": settings.request_data.reqId,
               "aimsid": settings.request_data.aimsid,
               "params": {
                   "sn": sn,
                   "fromMsgId": fromMsgId,
                   "count": count,
                   "lang": "ru",
                   "mentions": {
                       "resolve": 'false'
                   },
                   "patchVersion": settings.patchVersion
               }
               }
    # data = json.dumps(payload)
    data = '{"reqId":"' + settings.request_data.reqId + '","aimsid":"' + settings.request_data.aimsid + '","params":{"sn":"'+sn+'","fromMsgId":"'+fromMsgId+'","count":'+count+',"lang":"ru","mentions":{"resolve":false},"patchVersion":"'+settings.patchVersion+'"}}'
    r = session.post(url,
                     data=data,
                     headers=settings.headers,
                     cookies=settings.cookies
                     )


    return r.json().get('results').get('messages')


if __name__ == '__main__':
    with requests.Session() as sess:
        data = getHistory(sess)

        with open('results/test.json', 'a+') as f:
            f.write(json.dumps(data, indent=4,ensure_ascii=False))
