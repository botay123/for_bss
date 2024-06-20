import json

from tqdm import tqdm
import requests

from config import get_user_config
from utils import get_contacts_from_json, getFolders, contacts_from_filter, getChatInfo


def getHistory(session: requests.Session, sn, fromMsgId='-1', count='-50') -> list:
    url = 'https://u.icq.net/api/v92/rapi/getHistory'
    data = '{"reqId":"' + user_config.request_data.reqId + '","aimsid":"' + user_config.request_data.aimsid + '","params":{"sn":"' + sn + '","fromMsgId":"' + fromMsgId + '","count":' + count + ',"lang":"ru","mentions":{"resolve":false},"patchVersion":"' + user_config.patchVersion + '"}}'
    r = session.post(url,
                     data=data,
                     headers=user_config.headers,
                     cookies=user_config.cookies
                     )

    if 'results' in r.json():
        return r.json().get('results').get('messages')
    else:
        return []


if __name__ == '__main__':

    contacts = get_contacts_from_json()
    user_config = get_user_config()
    filtered_contacts = contacts_from_filter()

    pbar = tqdm(total=len(contacts), ascii=True)

    for contact in contacts:

        # пропускаем контакты, которых нет в фильтре
        if contact not in filtered_contacts:
            continue

        pbar.set_postfix_str(contact.friendly)

        folders = getFolders(contact)
        aimId = contact.aimId
        with requests.Session() as sess:

            data = getHistory(sess, aimId)
            getChatInfo(sess, contact, folders, user_config)
            count = 0
            while True:
                count += 1
                if len(data) > 0:
                    last_id = data[-1].get('msgId')
                    with open(f"{folders.get('json_path')}/data_{count}.json", 'w+', encoding="utf-8") as f:
                        f.write(json.dumps(data, indent=4, ensure_ascii=False))

                    data = getHistory(sess, aimId, fromMsgId=last_id)

                else:
                    break

    print('Done!')
