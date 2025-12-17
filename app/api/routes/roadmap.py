from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.student_profile import StudentProfile
from app.schemas.roadmap import RoadmapResponse, StepStatusUpdate
from app.services.roadmap_service import (
    generate_roadmap_for_user,
    get_roadmap_with_progress,
    update_step_status
)
from app.api.dependencies import get_current_user
from app.models.roadmap_steps import StepStatus

router = APIRouter(prefix="/roadmap", tags=["roadmap"])


@router.get("", response_model=RoadmapResponse)
def get_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's personalized roadmap with progress."""
    roadmap_data = get_roadmap_with_progress(db, current_user.id)
    
    if not roadmap_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found. Please generate a roadmap first."
        )
    
    return roadmap_data


@router.post("/generate", response_model=RoadmapResponse, status_code=status.HTTP_201_CREATED)
def generate_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a new roadmap based on user's profile."""
    # Check if profile exists
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile not found. Please create your profile first."
        )
    
    # Generate roadmap
    roadmap = generate_roadmap_for_user(db, current_user.id, profile)
    
    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No matching roadmap template found for your profile. Please contact admin."
        )
    
    # Get roadmap with progress
    roadmap_data = get_roadmap_with_progress(db, current_user.id)
    return roadmap_data


@router.put("/steps/{step_id}", status_code=status.HTTP_200_OK)
def update_step(
    step_id: int,
    step_update: StepStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the status of a roadmap step."""
    updated_step = update_step_status(
        db=db,
        user_id=current_user.id,
        step_id=step_id,
        status=step_update.status,
        notes=step_update.notes
    )
    
    if not updated_step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Step not found or does not belong to your roadmap"
        )
    
    return {
        "message": "Step updated successfully",
        "step_id": updated_step.step_id,
        "status": updated_step.status
    }




