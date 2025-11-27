from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.common.models.req_model import Feature
    from app.common.models.bdd_model import BDDScenario
    from app.common.models.test_script_model import TestScript
class Status(str, Enum):
    ONGOING= "ongoing"
    READY= "ready"
    NEW="new"
    FAILURE="failure"



class LocatorElements(SQLModel, table=True):
    __tablename__ = "locator_element"

    id: Optional[int] = Field(default=None, primary_key=True)
    feature_id: Optional[int] = Field(default=None, foreign_key="feature.id")
    status: Status =Field(default=Status.NEW)
    app_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    locator_items: List["LocatorItem"] = Relationship(back_populates="locator")
    bdd_scenarios: List["BDDScenario"] = Relationship(
        back_populates="locator_element"
    )
    test_script_id: Optional[int] = Field(default=None,foreign_key="test_script.id")
    test_script: Optional["TestScript"] = Relationship(back_populates="locator_element")


class LocatorItem(SQLModel, table=True):
    __tablename__ = "locator_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: Optional[str] = Field(default=None)
    page_url: Optional[str] = Field(default=None)
    task: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    locator_id: Optional[int] = Field(default=None, foreign_key="locator_element.id")

    locator: Optional["LocatorElements"] = Relationship(back_populates="locator_items")
    selectors: List["LocatorSelector"] = Relationship(back_populates="locator_item")


class LocatorSelector(SQLModel, table=True):
    __tablename__ = "locator_selectors"

    id: Optional[int] = Field(default=None, primary_key=True)
    locator_item_id: int = Field(foreign_key="locator_items.id")

    css:Optional[str] = Field(default=None)
    xpath: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    locator_item: Optional["LocatorItem"] = Relationship(back_populates="selectors")


class JoinLocatorsItems(SQLModel, table=True):
    __tablename__ = "join_locators_items"

    locator_id: Optional[int] = Field(foreign_key="locator_element.id", primary_key=True)
    locator_item_id: Optional[int] = Field(foreign_key="locator_items.id", primary_key=True)

