from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session
from shapely.geometry import shape, mapping
from geoalchemy2.shape import from_shape, to_shape

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.project import Project
from app.models.site import Site
from app.models.user import User
from app.schemas.site import SiteCreate, SiteOut

router = APIRouter(prefix="/sites", tags=["Sites"])


def _site_to_out(site: Site) -> SiteOut:
    geom_dict = mapping(to_shape(site.geometry))
    return SiteOut(
        id=site.id,
        name=site.name,
        project_id=site.project_id,
        site_type=site.site_type,
        geometry=geom_dict,
        created_at=site.created_at,
    )


@router.get("", response_model=list[SiteOut])
def list_sites(
    project_id: str | None = Query(default=None, alias="project_id"),
    db: Session = Depends(get_db),
):
    query = db.query(Site)
    if project_id:
        query = query.filter(Site.project_id == project_id)
    sites = query.order_by(Site.created_at.desc()).all()
    return [_site_to_out(s) for s in sites]


@router.post("", response_model=SiteOut, status_code=status.HTTP_201_CREATED)
def create_site(
    payload: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify that project exists
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{payload.project_id}' not found",
        )

    # Validate and convert geometry
    try:
        geom_dict = (
            payload.geometry
            if isinstance(payload.geometry, dict)
            else payload.geometry.model_dump()
        )
        s_geom = shape(geom_dict)
        if s_geom.geom_type != "Polygon":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Geometry must be a Polygon, got {s_geom.geom_type}",
            )
        wkb_geom = from_shape(s_geom, srid=4326)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid GeoJSON geometry: {e}",
        )

    site = Site(
        name=payload.name,
        project_id=payload.project_id,
        site_type=payload.site_type,
        geometry=wkb_geom,
    )
    db.add(site)
    db.commit()
    db.refresh(site)

    return _site_to_out(site)


@router.get("/{id}", response_model=SiteOut)
def get_site(id: str, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Site '{id}' not found",
        )
    return _site_to_out(site)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site = db.query(Site).filter(Site.id == id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Site '{id}' not found",
        )
    db.delete(site)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
