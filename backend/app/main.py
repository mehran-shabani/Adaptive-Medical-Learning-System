"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.config import settings
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.content.router import router as content_router
from app.quiz.router import router as quiz_router
from app.mastery.router import router as mastery_router
from app.recommender.router import router as recommender_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="An intelligent, personalized learning platform for medical students",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:*",
        "http://127.0.0.1:*",
        "http://10.0.2.2:*",  # Android emulator
        "http://192.168.*.*:*",  # Local network
        "*"  # Allow all for development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add X-Process-Time header to all responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint.
    
    Public endpoint - no authentication required.
    
    Returns:
        dict: Application health status
        
    Response:
        {
            "status": "ok",
            "version": "0.1.0"
        }
    """
    return {
        "status": "ok",
        "version": "0.1.0"
    }


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint.
    
    Public endpoint - no authentication required.
    
    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "Welcome to Adaptive Medical Learning System API",
        "docs": "/docs",
        "health": "/health",
        "version": "0.1.0",
        "note": "Version 0.1.0 is currently in development"
    }


# Include routers
app.include_router(
    auth_router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Authentication"]
)

app.include_router(
    users_router,
    prefix=f"{settings.API_V1_PREFIX}/users",
    tags=["Users"]
)

app.include_router(
    content_router,
    prefix=f"{settings.API_V1_PREFIX}/content",
    tags=["Content"]
)

app.include_router(
    quiz_router,
    prefix=f"{settings.API_V1_PREFIX}/quiz",
    tags=["Quiz"]
)

app.include_router(
    mastery_router,
    prefix=f"{settings.API_V1_PREFIX}/mastery",
    tags=["Mastery"]
)

app.include_router(
    recommender_router,
    prefix=f"{settings.API_V1_PREFIX}/recommender",
    tags=["Recommender"]
)


@app.on_event("startup")
async def startup_event():
    """Execute on application startup."""
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Create upload directory if it doesn't exist
    import os
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    logger.info(f"Upload directory: {settings.UPLOAD_DIR}")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown."""
    logger.info(f"Shutting down {settings.APP_NAME}")
