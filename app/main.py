from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, profile, roadmap
from app.database import engine, Base
from app.core.config import settings

# Create database tables (in production, use Alembic migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Career Navigator API",
    description="Backend API for engineering students to plan their learning journey",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(roadmap.router, prefix="/api")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Career Navigator API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}




