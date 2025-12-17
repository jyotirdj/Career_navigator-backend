"""
Script to seed initial roadmap templates and steps.
Run this after setting up the database to populate some sample roadmaps.
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.roadmap_templates import RoadmapTemplate
from app.models.roadmap_steps import RoadmapStep
from app.models.student_profile import Branch, CareerGoal


def seed_roadmaps():
    """Seed initial roadmap templates."""
    db: Session = SessionLocal()
    
    try:
        # Example: Python Backend Developer roadmap for CSE students (Year 1-4)
        python_backend_template = RoadmapTemplate(
            name="Python Backend Developer - CSE",
            description="Complete roadmap for becoming a Python Backend Developer (CSE students)",
            branch=Branch.CSE,
            career_goal=CareerGoal.PYTHON_BACKEND_DEVELOPER,
            start_year=1,
            end_year=4,
            is_active=True
        )
        db.add(python_backend_template)
        db.flush()
        
        # Steps for Python Backend Developer
        steps = [
            {"title": "Learn Python Basics", "description": "Master Python fundamentals: variables, data types, control flow, functions", "order": 1, "estimated_duration": "2 weeks"},
            {"title": "Learn Object-Oriented Programming", "description": "Understand classes, inheritance, polymorphism in Python", "order": 2, "estimated_duration": "2 weeks"},
            {"title": "Learn Git and Version Control", "description": "Master Git commands, branching, merging, and GitHub workflows", "order": 3, "estimated_duration": "1 week"},
            {"title": "Learn SQL and Database Basics", "description": "Understand relational databases, SQL queries, and database design", "order": 4, "estimated_duration": "3 weeks"},
            {"title": "Learn FastAPI Framework", "description": "Build REST APIs with FastAPI, understand routing, middleware, and dependency injection", "order": 5, "estimated_duration": "4 weeks"},
            {"title": "Learn Database ORMs (SQLAlchemy)", "description": "Master SQLAlchemy for database operations and migrations", "order": 6, "estimated_duration": "2 weeks"},
            {"title": "Learn Authentication & Authorization", "description": "Implement JWT authentication, password hashing, and role-based access", "order": 7, "estimated_duration": "2 weeks"},
            {"title": "Learn Testing (pytest)", "description": "Write unit tests, integration tests, and test APIs", "order": 8, "estimated_duration": "2 weeks"},
            {"title": "Learn Docker and Containerization", "description": "Containerize applications, understand Docker Compose", "order": 9, "estimated_duration": "2 weeks"},
            {"title": "Learn CI/CD Basics", "description": "Set up GitHub Actions, automated testing and deployment", "order": 10, "estimated_duration": "2 weeks"},
        ]
        
        for step_data in steps:
            step = RoadmapStep(
                template_id=python_backend_template.id,
                **step_data
            )
            db.add(step)
        
        # Example: Generic Python Backend Developer roadmap (all branches)
        python_backend_generic = RoadmapTemplate(
            name="Python Backend Developer - Generic",
            description="Python Backend Developer roadmap for all engineering branches",
            branch=None,  # Applies to all branches
            career_goal=CareerGoal.PYTHON_BACKEND_DEVELOPER,
            start_year=1,
            end_year=4,
            is_active=True
        )
        db.add(python_backend_generic)
        db.flush()
        
        # Add same steps for generic template
        for step_data in steps:
            step = RoadmapStep(
                template_id=python_backend_generic.id,
                **step_data
            )
            db.add(step)
        
        # Example: Data Engineer roadmap
        data_engineer_template = RoadmapTemplate(
            name="Data Engineer - Generic",
            description="Complete roadmap for becoming a Data Engineer",
            branch=None,
            career_goal=CareerGoal.DATA_ENGINEER,
            start_year=1,
            end_year=4,
            is_active=True
        )
        db.add(data_engineer_template)
        db.flush()
        
        data_engineer_steps = [
            {"title": "Learn Python Basics", "description": "Master Python fundamentals", "order": 1, "estimated_duration": "2 weeks"},
            {"title": "Learn SQL and Database Design", "description": "Advanced SQL, database optimization, indexing", "order": 2, "estimated_duration": "4 weeks"},
            {"title": "Learn Data Structures and Algorithms", "description": "Essential algorithms and data structures for data processing", "order": 3, "estimated_duration": "6 weeks"},
            {"title": "Learn Pandas and NumPy", "description": "Data manipulation and analysis with Python libraries", "order": 4, "estimated_duration": "3 weeks"},
            {"title": "Learn Apache Spark", "description": "Big data processing with Spark", "order": 5, "estimated_duration": "4 weeks"},
            {"title": "Learn Data Pipeline Design", "description": "ETL/ELT processes, data warehousing concepts", "order": 6, "estimated_duration": "3 weeks"},
            {"title": "Learn Cloud Platforms (AWS/GCP)", "description": "Data services on cloud platforms", "order": 7, "estimated_duration": "4 weeks"},
        ]
        
        for step_data in data_engineer_steps:
            step = RoadmapStep(
                template_id=data_engineer_template.id,
                **step_data
            )
            db.add(step)
        
        db.commit()
        print("✅ Successfully seeded roadmap templates and steps!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding roadmaps: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_roadmaps()




