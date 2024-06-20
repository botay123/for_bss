import json
import os

from pydantic.v1 import validator, BaseSettings


class Buddie(BaseSettings):
    aimId: str
    userType: str
    chatType: str
    friendly: str

    @validator('chatType', 'friendly', pre=True)
    def none_to_empty_(cls, v: object) -> object:
        if v is None:
            return ''
        return v


class RequestData(BaseSettings):
    reqId: str = ''
    aimsid: str = ''


class UserConfig(BaseSettings):
    request_data: RequestData = RequestData()
    cookies: dict = {
        'cookie-policy-accepted': '1',
        'domain_sid': '',
        'tmr_detect': '',
    }
    patchVersion: str = ''
    headers: dict = {
        'Content-Type': 'application/json;charset=utf-8'
    }

    url_contacts: str = ''


class Settings(BaseSettings):
    directory: str = 'results'
    user_data: str = 'user_data'
    user_settings: str = f'{user_data}/user_settings.json'
    uset_contacts: str = f'{user_data}/contacts.json'
    uset_filter: str = f'{user_data}/filter.txt'
    uset_logs: str = f'{user_data}/logs.log'

    wait_interval: float = 0.1


def get_user_config() -> UserConfig:
    tmp = Settings()

    if not os.path.exists(tmp.user_settings):
        raise Exception(f'Не найдены файлы {tmp.user_settings}, запустите сбор данных для пользователя')

    with open(tmp.user_settings, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    return UserConfig(**data)


settings = Settings()
