from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.student_profile import Branch, CareerGoal
from app.database import Base


class RoadmapTemplate(Base):
    __tablename__ = "roadmap_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    branch = Column(Enum(Branch), nullable=True)  # None means applies to all branches
    career_goal = Column(Enum(CareerGoal), nullable=False)
    start_year = Column(Integer, nullable=True)  # None means applies to all years
    end_year = Column(Integer, nullable=True)  # None means applies to all years
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    steps = relationship("RoadmapStep", back_populates="template", cascade="all, delete-orphan", order_by="RoadmapStep.order")

