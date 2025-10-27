"""
Pydantic schemas for content management endpoints.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class TopicCreate(BaseModel):
    """Schema for creating a new topic."""
    name: str = Field(..., min_length=1, max_length=200)
    system_name: Optional[str] = Field(None, max_length=100)
    parent_id: Optional[int] = None
    source_reference: Optional[str] = None
    description: Optional[str] = None


class TopicResponse(BaseModel):
    """Schema for topic response."""
    id: int
    name: str
    system_name: Optional[str]
    parent_id: Optional[int]
    source_reference: Optional[str]
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChunkResponse(BaseModel):
    """Schema for chunk response."""
    id: int
    topic_id: int
    page_start: Optional[int]
    page_end: Optional[int]
    text: str
    source_pdf_path: Optional[str]
    
    class Config:
        from_attributes = True


class PDFUploadResponse(BaseModel):
    """Schema for PDF upload response."""
    job_id: str = Field(..., description="Unique job ID for tracking ingestion")
    message: str
    filename: str
    topic_id: int


class TopicSummaryRequest(BaseModel):
    """Schema for requesting topic summary."""
    include_high_yield: bool = Field(True, description="Include high-yield traps and tips")
    max_length: int = Field(500, description="Maximum summary length in words")


class HighYieldTrap(BaseModel):
    """Schema for a high-yield trap or tip."""
    title: str
    description: str
    clinical_pearl: str


class TopicSummaryResponse(BaseModel):
    """Schema for topic summary response."""
    topic_id: int
    topic_name: str
    summary: str
    key_points: List[str]
    high_yield_traps: List[HighYieldTrap]
    chunk_count: int
    source_references: List[str]


class ContentSearchRequest(BaseModel):
    """Schema for semantic content search."""
    query: str = Field(..., min_length=1, description="Search query")
    topic_id: Optional[int] = Field(None, description="Filter by topic")
    limit: int = Field(5, ge=1, le=20, description="Number of results")


class ContentSearchResult(BaseModel):
    """Schema for single search result."""
    chunk_id: int
    topic_id: int
    topic_name: str
    text: str
    similarity_score: float
    page_reference: Optional[str]


class ContentSearchResponse(BaseModel):
    """Schema for search results."""
    query: str
    results: List[ContentSearchResult]
    total_results: int
