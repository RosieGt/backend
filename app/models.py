from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, Float
from sqlalchemy.orm import relationship

from app.database import Base


project_technology = Table(
    "project_technology",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column("technology_id", Integer, ForeignKey("technologies.id", ondelete="CASCADE"), primary_key=True),
)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    email = Column(String(120), unique=True, nullable=False, index=True)

   
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    repository_url = Column(String(255), nullable=True)
    live_url = Column(String(255), nullable=True)
    upvotes = Column(Integer, default=0, nullable=False)
    average_rating = Column(Float, default=0.0, nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)

    
    profile = relationship("Profile", back_populates="projects")
    feedbacks = relationship("Feedback", back_populates="project", cascade="all, delete-orphan")
    technologies = relationship("Technology", secondary=project_technology, back_populates="projects")


class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

   
    projects = relationship("Project", secondary=project_technology, back_populates="technologies")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(100), nullable=False)
    comment = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    
    project = relationship("Project", back_populates="feedbacks")