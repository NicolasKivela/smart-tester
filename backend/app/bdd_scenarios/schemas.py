from pydantic import BaseModel

class BDD_Scenario(BaseModel):
    id:int
    feature: str
    scenario: str
    given: list
    when: list
    then: list

