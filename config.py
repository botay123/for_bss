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
    reqId: str = '69426-1718634050'
    aimsid: str = '010.1999577206.2194057066:749204815'


class Settings(BaseSettings):
    request_data: RequestData = RequestData()
    cookies: dict = {
        'cookie-policy-accepted': '1',
        'domain_sid': 'RbPQzywpfY4tELKKGzT_y%3A1718633839478',
        'tmr_detect': '0%7C1718633946104',
    }
    patchVersion: str = '7362531439583167349'
    headers: dict = {
        'Content-Type': 'application/json;charset=utf-8'
    }

    directory: str = 'results'

settings = Settings()
