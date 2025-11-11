from sqlmodel import Sqlmodel, Field, Relationship
from pydantic import BaseModel
#TODO: Refactor database sqlmodels for test_scripts
class test_script(BaseModel):
    id: int
    feature_id: int
    bdd_ids: list
    script_code: str
