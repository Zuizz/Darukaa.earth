import uuid
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.site import Site
from app.models.project import Project
from app.models.metric import SiteMetric

# 12-month calendar matching mockMetrics.js
MONTHS = [
    ("2023-12", "Dec 23"),
    ("2024-01", "Jan 24"),
    ("2024-02", "Feb 24"),
    ("2024-03", "Mar 24"),
    ("2024-04", "Apr 24"),
    ("2024-05", "May 24"),
    ("2024-06", "Jun 24"),
    ("2024-07", "Jul 24"),
    ("2024-08", "Aug 24"),
    ("2024-09", "Sep 24"),
    ("2024-10", "Oct 24"),
    ("2024-11", "Nov 24"),
]

# Hardcoded reference series from mockMetrics.js for exact 1-to-1 consistency
KNOWN_SITE_SERIES = {
    "site-k-001": {
        "canopy": [64.2, 63.8, 61.5, 59.1, 57.4, 63.0, 69.3, 72.8, 74.2, 73.5, 71.4, 72.4],
        "carbon": [12.4, 11.8, 10.2, 9.4, 8.8, 15.2, 19.8, 22.4, 21.6, 18.2, 16.4, 18.6],
        "biomass": 138.5,
        "health": 86,
    },
    "site-k-002": {
        "canopy": [58.5, 57.9, 56.1, 54.3, 53.0, 58.6, 63.4, 66.8, 67.5, 66.9, 65.2, 66.1],
        "carbon": [10.1, 9.8, 8.7, 7.9, 7.4, 12.8, 16.5, 18.9, 18.2, 15.6, 13.9, 15.3],
        "biomass": 119.2,
        "health": 78,
    },
    "site-sun-001": {
        "biodiversity": [71.0, 72.4, 73.2, 71.8, 69.5, 74.0, 78.6, 82.1, 83.4, 82.0, 80.8, 81.5],
        "species": [26, 28, 30, 27, 24, 32, 42, 48, 46, 40, 34, 35],
        "disturbance": 1.6,
        "health": 82,
    },
    "site-sun-002": {
        "biodiversity": [79.2, 80.1, 80.8, 79.4, 77.8, 81.5, 85.0, 88.3, 89.1, 88.0, 86.5, 87.2],
        "species": [32, 34, 35, 31, 28, 37, 46, 52, 50, 44, 39, 40],
        "disturbance": 1.1,
        "health": 89,
    },
    "site-sun-003": {
        "biodiversity": [66.5, 67.2, 68.0, 66.8, 65.1, 69.4, 73.1, 76.5, 77.2, 76.0, 74.5, 75.4],
        "species": [22, 23, 25, 23, 20, 27, 35, 41, 38, 33, 29, 31],
        "disturbance": 2.4,
        "health": 76,
    },
    "site-coorg-001": {
        "canopy": [73.5, 73.1, 71.8, 70.2, 69.4, 73.8, 77.2, 79.5, 80.1, 79.4, 78.1, 78.6],
        "carbon": [14.8, 14.2, 13.0, 12.1, 11.5, 17.6, 22.5, 25.1, 24.2, 21.0, 18.5, 19.9],
        "biomass": 164.2,
        "health": 91,
    },
    "site-coorg-002": {
        "canopy": [65.4, 64.9, 63.8, 62.1, 61.5, 66.2, 70.1, 72.4, 73.0, 72.1, 70.8, 71.2],
        "carbon": [12.6, 12.0, 11.1, 10.2, 9.8, 15.0, 19.1, 21.4, 20.8, 18.0, 15.7, 16.8],
        "biomass": 141.0,
        "health": 84,
    },
}

# Seasonal phenology multipliers: dry season dip (Apr-May), monsoon flush (Jun-Sep), stabilization (Oct-Nov)
CANOPY_FACTORS = [0.95, 0.94, 0.91, 0.88, 0.86, 0.94, 1.02, 1.07, 1.09, 1.07, 1.04, 1.05]
CARBON_FACTORS = [0.78, 0.74, 0.64, 0.59, 0.55, 0.95, 1.23, 1.40, 1.35, 1.14, 1.03, 1.16]
BIO_FACTORS =    [0.95, 0.96, 0.98, 0.96, 0.93, 0.99, 1.04, 1.08, 1.09, 1.07, 1.05, 1.06]
SPECIES_FACTORS = [0.72, 0.77, 0.83, 0.75, 0.66, 0.88, 1.19, 1.36, 1.30, 1.13, 0.97, 1.00]


def generate_site_metrics_rows(site_id: str, is_carbon: bool = True) -> list[dict]:
    """Generates 12 monthly rows following the Indian seasonal phenology model."""
    if site_id in KNOWN_SITE_SERIES:
        known = KNOWN_SITE_SERIES[site_id]
        rows = []
        is_known_carbon = "canopy" in known
        for i, (ym, _) in enumerate(MONTHS):
            if is_known_carbon:
                row = {
                    "month": ym,
                    "canopy_cover": known["canopy"][i],
                    "carbon_sequestration": known["carbon"][i],
                    "biomass_density": round(known["biomass"] * (0.95 + 0.05 * (i / 11)), 1),
                    "health_score": round(known["health"] * (0.92 + 0.08 * (CANOPY_FACTORS[i] - 0.86) / 0.23), 1),
                    "biodiversity_index": None,
                    "species_count": None,
                    "disturbance_index": None,
                }
            else:
                row = {
                    "month": ym,
                    "biodiversity_index": known["biodiversity"][i],
                    "species_count": known["species"][i],
                    "disturbance_index": known["disturbance"],
                    "health_score": round(known["health"] * (0.92 + 0.08 * (BIO_FACTORS[i] - 0.93) / 0.16), 1),
                    "canopy_cover": None,
                    "carbon_sequestration": None,
                    "biomass_density": None,
                }
            rows.append(row)
        return rows

    # Deterministic base per site id hash
    base_seed = sum(ord(c) for c in site_id) % 15
    rows = []

    if is_carbon:
        base_canopy = 64.0 + (base_seed * 0.7)
        base_carbon = 14.0 + (base_seed * 0.4)
        base_biomass = 125.0 + (base_seed * 2.5)
        base_health = 78.0 + (base_seed * 0.8)

        for i, (ym, _) in enumerate(MONTHS):
            canopy = round(base_canopy * CANOPY_FACTORS[i], 1)
            carbon = round(base_carbon * CARBON_FACTORS[i], 1)
            biomass = round(base_biomass * (0.96 + 0.04 * (i / 11)), 1)
            health = round(base_health * (0.94 + 0.06 * (CANOPY_FACTORS[i] - 0.86) / 0.23), 1)

            rows.append({
                "month": ym,
                "canopy_cover": canopy,
                "carbon_sequestration": carbon,
                "biomass_density": biomass,
                "health_score": min(98.0, health),
                "biodiversity_index": None,
                "species_count": None,
                "disturbance_index": None,
            })
    else:
        base_bio = 75.0 + (base_seed * 0.8)
        base_species = 35 + (base_seed % 10)
        dist_val = round(1.2 + (base_seed % 8) * 0.15, 1)
        base_health = 80.0 + (base_seed * 0.7)

        for i, (ym, _) in enumerate(MONTHS):
            bio = round(base_bio * BIO_FACTORS[i], 1)
            species = int(round(base_species * SPECIES_FACTORS[i]))
            health = round(base_health * (0.95 + 0.05 * (BIO_FACTORS[i] - 0.93) / 0.16), 1)

            rows.append({
                "month": ym,
                "biodiversity_index": bio,
                "species_count": species,
                "disturbance_index": dist_val,
                "health_score": min(98.0, health),
                "canopy_cover": None,
                "carbon_sequestration": None,
                "biomass_density": None,
            })

    return rows


def seed_metrics_for_all_sites(db: Session) -> int:
    """Seeds 12 months of metrics for every site currently in the database."""
    sites = db.query(Site).all()
    if not sites:
        print("No sites found in database to seed.")
        return 0

    total_inserted = 0
    for site in sites:
        # Determine project type
        project = db.query(Project).filter(Project.id == site.project_id).first()
        is_carbon = True
        if project and project.type == "biodiversity":
            is_carbon = False
        elif site.site_type and "bio" in site.site_type.lower():
            is_carbon = False

        rows = generate_site_metrics_rows(site.id, is_carbon=is_carbon)

        # Upsert each monthly metric
        for r in rows:
            existing = (
                db.query(SiteMetric)
                .filter(SiteMetric.site_id == site.id, SiteMetric.month == r["month"])
                .first()
            )
            if not existing:
                metric = SiteMetric(
                    id=f"met-{uuid.uuid4().hex[:8]}",
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
                total_inserted += 1
            else:
                # Update existing row with calibrated values
                existing.canopy_cover = r["canopy_cover"]
                existing.carbon_sequestration = r["carbon_sequestration"]
                existing.biomass_density = r["biomass_density"]
                existing.biodiversity_index = r["biodiversity_index"]
                existing.species_count = r["species_count"]
                existing.disturbance_index = r["disturbance_index"]
                existing.health_score = r["health_score"]

        db.commit()
        print(f"Seeded 12 metrics for site: {site.id} ({site.name}) [type={'carbon' if is_carbon else 'biodiversity'}]")

    return total_inserted


if __name__ == "__main__":
    db = SessionLocal()
    try:
        count = seed_metrics_for_all_sites(db)
        print(f"Metrics seeding complete. Total records inserted/updated: {count}")
    finally:
        db.close()
