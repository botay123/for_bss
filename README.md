### Скрипт для экспорта данных из ICQ

Для работы необходимо:

1. Зайти в бразуер, нажать F12
2. Авторизироваться в icq web
3. Скопировать из запросов список контактов, id и куки
   domain_sid
   tmr_detect

   reqId
   aimsid

   вставить данные в config.py

4. Запустить сначала получение истории json [history_to_json.py](history_to_json.py)
5. Запустить получение файлов [download_files.py](download_files.py)