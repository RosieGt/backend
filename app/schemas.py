from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, Field

# --- Technology ---
class TechnologyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class TechnologyCreate(TechnologyBase):
    pass

class TechnologyResponse(TechnologyBase):
    id: int

    class Config:
        from_attributes = True

# --- Feedback ---
class FeedbackCreateInProject(BaseModel):
    author_name: str = Field(..., min_length=2, max_length=100)
    comment: str = Field(..., min_length=3)
    rating: int = Field(..., ge=1, le=5)  # Nota obrigatória de 1 a 5

class FeedbackResponse(BaseModel):
    id: int
    author_name: str
    comment: str
    rating: int
    project_id: int

    class Config:
        from_attributes = True

# --- Project ---
class ProjectBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: str = Field(..., min_length=5)
    repository_url: Optional[HttpUrl] = None
    live_url: Optional[HttpUrl] = None

class ProjectCreate(ProjectBase):
    profile_id: int

    technology_ids: Optional[List[int]] = []

class ProjectResponse(ProjectBase):
    id: int
    profile_id: int
    upvotes: int
    average_rating: float
    technologies: List[TechnologyResponse] = []

    class Config:
        from_attributes = True

# DTO para resposta paginada
class PaginatedProjectsResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[ProjectResponse]

# --- Profile ---
class ProfileBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    email: EmailStr

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    projects: List[ProjectResponse] = []

    class Config:
        from_attributes = True