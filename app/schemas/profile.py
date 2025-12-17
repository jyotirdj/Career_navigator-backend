from pydantic import BaseModel
from typing import Optional
from app.models.student_profile import Branch, CareerGoal


class StudentProfileBase(BaseModel):
    branch: Branch
    current_year: int
    current_semester: int
    career_goal: CareerGoal
    current_skills: Optional[str] = None


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(BaseModel):
    branch: Optional[Branch] = None
    current_year: Optional[int] = None
    current_semester: Optional[int] = None
    career_goal: Optional[CareerGoal] = None
    current_skills: Optional[str] = None


class StudentProfileResponse(StudentProfileBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True




