from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.site import Site
from app.models.project import Project
from app.models.metric import SiteMetric
from app.schemas.metric import (
    SiteMetricOut,
    PrimaryMetricOut,
    SecondaryMetricOut,
    SupportingMetricOut,
    SiteMetricRecord,
)
from app.seed_metrics import generate_site_metrics_rows

router = APIRouter(tags=["metrics"])

# Helper mapping for YYYY-MM to frontend label format (e.g. '2024-06' -> 'Jun 24')
MONTH_LABEL_MAP = {
    "2023-12": "Dec 23",
    "2024-01": "Jan 24",
    "2024-02": "Feb 24",
    "2024-03": "Mar 24",
    "2024-04": "Apr 24",
    "2024-05": "May 24",
    "2024-06": "Jun 24",
    "2024-07": "Jul 24",
    "2024-08": "Aug 24",
    "2024-09": "Sep 24",
    "2024-10": "Oct 24",
    "2024-11": "Nov 24",
}


def _format_month_label(ym: str) -> str:
    if ym in MONTH_LABEL_MAP:
        return MONTH_LABEL_MAP[ym]
    try:
        dt = datetime.strptime(ym, "%Y-%m")
        return dt.strftime("%b %y")
    except ValueError:
        return ym


@router.get("/sites/{id}/metrics", response_model=SiteMetricOut)
def get_site_metrics(id: str, db: Session = Depends(get_db)):
    """
    Returns the 12-month time series analytics metrics for a specific site.
    Payload shape conforms to the expectations of SiteDetail.jsx chart components.
    """
    site = db.query(Site).filter(Site.id == id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    metrics = (
        db.query(SiteMetric)
        .filter(SiteMetric.site_id == id)
        .order_by(SiteMetric.month.asc())
        .all()
    )

    # Determine site type
    project = db.query(Project).filter(Project.id == site.project_id).first()
    is_carbon = True
    if project and project.type == "biodiversity":
        is_carbon = False
    elif site.site_type and "bio" in site.site_type.lower():
        is_carbon = False

    # If no metrics exist for this site, generate and persist initial 12-month series
    if not metrics:
        seed_rows = generate_site_metrics_rows(site.id, is_carbon=is_carbon)
        for r in seed_rows:
            metric = SiteMetric(
                site_id=site.id,
                month=r["month"],
                canopy_cover=r["canopy_cover"],
                carbon_sequestration=r["carbon_sequestration"],
                biomass_density=r["biomass_density"],
                biodiversity_index=r["biodiversity_index"],
                species_count=r["species_count"],
                disturbance_index=r["disturbance_index"],
                health_score=r["health_score"],
            )
            db.add(metric)
        db.commit()
        metrics = (
            db.query(SiteMetric)
            .filter(SiteMetric.site_id == id)
            .order_by(SiteMetric.month.asc())
            .all()
        )

    first = metrics[0]
    latest = metrics[-1]
    months_labels = [_format_month_label(m.month) for m in metrics]

    if is_carbon:
        canopy_trend = [m.canopy_cover if m.canopy_cover is not None else 65.0 for m in metrics]
        carbon_trend = [m.carbon_sequestration if m.carbon_sequestration is not None else 15.0 for m in metrics]
        
        canopy_diff = latest.canopy_cover - first.canopy_cover if (latest.canopy_cover and first.canopy_cover) else 5.0
        annual_sequestration = sum(m.carbon_sequestration or 0.0 for m in metrics)
        
        biomass_latest = latest.biomass_density if latest.biomass_density is not None else 130.0
        biomass_first = first.biomass_density if first.biomass_density is not None else 125.0
        biomass_pct = ((biomass_latest - biomass_first) / biomass_first * 100.0) if biomass_first else 4.0

        current_health = latest.health_score if latest.health_score is not None else 85.0
        health_target = min(98.0, current_health + 5.0)

        primary_metric = PrimaryMetricOut(
            label="Canopy Cover",
            unit="%",
            currentValue=f"{latest.canopy_cover:.1f}%" if latest.canopy_cover else "70.0%",
            annualChange=f"{canopy_diff:+.1f}%",
            description="Satellite-derived canopy cover percentage (Sentinel-2 NDVI composite)",
            trend=canopy_trend,
        )

        secondary_metric = SecondaryMetricOut(
            label="Carbon Sequestration",
            unit="tCO₂e/mo",
            totalAnnual=f"{annual_sequestration:.1f} tCO₂e",
            description="Monthly estimated above-ground biomass carbon increment",
            trend=carbon_trend,
        )

        supporting_metric = SupportingMetricOut(
            label="Biomass Density",
            value=f"{biomass_latest:.1f} Mg/ha",
            change=f"{biomass_pct:+.1f}% YoY",
        )

        site_type_str = "carbon"

    else:
        bio_trend = [m.biodiversity_index if m.biodiversity_index is not None else 80.0 for m in metrics]
        species_trend = [m.species_count if m.species_count is not None else 35 for m in metrics]

        bio_diff = (latest.biodiversity_index - first.biodiversity_index) if (latest.biodiversity_index and first.biodiversity_index) else 6.0
        annual_observations = sum(m.species_count or 0 for m in metrics)

        dist_latest = latest.disturbance_index if latest.disturbance_index is not None else 1.5
        dist_first = first.disturbance_index if first.disturbance_index is not None else 1.8
        dist_diff = dist_latest - dist_first

        current_health = latest.health_score if latest.health_score is not None else 82.0
        health_target = min(98.0, current_health + 6.0)

        primary_metric = PrimaryMetricOut(
            label="Biodiversity Index",
            unit="/100",
            currentValue=f"{latest.biodiversity_index:.1f}" if latest.biodiversity_index else "80.0",
            annualChange=f"{bio_diff:+.1f} pts",
            description="Composite bio-acoustic and ground survey index across intertidal flora/fauna",
            trend=bio_trend,
        )

        secondary_metric = SecondaryMetricOut(
            label="Species Observations",
            unit="species",
            totalAnnual=f"{annual_observations} records",
            description="Monthly unique flora and fauna species identified during transect surveys",
            trend=species_trend,
        )

        supporting_metric = SupportingMetricOut(
            label="Disturbance Index",
            value=f"{dist_latest:.1f} / 10",
            change=f"{dist_diff:+.1f} YoY (low)",
        )

        site_type_str = "biodiversity"

    records = [
        SiteMetricRecord.model_validate(m)
        for m in metrics
    ]

    return SiteMetricOut(
        siteId=site.id,
        type=site_type_str,
        healthScore=round(current_health, 1),
        healthTarget=round(health_target, 1),
        primaryMetric=primary_metric,
        secondaryMetric=secondary_metric,
        supportingMetric=supporting_metric,
        months=months_labels,
        records=records,
    )
