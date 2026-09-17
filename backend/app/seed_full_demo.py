import sys
import uuid
from shapely.geometry import shape
from geoalchemy2.shape import from_shape

from app.core.database import SessionLocal
from app.models.project import Project
from app.models.site import Site
from app.seed_metrics import seed_metrics_for_all_sites

INITIAL_PROJECTS = [
    {
        "id": "prj-001",
        "name": "Kaaveri Agroforestry Programme",
        "type": "carbon",
        "status": "active",
        "description": "Afforestation & soil carbon enhancement across the Kaveri river basin in South India.",
    },
    {
        "id": "prj-002",
        "name": "Sundarbans Mangrove Restoration",
        "type": "biodiversity",
        "status": "monitoring",
        "description": "Community-led mangrove canopy recovery and intertidal habitat protection in West Bengal.",
    },
    {
        "id": "prj-003",
        "name": "Western Ghats Canopy Corridor",
        "type": "carbon",
        "status": "active",
        "description": "High-altitude shola forest regeneration and biodiversity sanctuary in Coorg.",
    },
]

INITIAL_SITES = [
    {
        "id": "site-k-001",
        "name": "Upper Basin Sector 4",
        "project_id": "prj-001",
        "site_type": "carbon",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[75.78, 12.38], [75.85, 12.38], [75.85, 12.45], [75.78, 12.45], [75.78, 12.38]]],
        },
    },
    {
        "id": "site-k-002",
        "name": "Delta Buffer Zone B",
        "project_id": "prj-001",
        "site_type": "carbon",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[79.58, 10.73], [79.66, 10.73], [79.66, 10.81], [79.58, 10.81], [79.58, 10.73]]],
        },
    },
    {
        "id": "site-sun-001",
        "name": "Plot Alpha — Gosaba Block",
        "project_id": "prj-002",
        "site_type": "biodiversity",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[88.78, 22.13], [88.86, 22.13], [88.86, 22.21], [88.78, 22.21], [88.78, 22.13]]],
        },
    },
    {
        "id": "site-sun-002",
        "name": "Plot Beta — Satjelia Island",
        "project_id": "prj-002",
        "site_type": "biodiversity",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[88.86, 22.10], [88.94, 22.10], [88.94, 22.18], [88.86, 22.18], [88.86, 22.10]]],
        },
    },
    {
        "id": "site-sun-003",
        "name": "Estuary Reserve Sector 3",
        "project_id": "prj-002",
        "site_type": "biodiversity",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[88.73, 22.03], [88.81, 22.03], [88.81, 22.11], [88.73, 22.11], [88.73, 22.03]]],
        },
    },
    {
        "id": "site-coorg-001",
        "name": "Kodagu Evergreen Block 1",
        "project_id": "prj-003",
        "site_type": "carbon",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[75.68, 12.28], [75.76, 12.28], [75.76, 12.36], [75.68, 12.36], [75.68, 12.28]]],
        },
    },
    {
        "id": "site-coorg-002",
        "name": "Brahmagiri Ridge Extension",
        "project_id": "prj-003",
        "site_type": "carbon",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[75.63, 11.93], [75.71, 11.93], [75.71, 12.01], [75.63, 12.01], [75.63, 11.93]]],
        },
    },
]


def seed_full_demo():
    db = SessionLocal()
    try:
        # 1. Seed Projects
        print("Seeding demo projects...")
        for p_data in INITIAL_PROJECTS:
            existing = db.query(Project).filter(Project.id == p_data["id"]).first()
            if not existing:
                prj = Project(
                    id=p_data["id"],
                    name=p_data["name"],
                    type=p_data["type"],
                    status=p_data["status"],
                    description=p_data["description"],
                )
                db.add(prj)
                print(f"Created project: {prj.id} ({prj.name})")
            else:
                print(f"Project already exists: {existing.id}")

        db.commit()

        # 2. Seed Sites
        print("Seeding demo sites with PostGIS polygons...")
        for s_data in INITIAL_SITES:
            existing = db.query(Site).filter(Site.id == s_data["id"]).first()
            if not existing:
                s_geom = shape(s_data["geometry"])
                wkb_geom = from_shape(s_geom, srid=4326)
                site = Site(
                    id=s_data["id"],
                    name=s_data["name"],
                    project_id=s_data["project_id"],
                    site_type=s_data["site_type"],
                    geometry=wkb_geom,
                )
                db.add(site)
                print(f"Created site: {site.id} ({site.name})")
            else:
                print(f"Site already exists: {existing.id}")

        db.commit()

        # 3. Seed Metrics
        print("Seeding 12-month telemetry metrics for all sites...")
        metrics_count = seed_metrics_for_all_sites(db)
        print(f"Full demo seed complete. Inserted/updated {metrics_count} metric records.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding demo database: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_full_demo()
