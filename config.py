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


class Settings(BaseSettings):
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

    directory: str = 'results'
    wait_interval: float = 0.1


settings = Settings()
