"""
Pydantic schemas for content management endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class TopicCreate(BaseModel):
    """Schema for creating a new topic."""

    name: str = Field(..., min_length=1, max_length=200)
    system_name: str | None = Field(None, max_length=100)
    parent_id: int | None = None
    source_reference: str | None = None
    description: str | None = None


class TopicResponse(BaseModel):
    """Schema for topic response."""

    id: int
    name: str
    system_name: str | None
    parent_id: int | None
    source_reference: str | None
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ChunkResponse(BaseModel):
    """Schema for chunk response."""

    id: int
    topic_id: int
    page_start: int | None
    page_end: int | None
    text: str
    source_pdf_path: str | None

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


class CitationInfo(BaseModel):
    """
    Schema for citation information.

    Links summary/content back to specific source chunks for traceability.
    """

    source_reference: str = Field(..., description="Source reference (e.g., 'Harrison 21e p.304-305')")
    chunk_id: int = Field(..., description="Database chunk ID")


class TopicSummaryResponse(BaseModel):
    """
    Schema for topic summary response with citations.

    Includes citations array to trace content back to source chunks
    for transparency and copyright compliance.
    """

    topic_id: int
    topic_name: str
    summary: str
    key_points: list[str]
    high_yield_traps: list[HighYieldTrap]
    chunk_count: int
    source_references: list[str]  # Deprecated: use citations instead
    citations: list[CitationInfo] = Field(default_factory=list, description="Citations linking to source chunks")


class ContentSearchRequest(BaseModel):
    """Schema for semantic content search."""

    query: str = Field(..., min_length=1, description="Search query")
    topic_id: int | None = Field(None, description="Filter by topic")
    limit: int = Field(5, ge=1, le=20, description="Number of results")


class ContentSearchResult(BaseModel):
    """Schema for single search result."""

    chunk_id: int
    topic_id: int
    topic_name: str
    text: str
    similarity_score: float
    page_reference: str | None


class ContentSearchResponse(BaseModel):
    """Schema for search results."""

    query: str
    results: list[ContentSearchResult]
    total_results: int
