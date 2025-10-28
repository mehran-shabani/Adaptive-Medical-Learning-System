"""
SQLAlchemy models for content management.
"""

import enum

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.config import settings
from app.db import Base
from app.utils.timestamps import utcnow


class IngestionStatus(str, enum.Enum):
    """Enum for ingestion job status."""

    QUEUED = "queued"  # Job queued for processing
    RUNNING = "running"  # Job is currently running
    DONE = "done"  # Job completed successfully
    ERROR = "error"  # Job failed with error


class Topic(Base):
    """
    Topic model representing medical subjects and sub-topics.

    Follows a hierarchical structure (e.g., System -> Organ -> Disease)

    Attributes:
        id: Primary key
        parent_id: Foreign key to parent topic (for hierarchy)
        name: Topic name (e.g., "Diabetic Ketoacidosis")
        system_name: Body system (e.g., "Endocrine", "Cardiovascular")
        source_reference: Reference to source material
        description: Topic description
        created_at: Topic creation timestamp
    """

    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("topics.id"), nullable=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    system_name = Column(String(100), nullable=True, index=True)
    source_reference = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    # Relationships
    parent = relationship("Topic", remote_side=[id], backref="subtopics")
    chunks = relationship("Chunk", back_populates="topic", cascade="all, delete-orphan")
    quiz_questions = relationship("QuizQuestion", back_populates="topic")
    masteries = relationship("Mastery", back_populates="topic")

    def __repr__(self):
        return f"<Topic(id={self.id}, name={self.name}, system={self.system_name})>"


class Chunk(Base):
    """
    Chunk model representing text segments from source material.

    Text is split into chunks for embedding and retrieval.
    Each chunk is associated with a topic and has a vector embedding.

    Attributes:
        id: Primary key
        topic_id: Foreign key to topic
        page_start: Starting page number in source document
        page_end: Ending page number in source document
        text: Chunk text content
        embedding_vector: Vector embedding of text (1536 dimensions)
        source_pdf_path: Path to source PDF file
        metadata: Additional metadata (JSON)
        created_at: Chunk creation timestamp
    """

    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)
    page_start = Column(Integer, nullable=True)
    page_end = Column(Integer, nullable=True)
    text = Column(Text, nullable=False)
    embedding_vector = Column(Vector(settings.VECTOR_DIMENSION), nullable=True)
    source_pdf_path = Column(String(500), nullable=True)
    metadata = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=utcnow, nullable=False)

    # Relationships
    topic = relationship("Topic", back_populates="chunks")

    def __repr__(self):
        return f"<Chunk(id={self.id}, topic_id={self.topic_id}, pages={self.page_start}-{self.page_end})>"


class IngestionJob(Base):
    """
    Ingestion job model for tracking PDF processing jobs.

    Tracks the status of background PDF ingestion tasks.
    This is critical for providing user feedback on long-running operations.

    Attributes:
        id: Primary key
        job_id: Unique job identifier (string)
        user_id: Foreign key to user who initiated the job
        topic_id: Foreign key to target topic
        status: Current job status (queued/running/done/error)
        pdf_filename: Original PDF filename
        chunk_count: Number of chunks created (null until done)
        error_message: Error details if status is 'error'
        created_at: Job creation timestamp
        finished_at: Job completion timestamp

    Notes:
        - Job tracking is essential for UX with large PDF files
        - Status transitions: queued -> running -> done/error
        - Frontend polls GET /content/ingestion-status/{job_id} for updates
    """

    __tablename__ = "ingestion_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)

    status = Column(Enum(IngestionStatus), default=IngestionStatus.QUEUED, nullable=False, index=True)

    pdf_filename = Column(String(500), nullable=True)
    chunk_count = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=utcnow, nullable=False)
    finished_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<IngestionJob(job_id={self.job_id}, status={self.status}, chunks={self.chunk_count})>"
