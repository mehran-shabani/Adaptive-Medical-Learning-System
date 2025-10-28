"""
Content service layer for business logic.
"""

import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.content.embedding import EmbeddingService
from app.content.llm_client import LLMClient
from app.content.models import Chunk, Topic
from app.content.schemas import (
    CitationInfo,
    ContentSearchRequest,
    ContentSearchResponse,
    HighYieldTrap,
    TopicCreate,
    TopicSummaryResponse,
)
from app.utils.timestamps import utcnow

logger = logging.getLogger(__name__)


class ContentService:
    """Service class for content operations."""

    @staticmethod
    def create_topic(topic_data: TopicCreate, db: Session) -> Topic:
        """
        Create a new topic.

        Args:
            topic_data: Topic creation data
            db: Database session

        Returns:
            Topic: Created topic
        """
        topic = Topic(
            name=topic_data.name,
            system_name=topic_data.system_name,
            parent_id=topic_data.parent_id,
            source_reference=topic_data.source_reference,
            description=topic_data.description,
            created_at=utcnow(),
        )

        db.add(topic)
        db.commit()
        db.refresh(topic)

        logger.info(f"Created topic: {topic.id} - {topic.name}")
        return topic

    @staticmethod
    def get_topic_by_id(topic_id: int, db: Session) -> Topic | None:
        """Get topic by ID."""
        return db.query(Topic).filter(Topic.id == topic_id).first()

    @staticmethod
    def list_topics(system_name: str | None = None, parent_id: int | None = None, db: Session = None) -> list[Topic]:
        """
        List topics with optional filters.

        Args:
            system_name: Filter by system name
            parent_id: Filter by parent topic
            db: Database session

        Returns:
            List[Topic]: List of topics
        """
        query = db.query(Topic)

        if system_name:
            query = query.filter(Topic.system_name == system_name)

        if parent_id is not None:
            query = query.filter(Topic.parent_id == parent_id)

        return query.all()

    @staticmethod
    async def get_topic_summary(topic_id: int, include_high_yield: bool, db: Session) -> TopicSummaryResponse:
        """
        Generate summary and high-yield points for a topic.

        Uses LLM to summarize chunks and extract clinical pearls.

        Args:
            topic_id: Topic ID
            include_high_yield: Whether to include high-yield traps
            db: Database session

        Returns:
            TopicSummaryResponse: Topic summary with key points

        Raises:
            HTTPException: If topic not found or no content available
        """
        # Get topic
        topic = ContentService.get_topic_by_id(topic_id, db)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

        # Get chunks for topic
        chunks = db.query(Chunk).filter(Chunk.topic_id == topic_id).all()

        if not chunks:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No content available for this topic")

        logger.info(f"Generating summary for topic {topic_id} with {len(chunks)} chunks")

        # Combine chunk texts
        combined_text = "\n\n".join([chunk.text for chunk in chunks[:10]])  # Limit to first 10 chunks

        # Generate summary using LLM with hallucination prevention
        summary_data = await LLMClient.generate_summary(
            topic_name=topic.name, chunks_text=combined_text, include_high_yield=include_high_yield
        )

        # Extract data from LLM response
        summary = summary_data.get("summary", "")
        key_points = summary_data.get("key_points", [])
        high_yield_data = summary_data.get("high_yield_traps", [])

        high_yield_traps = [HighYieldTrap(**trap) for trap in high_yield_data] if include_high_yield else []

        # Get unique source references (deprecated field)
        source_refs = list({chunk.source_pdf_path for chunk in chunks if chunk.source_pdf_path})

        # Build citations from chunks metadata
        citations = []
        for chunk in chunks[:10]:  # Include citations for first 10 chunks used
            if hasattr(chunk, "metadata") and chunk.metadata:
                # Try to extract source_reference from metadata
                try:
                    import json

                    metadata = json.loads(chunk.metadata) if isinstance(chunk.metadata, str) else chunk.metadata
                    source_ref = metadata.get("source_reference", "Unknown source")
                except:
                    source_ref = chunk.source_pdf_path or "Unknown source"
            else:
                source_ref = chunk.source_pdf_path or "Unknown source"

            # Format page reference
            if chunk.page_start and chunk.page_end:
                source_ref += f" p.{chunk.page_start}"
                if chunk.page_end != chunk.page_start:
                    source_ref += f"-{chunk.page_end}"

            citations.append(CitationInfo(source_reference=source_ref, chunk_id=chunk.id))

        # Remove duplicate citations
        unique_citations = []
        seen = set()
        for citation in citations:
            key = (citation.source_reference, citation.chunk_id)
            if key not in seen:
                seen.add(key)
                unique_citations.append(citation)

        return TopicSummaryResponse(
            topic_id=topic.id,
            topic_name=topic.name,
            summary=summary,
            key_points=key_points,
            high_yield_traps=high_yield_traps,
            chunk_count=len(chunks),
            source_references=source_refs,
            citations=unique_citations,
        )

    @staticmethod
    async def search_content(search_request: ContentSearchRequest, db: Session) -> ContentSearchResponse:
        """
        Search content using semantic similarity.

        Args:
            search_request: Search parameters
            db: Database session

        Returns:
            ContentSearchResponse: Search results with similarity scores
        """
        # Generate embedding for query
        embedding_service = EmbeddingService()
        query_embedding = await embedding_service.create_embedding(search_request.query)

        if not query_embedding:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate query embedding"
            )

        # TODO: Implement vector similarity search using pgvector
        # Example query:
        # SELECT *, embedding_vector <-> query_embedding AS distance
        # FROM chunks
        # WHERE topic_id = ? (optional filter)
        # ORDER BY distance
        # LIMIT ?

        # Placeholder: return empty results
        logger.warning("Vector search not yet implemented")

        return ContentSearchResponse(query=search_request.query, results=[], total_results=0)
