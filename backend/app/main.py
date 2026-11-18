"""
FormPilot AI — Main FastAPI Application.
Tagline: Understand. Fill. Verify. Apply.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .core.config import settings
from .database import init_db
from .api import auth, documents, forms, applications, eligibility, assistant, dashboard, ml

# Initialize database schema on startup
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent AI-powered application assistance platform: Understand, Fill, Verify, Apply.",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(forms.router, prefix=settings.API_V1_STR)
app.include_router(applications.router, prefix=settings.API_V1_STR)
app.include_router(eligibility.router, prefix=settings.API_V1_STR)
app.include_router(assistant.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)
app.include_router(ml.router, prefix=settings.API_V1_STR)

# Static files directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Mount Generated PDFs directory
if os.path.exists(settings.GENERATED_DIR):
    app.mount("/generated", StaticFiles(directory=settings.GENERATED_DIR), name="generated")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "version": settings.VERSION
    }

# Serve root single-page application
@app.get("/")
def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "app": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "docs": "/docs",
        "status": "online"
    }
