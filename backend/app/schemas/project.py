from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str
    type: str  # 'carbon' | 'biodiversity'
    status: str = "active"  # 'active' | 'monitoring' | 'archived'
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    status: str | None = None
    description: str | None = None


class ProjectOut(ProjectBase):
    id: str
    site_count: int = Field(default=0, serialization_alias="siteCount")
    last_updated: datetime = Field(serialization_alias="lastUpdated")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


ProjectResponse = ProjectOut
