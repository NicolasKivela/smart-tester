from pydantic import BaseModel,HttpUrl

class Credentials(BaseModel):
    username: str
    password: str

class Req_Process(BaseModel):
    url: HttpUrl
    credentials: Credentials

class Processed_Req(BaseModel):
    id: int
    feature: str
    summary: str 
    requirements: list[str]
    bdd_scenarios: list
class Req_Topics(BaseModel):
    # topics: list
    topics: list[str]
