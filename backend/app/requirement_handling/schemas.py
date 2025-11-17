from pydantic import BaseModel,HttpUrl
from typing import Optional
class Credentials(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    

class UrlCredentials(BaseModel):
    url: HttpUrl
    username: Optional[str] = None
    password: Optional[str] = None

class Extracted_Reqs(BaseModel):
    topic_reqs: list [str]
