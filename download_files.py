import json
import os
from time import sleep
from pathlib import Path

import requests
from tqdm import tqdm

from utils import get_contacts_from_json, getFolders, contacts_from_filter, get_logger
from config import settings, get_user_config


def getFiles(img_id: str, path: str):
    with requests.Session() as session:
        url = f'https://u.icq.net/api/v92/files/info/{img_id}/?aimsid={user_config.request_data.aimsid}'

        r = session.get(url, cookies=user_config.cookies)
        sleep(settings.wait_interval)

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
    user_config = get_user_config()
    filtered_contacts = contacts_from_filter()

    logger = get_logger()

    skip = False
    start_folder = ''  # имя папки, если вдруг надо начать не с начала

    pbar = tqdm(total=len(contacts), ascii=True)

    for contact in contacts:

        if contact not in filtered_contacts:
            continue

        pbar.set_postfix_str(contact.friendly)

        if contact.friendly == start_folder:
            skip = False

        folders = getFolders(contact)
        aimId = contact.aimId

        json_path = folders.get('json_path')
        img_path = folders.get('img_path')
        files = os.listdir(json_path)

        if len(files) == 0 or skip:
            continue

        for file in files:
            with open(f'{json_path}/{file}', 'r', encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                except Exception as e:
                    logger.error(f'Не удалось распарсить json {e.args}')
                    continue

            for msg in data:
                if 'filesharing' in msg:
                    for filesharing in msg.get('filesharing'):
                        f_id = filesharing.get('id')
                        try:
                            getFiles(f_id, img_path)
                        except Exception as e:
                            logger.error(e.args)
