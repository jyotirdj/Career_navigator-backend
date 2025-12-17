from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.student_profile import StudentProfile
from app.schemas.profile import StudentProfileCreate, StudentProfileUpdate, StudentProfileResponse
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=StudentProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's student profile."""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create your profile first."
        )
    
    return profile


@router.post("", response_model=StudentProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: StudentProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new student profile."""
    # Check if profile already exists
    existing_profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == current_user.id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists. Use PUT to update."
        )
    
    # Validate year and semester
    if profile_data.current_year < 1 or profile_data.current_year > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current year must be between 1 and 4"
        )
    
    if profile_data.current_semester < 1 or profile_data.current_semester > 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current semester must be 1 or 2"
        )
    
    new_profile = StudentProfile(
        user_id=current_user.id,
        **profile_data.model_dump()
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    return new_profile


@router.put("", response_model=StudentProfileResponse)
def update_profile(
    profile_data: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update student profile."""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create your profile first."
        )
    
    # Update only provided fields
    update_data = profile_data.model_dump(exclude_unset=True)
    
    # Validate year and semester if provided
    if "current_year" in update_data:
        if update_data["current_year"] < 1 or update_data["current_year"] > 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current year must be between 1 and 4"
            )
    
    if "current_semester" in update_data:
        if update_data["current_semester"] < 1 or update_data["current_semester"] > 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current semester must be 1 or 2"
            )
    
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    return profile




