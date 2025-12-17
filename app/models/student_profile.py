from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class Branch(str, enum.Enum):
    CSE = "CSE"
    MECHANICAL = "Mechanical"
    ECE = "ECE"
    EEE = "EEE"
    CIVIL = "Civil"
    CHEMICAL = "Chemical"
    AEROSPACE = "Aerospace"
    BIOMEDICAL = "Biomedical"


class CareerGoal(str, enum.Enum):
    PYTHON_BACKEND_DEVELOPER = "Python Backend Developer"
    DATA_ENGINEER = "Data Engineer"
    DEVOPS_ENGINEER = "DevOps Engineer"
    CLOUD_ENGINEER = "Cloud Engineer"
    FRONTEND_DEVELOPER = "Frontend Developer"
    FULL_STACK_DEVELOPER = "Full Stack Developer"
    MACHINE_LEARNING_ENGINEER = "Machine Learning Engineer"
    MOBILE_DEVELOPER = "Mobile Developer"


class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    branch = Column(Enum(Branch), nullable=False)
    current_year = Column(Integer, nullable=False)  # 1, 2, 3, or 4
    current_semester = Column(Integer, nullable=False)  # 1 or 2
    career_goal = Column(Enum(CareerGoal), nullable=False)
    current_skills = Column(String, nullable=True)  # JSON string or comma-separated
    
    # Relationships
    user = relationship("User", back_populates="profile")




