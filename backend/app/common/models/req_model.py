from pydantic import BaseModel,HttpUrl
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from app.common.models.bdd_model import BDDScenario 
class Credentials(BaseModel):
    username: str | None
    password: str | None

class UrlCredentials(BaseModel):
    url: HttpUrl
    credentials: Credentials

class Processed_Req(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    feature: str
    summary: str 
    requirements: list["Extracted_Reqs"] = Relationship(back_populates="processed_req")
    bdd_scenarios: list["BDDScenario"] = Relationship(back_populates="requirement")
class Req_Topics(BaseModel):
    # topics: list
    topics: list[str]
class Extracted_Reqs(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_reqs: str  
    processed_req_id: Optional[int] = Field(default=None, foreign_key="processed_req.id")

    processed_req: Optional["Processed_Req"] = Relationship(back_populates="requirements")