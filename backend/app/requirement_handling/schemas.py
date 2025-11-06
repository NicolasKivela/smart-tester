from pydantic import BaseModel,HttpUrl

class Credentials(BaseModel):
    username: str
    password: str

class UrlCredentials(BaseModel):
    url: HttpUrl
    credentials: Credentials

class Extracted_Reqs(BaseModel):
    topic_reqs: list [str]
