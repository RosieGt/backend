from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/technologies", tags=["Technologies"])


@router.post("/", response_model=schemas.TechnologyResponse, status_code=status.HTTP_201_CREATED)
def create_technology(tech_in: schemas.TechnologyCreate, db: Session = Depends(get_db)):
    # Validação de unicidade do nome da tecnologia
    existing_tech = db.query(models.Technology).filter(models.Technology.name.ilike(tech_in.name)).first()
    if existing_tech:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tecnologia já cadastrada."
        )

    tech = models.Technology(name=tech_in.name)
    db.add(tech)
    db.commit()
    db.refresh(tech)
    return tech


@router.get("/", response_model=List[schemas.TechnologyResponse])
def list_technologies(db: Session = Depends(get_db)):
    return db.query(models.Technology).all()