from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from datetime import datetime
from app.models import RoadmapTemplate, UserRoadmap, UserRoadmapStep, RoadmapStep
from app.models.student_profile import StudentProfile
from app.models.roadmap_steps import StepStatus


def find_matching_template(
    db: Session,
    branch,
    career_goal,
    current_year: int
) -> Optional[RoadmapTemplate]:
    """Find the best matching roadmap template for a student profile."""
    # First, try to find exact match (branch + career_goal + year range)
    template = db.query(RoadmapTemplate).filter(
        RoadmapTemplate.branch == branch,
        RoadmapTemplate.career_goal == career_goal,
        RoadmapTemplate.is_active == True,
        (RoadmapTemplate.start_year.is_(None) | (RoadmapTemplate.start_year <= current_year)),
        (RoadmapTemplate.end_year.is_(None) | (RoadmapTemplate.end_year >= current_year))
    ).first()
    
    if template:
        return template
    
    # Fallback: match by career_goal only (branch-agnostic)
    template = db.query(RoadmapTemplate).filter(
        RoadmapTemplate.branch.is_(None),
        RoadmapTemplate.career_goal == career_goal,
        RoadmapTemplate.is_active == True,
        (RoadmapTemplate.start_year.is_(None) | (RoadmapTemplate.start_year <= current_year)),
        (RoadmapTemplate.end_year.is_(None) | (RoadmapTemplate.end_year >= current_year))
    ).first()
    
    return template


def generate_roadmap_for_user(
    db: Session,
    user_id: int,
    profile: StudentProfile
) -> Optional[UserRoadmap]:
    """Generate a personalized roadmap for a user based on their profile."""
    # Check if user already has a roadmap
    existing_roadmap = db.query(UserRoadmap).filter(
        UserRoadmap.user_id == user_id
    ).first()
    
    if existing_roadmap:
        return existing_roadmap
    
    # Find matching template
    template = find_matching_template(
        db=db,
        branch=profile.branch,
        career_goal=profile.career_goal,
        current_year=profile.current_year
    )
    
    if not template:
        return None
    
    # Create user roadmap
    roadmap = UserRoadmap(
        user_id=user_id,
        template_id=template.id,
        created_at=datetime.utcnow().isoformat()
    )
    db.add(roadmap)
    db.flush()
    
    # Create user roadmap steps from template steps
    template_steps = db.query(RoadmapStep).filter(
        RoadmapStep.template_id == template.id
    ).order_by(RoadmapStep.order).all()
    
    for step in template_steps:
        user_step = UserRoadmapStep(
            roadmap_id=roadmap.id,
            step_id=step.id,
            status=StepStatus.NOT_STARTED
        )
        db.add(user_step)
    
    db.commit()
    db.refresh(roadmap)
    return roadmap


def get_roadmap_with_progress(
    db: Session,
    user_id: int
) -> Optional[dict]:
    """Get user's roadmap with progress and completion percentage."""
    roadmap = db.query(UserRoadmap).filter(
        UserRoadmap.user_id == user_id
    ).first()
    
    if not roadmap:
        return None
    
    # Load steps with their related step data
    steps = db.query(UserRoadmapStep).options(
        joinedload(UserRoadmapStep.step)
    ).join(RoadmapStep).filter(
        UserRoadmapStep.roadmap_id == roadmap.id
    ).order_by(RoadmapStep.order).all()
    
    # Compute statistics
    total_steps = len(steps)
    completed_steps = sum(1 for step in steps if step.status == StepStatus.COMPLETED)
    in_progress_steps = sum(1 for step in steps if step.status == StepStatus.IN_PROGRESS)
    not_started_steps = sum(1 for step in steps if step.status == StepStatus.NOT_STARTED)
    
    # Calculate completion percentage: completed_steps / total_steps * 100
    completion_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0.0
    
    # Find current step: first in_progress, else first not_started
    current_step = None
    in_progress_step = next((step for step in steps if step.status == StepStatus.IN_PROGRESS), None)
    if in_progress_step:
        current_step = {
            "step_id": in_progress_step.step_id,
            "title": in_progress_step.step.title,
            "order": in_progress_step.step.order
        }
    else:
        not_started_step = next((step for step in steps if step.status == StepStatus.NOT_STARTED), None)
        if not_started_step:
            current_step = {
                "step_id": not_started_step.step_id,
                "title": not_started_step.step.title,
                "order": not_started_step.step.order
            }
    
    return {
        "id": roadmap.id,
        "template_id": roadmap.template_id,
        "created_at": roadmap.created_at,
        "steps": steps,
        "total_steps": total_steps,
        "completed_steps": completed_steps,
        "in_progress_steps": in_progress_steps,
        "not_started_steps": not_started_steps,
        "completion_percentage": round(completion_percentage, 2),
        "current_step": current_step
    }


def update_step_status(
    db: Session,
    user_id: int,
    step_id: int,
    status: StepStatus,
    notes: Optional[str] = None
) -> Optional[UserRoadmapStep]:
    """Update the status of a roadmap step for a user."""
    # Verify the step belongs to the user's roadmap
    user_step = db.query(UserRoadmapStep).options(
        joinedload(UserRoadmapStep.step)
    ).join(UserRoadmap).filter(
        UserRoadmap.user_id == user_id,
        UserRoadmapStep.step_id == step_id
    ).first()
    
    if not user_step:
        return None
    
    # Get the roadmap to access all steps
    roadmap = user_step.roadmap
    
    # If marking as in_progress, ensure only one step is in_progress at a time
    if status == StepStatus.IN_PROGRESS:
        # Set all other in_progress steps to not_started (unless they're completed)
        other_in_progress_steps = db.query(UserRoadmapStep).join(UserRoadmap).filter(
            UserRoadmap.user_id == user_id,
            UserRoadmapStep.roadmap_id == roadmap.id,
            UserRoadmapStep.step_id != step_id,
            UserRoadmapStep.status == StepStatus.IN_PROGRESS
        ).all()
        
        for other_step in other_in_progress_steps:
            other_step.status = StepStatus.NOT_STARTED
    
    # If marking as completed, handle auto-advancement
    if status == StepStatus.COMPLETED:
        # 1. Set completed_at timestamp if not already set
        if not user_step.completed_at:
            user_step.completed_at = datetime.utcnow().isoformat()
        
        # 2. Ensure only one step is in_progress: clear all other in_progress steps
        other_in_progress_steps = db.query(UserRoadmapStep).join(UserRoadmap).filter(
            UserRoadmap.user_id == user_id,
            UserRoadmapStep.roadmap_id == roadmap.id,
            UserRoadmapStep.step_id != step_id,
            UserRoadmapStep.status == StepStatus.IN_PROGRESS
        ).all()
        
        for other_step in other_in_progress_steps:
            other_step.status = StepStatus.NOT_STARTED
        
        # 3. Automatically move the next step (order + 1) to "in_progress"
        current_step_order = user_step.step.order
        next_step = db.query(UserRoadmapStep).options(
            joinedload(UserRoadmapStep.step)
        ).join(RoadmapStep).join(UserRoadmap).filter(
            UserRoadmap.user_id == user_id,
            UserRoadmapStep.roadmap_id == roadmap.id,
            RoadmapStep.order == current_step_order + 1,
            UserRoadmapStep.status != StepStatus.COMPLETED  # Don't change already completed steps
        ).first()
        
        if next_step:
            next_step.status = StepStatus.IN_PROGRESS
    
    elif status != StepStatus.COMPLETED:
        # If changing from completed to something else, clear completed_at
        user_step.completed_at = None
    
    # Update the step status
    user_step.status = status
    if notes is not None:
        user_step.notes = notes
    
    db.commit()
    db.refresh(user_step)
    return user_step

