from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/profiles", tags=["Profiles"])


@router.post("/", response_model=schemas.ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile_in: schemas.ProfileCreate, db: Session = Depends(get_db)):
    
    existing_profile = db.query(models.Profile).filter(models.Profile.email == profile_in.email).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um perfil cadastrado com este e-mail."
        )

    profile = models.Profile(
        name=profile_in.name,
        bio=profile_in.bio,
        email=profile_in.email
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/{profile_id}", response_model=schemas.ProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil não encontrado."
        )
    return profile