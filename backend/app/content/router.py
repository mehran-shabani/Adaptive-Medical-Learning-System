"""
Content management API endpoints.
"""
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import os
import shutil
from typing import Optional, List
import logging

from app.db import get_db
from app.config import settings
from app.content.schemas import (
    TopicCreate, TopicResponse, PDFUploadResponse,
    TopicSummaryResponse, ContentSearchRequest, ContentSearchResponse
)
from app.content.service import ContentService
from app.content.ingestion import PDFIngestionService
from app.utils.security import generate_random_string

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/topics", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic_data: TopicCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new medical topic.
    
    Args:
        topic_data: Topic creation data
        db: Database session
        
    Returns:
        TopicResponse: Created topic
    """
    return ContentService.create_topic(topic_data, db)


@router.get("/topics", response_model=List[TopicResponse])
async def list_topics(
    system_name: Optional[str] = None,
    parent_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    List topics with optional filters.
    
    Args:
        system_name: Filter by body system
        parent_id: Filter by parent topic
        db: Database session
        
    Returns:
        List[TopicResponse]: List of topics
    """
    return ContentService.list_topics(system_name, parent_id, db)


@router.get("/topics/{topic_id}", response_model=TopicResponse)
async def get_topic(
    topic_id: int,
    db: Session = Depends(get_db)
):
    """
    Get topic by ID.
    
    Args:
        topic_id: Topic ID
        db: Database session
        
    Returns:
        TopicResponse: Topic details
    """
    topic = ContentService.get_topic_by_id(topic_id, db)
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    return topic


@router.get("/topics/{topic_id}/summary", response_model=TopicSummaryResponse)
async def get_topic_summary(
    topic_id: int,
    include_high_yield: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get AI-generated summary for a topic.
    
    Generates a summary from all chunks associated with the topic,
    including key points and high-yield clinical pearls.
    
    Args:
        topic_id: Topic ID
        include_high_yield: Include high-yield traps and tips
        db: Database session
        
    Returns:
        TopicSummaryResponse: Topic summary with key insights
    """
    return await ContentService.get_topic_summary(topic_id, include_high_yield, db)


@router.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    topic_id: int = Form(...),
    source_reference: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF file for content ingestion.
    
    The PDF will be processed asynchronously:
    1. Text extraction
    2. Chunking
    3. Embedding generation
    4. Storage in vector database
    
    Args:
        background_tasks: FastAPI background tasks
        file: PDF file to upload
        topic_id: Topic to associate content with
        source_reference: Optional source reference (e.g., "Harrison's 21st Ed")
        db: Database session
        
    Returns:
        PDFUploadResponse: Upload confirmation with job ID
        
    Example:
        curl -X POST "http://localhost:8000/api/v1/content/upload-pdf" \
             -F "file=@harrison_endocrine.pdf" \
             -F "topic_id=5" \
             -F "source_reference=Harrison's Internal Medicine, 21st Edition"
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to start
    
    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024  # Convert to bytes
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB"
        )
    
    # Validate topic exists
    topic = ContentService.get_topic_by_id(topic_id, db)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    # Generate unique job ID
    job_id = generate_random_string(16)
    
    # Save file
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / f"{job_id}_{file.filename}"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Saved uploaded file: {file_path}")
        
        # Add ingestion task to background
        metadata = {
            "source_reference": source_reference,
            "job_id": job_id
        }
        
        # TODO: Use Celery for production
        # For now, use FastAPI background tasks
        async def process_pdf():
            ingestion_service = PDFIngestionService(db)
            try:
                result = await ingestion_service.ingest_pdf(
                    str(file_path),
                    topic_id,
                    metadata
                )
                logger.info(f"Ingestion completed: {result}")
            except Exception as e:
                logger.error(f"Ingestion failed for job {job_id}: {e}")
        
        background_tasks.add_task(process_pdf)
        
        return PDFUploadResponse(
            job_id=job_id,
            message="PDF upload successful. Processing started in background.",
            filename=file.filename,
            topic_id=topic_id
        )
        
    except Exception as e:
        # Clean up file on error
        if file_path.exists():
            file_path.unlink()
        
        logger.error(f"Error uploading PDF: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload PDF"
        )


@router.post("/search", response_model=ContentSearchResponse)
async def search_content(
    search_request: ContentSearchRequest,
    db: Session = Depends(get_db)
):
    """
    Search content using semantic similarity.
    
    Uses vector embeddings to find relevant content chunks.
    
    Args:
        search_request: Search parameters
        db: Database session
        
    Returns:
        ContentSearchResponse: Relevant content chunks with similarity scores
    """
    return await ContentService.search_content(search_request, db)


# Import Path at the top
from pathlib import Path
