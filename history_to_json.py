import json
from typing import List

import requests

from config import Buddie, settings, RequestData


def getHistory(session: requests.Session, sn='740975219', fromMsgId='-1', count='-50'):
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

    return r.json().get('results').get('messages')


if __name__ == '__main__':
    with requests.Session() as sess:

        data = getHistory(sess)
        count = 0
        while True:
            count += 1
            if len(data) > 0:
                last_id = data[-1].get('msgId')
                with open(f'results/test{count}.json', 'a+') as f:
                    f.write(json.dumps(data, indent=4, ensure_ascii=False))

                data = getHistory(sess, fromMsgId=last_id)

            else:
                break
