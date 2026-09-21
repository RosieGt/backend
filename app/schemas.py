from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, Field




class TechnologyBase(BaseModel):
    
    name: str = Field(..., min_length=1, max_length=50, strip_whitespace=True)

class TechnologyCreate(TechnologyBase):
    pass

class TechnologyResponse(TechnologyBase):
    id: int

    class Config:
        from_attributes = True


class FeedbackBase(BaseModel):
    author_name: str = Field(..., min_length=2, max_length=100, strip_whitespace=True)
    comment: str = Field(..., min_length=3, strip_whitespace=True)
    rating: Optional[int] = Field(None, ge=1, le=5)  

class FeedbackCreate(FeedbackBase):
    project_id: int

class FeedbackResponse(FeedbackBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, strip_whitespace=True)
    description: str = Field(..., min_length=5, strip_whitespace=True)
    repository_url: Optional[HttpUrl] = None
    live_url: Optional[HttpUrl] = None

class ProjectCreate(ProjectBase):
    profile_id: int
    
    technology_ids: Optional[List[int]] = []

class ProjectResponse(ProjectBase):
    id: int
    profile_id: int
    technologies: List[TechnologyResponse] = []

    class Config:
        from_attributes = True




class ProfileBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, strip_whitespace=True)
    bio: Optional[str] = Field(None, max_length=500)
    email: EmailStr

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    projects: List[ProjectResponse] = []

    class Config:
        from_attributes = True