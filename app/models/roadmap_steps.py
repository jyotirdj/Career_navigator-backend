from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class StepStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class RoadmapStep(Base):
    __tablename__ = "roadmap_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("roadmap_templates.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)  # Order within the template
    estimated_duration = Column(String, nullable=True)  # e.g., "2 weeks", "1 month"
    resources = Column(Text, nullable=True)  # JSON string or text with links
    
    # Relationships
    template = relationship("RoadmapTemplate", back_populates="steps")
    user_steps = relationship("UserRoadmapStep", back_populates="step")


class UserRoadmap(Base):
    __tablename__ = "user_roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("roadmap_templates.id"), nullable=False)
    created_at = Column(String, nullable=False)  # ISO format string
    
    # Relationships
    user = relationship("User", back_populates="roadmaps")
    template = relationship("RoadmapTemplate")
    steps = relationship("UserRoadmapStep", back_populates="roadmap", cascade="all, delete-orphan")


class UserRoadmapStep(Base):
    __tablename__ = "user_roadmap_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("user_roadmaps.id"), nullable=False)
    step_id = Column(Integer, ForeignKey("roadmap_steps.id"), nullable=False)
    status = Column(Enum(StepStatus), default=StepStatus.NOT_STARTED, nullable=False)
    notes = Column(Text, nullable=True)
    completed_at = Column(String, nullable=True)  # ISO format string
    
    # Relationships
    roadmap = relationship("UserRoadmap", back_populates="steps")
    step = relationship("RoadmapStep", back_populates="user_steps")




