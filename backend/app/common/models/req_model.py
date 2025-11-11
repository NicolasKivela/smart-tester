from datetime import datetime
from pydantic import BaseModel,HttpUrl
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
if TYPE_CHECKING:
    from app.common.models.bdd_model import BDDScenario 

class CoverageStatusEnum(str, Enum):
    covered = "covered"
    partial = "partial"
    missing = "missing"

# ───────────────────────────────
#  requirements_documents table
# ───────────────────────────────
class RequirementDocument(SQLModel, table=True):
    __tablename__ = "requirement_document"

    id: Optional[int] = Field(default=None, primary_key=True)
    document_name: str
    raw_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


    features: List["Feature"] = Relationship(back_populates="requirement_document")

class Feature(SQLModel, table=True):
    __tablename__ = "feature"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    summary: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    requirement_document: Optional["RequirementDocument"] = Relationship(back_populates="features")
    requirement_document_id: Optional[int] = Field(default=None, foreign_key="requirement_document.id")
    # one feature -> many requirements
    requirements: List["Requirement"] = Relationship(back_populates="feature")
    bdd_scenarios: List["BDDScenario"] = Relationship(back_populates="feature")


class Requirement(SQLModel, table=True):
    __tablename__ = "requirements"

    id: Optional[int] = Field(default=None, primary_key=True)
    identifier: str
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # foreign key to the feature
    feature_id: Optional[int] = Field(default=None, foreign_key="feature.id")

    # each requirement belongs to one feature
    feature: Optional[Feature] = Relationship(back_populates="requirements")


# ───────────────────────────────
#  join_feature_requirements table
# ───────────────────────────────
class JoinFeatureRequirement(SQLModel, table=True):
    __tablename__ = "join_feature_requirements"

    feature_id: Optional[int] = Field(foreign_key="feature.id", primary_key=True)
    requirement_id: Optional[int] = Field(foreign_key="requirements.id", primary_key=True)
    coverage_status: Optional[str] = None 