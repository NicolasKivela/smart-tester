
from pydantic import BaseModel

class test_script(BaseModel):
    id: int
    feature_id: int
    bdd_ids: list
    script_code: str
