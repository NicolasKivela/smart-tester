from pydantic import BaseModel
from typing import Optional

class BDD_Scenario(BaseModel):
    scenario: str
    content: str
class Generate_BDD(BaseModel):
    prompt: str
    feature: str