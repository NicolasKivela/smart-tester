
from pydantic import BaseModel

class test_script(BaseModel):
    id: int
    bdd_id: int
    content: str
