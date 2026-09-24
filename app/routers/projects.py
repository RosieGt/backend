from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.post("/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == project_in.profile_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado.")

    repo_url = str(project_in.repository_url) if project_in.repository_url else None
    live_url = str(project_in.live_url) if project_in.live_url else None

    project = models.Project(
        title=project_in.title,
        description=project_in.description,
        repository_url=repo_url,
        live_url=live_url,
        profile_id=project_in.profile_id,
        upvotes=0,
        average_rating=0.0
    )

    if project_in.technology_ids:
        technologies = db.query(models.Technology).filter(models.Technology.id.in_(project_in.technology_ids)).all()
        project.technologies = technologies

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/", response_model=schemas.PaginatedProjectsResponse)
def list_projects(
    technology: Optional[str] = Query(None, description="Filtrar por nome da tecnologia"),
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Project)

    if technology:
        query = query.join(models.Project.technologies).filter(
            models.Technology.name.ilike(f"%{technology}%")
        )

    total = query.count()
    skip = (page - 1) * limit
    projects = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": projects
    }


@router.put("/{project_id}/upvote", response_model=schemas.ProjectResponse)
def upvote_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado.")

    project.upvotes += 1
    db.commit()
    db.refresh(project)
    return project


@router.post("/{project_id}/feedbacks", response_model=schemas.FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback_for_project(
    project_id: int,
    feedback_in: schemas.FeedbackCreateInProject,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado.")

    
    new_feedback = models.Feedback(
        author_name=feedback_in.author_name,
        comment=feedback_in.comment,
        rating=feedback_in.rating,
        project_id=project_id
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    
    avg_result = db.query(func.avg(models.Feedback.rating)).filter(models.Feedback.project_id == project_id).scalar()
    project.average_rating = round(float(avg_result), 2) if avg_result is not None else 0.0

    db.commit()
    return new_feedback