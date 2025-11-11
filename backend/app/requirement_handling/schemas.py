from pydantic import BaseModel,HttpUrl
class Credentials(BaseModel):
    username: str
    password: str

class UrlCredentials(BaseModel):
    url: HttpUrl
    username: str
    password: str

class Extracted_Reqs(BaseModel):
    topic_reqs: list [str]
