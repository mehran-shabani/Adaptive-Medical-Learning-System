"""
SQLAlchemy models for content management.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.db import Base
from app.config import settings
from app.utils.timestamps import utcnow


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
