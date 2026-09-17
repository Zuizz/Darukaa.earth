from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class GeoJSONPolygon(BaseModel):
    type: str = "Polygon"
    coordinates: list[list[list[float]]]


class SiteBase(BaseModel):
    name: str
    project_id: str = Field(alias="projectId")
    site_type: str | None = Field(default=None, alias="siteType")
    geometry: GeoJSONPolygon | dict[str, Any]

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class SiteCreate(SiteBase):
    pass


class SiteOut(SiteBase):
    id: str
    created_at: datetime = Field(alias="createdAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


SiteResponse = SiteOut

