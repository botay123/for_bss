import json
import os
from time import sleep
from pathlib import Path

import requests

from history_to_json import getFolders
from scripts import get_contacts_from_json
from config import settings


def getImage(img_id: str, path: str):
    with requests.Session() as session:
        # url = f'https://u.icq.net/api/v92/files/info/{img_id}/?aimsid={settings.request_data.aimsid}%3A749204815&previews=192%2C600%2C800%2Cxlarge'
        url = f'https://u.icq.net/api/v92/files/info/{img_id}/?aimsid={settings.request_data.aimsid}'

        r = session.get(url, cookies=settings.cookies)
        sleep(0.5)

        info = r.json().get('result').get('info')
        dlink = info.get('dlink')
        file_name = info.get('file_name')

        data = session.get(dlink)

        img_path = f'{path}/{file_name}'
        my_file = Path(img_path)
        if my_file.is_file():
            return

        with open(img_path, 'wb+') as f:
            f.write(data.content)


if __name__ == '__main__':
    contacts = get_contacts_from_json()

    for contact in contacts:
        print(contact)
        folders = getFolders(contact)
        aimId = contact.aimId

        json_path = folders.get('json_path')
        img_path = folders.get('img_path')
        files = os.listdir(json_path)

        if len(files) == 0:
            continue

        for file in files:
            with open(f'{json_path}/{file}', 'r') as f:
                data = json.loads(f.read())
            for msg in data:
                if 'filesharing' in msg:
                    for filesharing in msg.get('filesharing'):
                        f_id = filesharing.get('id')
                        try:
                            getImage(f_id, img_path)
                        except Exception as e:
                            print(e.args)
