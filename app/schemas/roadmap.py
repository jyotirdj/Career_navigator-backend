from pydantic import BaseModel
from typing import List, Optional
from app.models.roadmap_steps import StepStatus


class RoadmapStepBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int
    estimated_duration: Optional[str] = None
    resources: Optional[str] = None


class RoadmapStepResponse(RoadmapStepBase):
    id: int
    template_id: int
    
    class Config:
        from_attributes = True


class UserRoadmapStepResponse(BaseModel):
    id: int
    step_id: int
    status: StepStatus
    notes: Optional[str] = None
    completed_at: Optional[str] = None
    step: RoadmapStepResponse
    
    class Config:
        from_attributes = True


class CurrentStepResponse(BaseModel):
    """Response model for current step information."""
    step_id: int
    title: str
    order: int
    
    class Config:
        from_attributes = True


class RoadmapResponse(BaseModel):
    id: int
    template_id: int
    created_at: str
    steps: List[UserRoadmapStepResponse]
    # Computed fields
    total_steps: int
    completed_steps: int
    in_progress_steps: int
    not_started_steps: int
    completion_percentage: float  # completed_steps / total_steps * 100
    current_step: Optional[CurrentStepResponse] = None
    
    class Config:
        from_attributes = True


class StepStatusUpdate(BaseModel):
    status: StepStatus
    notes: Optional[str] = None




