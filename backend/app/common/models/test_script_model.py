from sqlmodel import SQLModel, Field, Relationship  
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING, List
#TODO: Refactor database sqlmodels for test_scripts
if TYPE_CHECKING:
    from app.common.models import Feature,BDDScenario,LocatorElements
class TestScript(SQLModel, table=True):
    __tablename__ = "test_script"
    id: Optional[int] = Field(default=None,primary_key=True)
    feature_id: Optional[int] = Field(default=None, foreign_key="feature.id")
    bdd_scenarios: List["BDDScenario"] = Relationship(back_populates="test_script")
    locator_element: Optional["LocatorElements"] = Relationship(back_populates="test_script")
    script_code: str
