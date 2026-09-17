from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PrimaryMetricOut(BaseModel):
    label: str
    unit: str
    current_value: str = Field(alias="currentValue")
    annual_change: str = Field(alias="annualChange")
    description: str
    trend: list[float]

    model_config = ConfigDict(populate_by_name=True)


class SecondaryMetricOut(BaseModel):
    label: str
    unit: str
    total_annual: str = Field(alias="totalAnnual")
    description: str
    trend: list[float | int]

    model_config = ConfigDict(populate_by_name=True)


class SupportingMetricOut(BaseModel):
    label: str
    value: str
    change: str

    model_config = ConfigDict(populate_by_name=True)


class SiteMetricRecord(BaseModel):
    id: str
    site_id: str = Field(alias="siteId")
    month: str
    canopy_cover: float | None = Field(default=None, alias="canopyCover")
    carbon_sequestration: float | None = Field(default=None, alias="carbonSequestration")
    biomass_density: float | None = Field(default=None, alias="biomassDensity")
    biodiversity_index: float | None = Field(default=None, alias="biodiversityIndex")
    species_count: int | None = Field(default=None, alias="speciesCount")
    disturbance_index: float | None = Field(default=None, alias="disturbanceIndex")
    health_score: float | None = Field(default=None, alias="healthScore")
    created_at: datetime | None = Field(default=None, alias="createdAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SiteMetricOut(BaseModel):
    site_id: str = Field(alias="siteId")
    type: str
    health_score: float = Field(alias="healthScore")
    health_target: float = Field(alias="healthTarget")
    primary_metric: PrimaryMetricOut = Field(alias="primaryMetric")
    secondary_metric: SecondaryMetricOut = Field(alias="secondaryMetric")
    supporting_metric: SupportingMetricOut = Field(alias="supportingMetric")
    months: list[str] = Field(default_factory=list)
    records: list[SiteMetricRecord] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
