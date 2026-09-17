from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.project import Project
from app.models.site import Site
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    results = (
        db.query(Project, func.count(Site.id).label("site_count"))
        .outerjoin(Site, Project.id == Site.project_id)
        .group_by(Project.id)
        .order_by(Project.created_at.desc())
        .all()
    )
    return [
        ProjectOut(
            id=p.id,
            name=p.name,
            type=p.type,
            status=p.status,
            description=p.description,
            site_count=site_count,
            last_updated=p.updated_at,
        )
        for p, site_count in results
    ]


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = Project(
        name=payload.name,
        type=payload.type,
        status=payload.status,
        description=payload.description,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectOut(
        id=project.id,
        name=project.name,
        type=project.type,
        status=project.status,
        description=project.description,
        site_count=0,
        last_updated=project.updated_at,
    )


@router.get("/{id}", response_model=ProjectOut)
def get_project(id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{id}' not found",
        )
    site_count = (
        db.query(func.count(Site.id)).filter(Site.project_id == id).scalar() or 0
    )
    return ProjectOut(
        id=project.id,
        name=project.name,
        type=project.type,
        status=project.status,
        description=project.description,
        site_count=site_count,
        last_updated=project.updated_at,
    )


@router.patch("/{id}", response_model=ProjectOut)
def update_project(
    id: str,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{id}' not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    site_count = (
        db.query(func.count(Site.id)).filter(Site.project_id == id).scalar() or 0
    )
    return ProjectOut(
        id=project.id,
        name=project.name,
        type=project.type,
        status=project.status,
        description=project.description,
        site_count=site_count,
        last_updated=project.updated_at,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{id}' not found",
        )
    db.delete(project)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
