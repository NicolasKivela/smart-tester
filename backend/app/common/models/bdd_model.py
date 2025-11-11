# app/models/bdd_model.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from app.common.models import Feature, LocatorElements
class BDDScenario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    scenario: str
    content: str

    feature_id: Optional[int] = Field(default=None, foreign_key="feature.id")

    feature: Optional["Feature"] = Relationship(back_populates="bdd_scenarios")
    locator_element: Optional["LocatorElements"] = Relationship(back_populates="bdd_scenarios")
    