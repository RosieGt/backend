from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.post("/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    
    profile = db.query(models.Profile).filter(models.Profile.id == project_in.profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil informado para o projeto não foi encontrado."
        )

    
    repo_url = str(project_in.repository_url) if project_in.repository_url else None
    live_url = str(project_in.live_url) if project_in.live_url else None

    project = models.Project(
        title=project_in.title,
        description=project_in.description,
        repository_url=repo_url,
        live_url=live_url,
        profile_id=project_in.profile_id
    )

    
    if project_in.technology_ids:
        technologies = (
            db.query(models.Technology)
            .filter(models.Technology.id.in_(project_in.technology_ids))
            .all()
        )
        project.technologies = technologies

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/", response_model=List[schemas.ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()