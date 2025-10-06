from pydantic import BaseModel,HttpUrl

class Credentials(BaseModel):
    username: str
    password: str
class Req_Process(BaseModel):
    url: HttpUrl
    credentials: Credentials
class Req_Topics(BaseModel):
    topics: list
