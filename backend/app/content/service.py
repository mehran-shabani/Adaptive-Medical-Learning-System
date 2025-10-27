"""
Content service layer for business logic.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
import logging
import httpx

from app.content.models import Topic, Chunk
from app.content.schemas import (
    TopicCreate, TopicSummaryResponse, HighYieldTrap,
    ContentSearchRequest, ContentSearchResponse, ContentSearchResult
)
from app.content.embedding import EmbeddingService
from app.config import settings
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
            created_at=utcnow()
        )
        
        db.add(topic)
        db.commit()
        db.refresh(topic)
        
        logger.info(f"Created topic: {topic.id} - {topic.name}")
        return topic
    
    @staticmethod
    def get_topic_by_id(topic_id: int, db: Session) -> Optional[Topic]:
        """Get topic by ID."""
        return db.query(Topic).filter(Topic.id == topic_id).first()
    
    @staticmethod
    def list_topics(
        system_name: Optional[str] = None,
        parent_id: Optional[int] = None,
        db: Session = None
    ) -> List[Topic]:
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
    async def get_topic_summary(
        topic_id: int,
        include_high_yield: bool,
        db: Session
    ) -> TopicSummaryResponse:
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Topic not found"
            )
        
        # Get chunks for topic
        chunks = db.query(Chunk).filter(Chunk.topic_id == topic_id).all()
        
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No content available for this topic"
            )
        
        logger.info(f"Generating summary for topic {topic_id} with {len(chunks)} chunks")
        
        # Combine chunk texts
        combined_text = "\n\n".join([chunk.text for chunk in chunks[:10]])  # Limit to first 10 chunks
        
        # Generate summary using LLM
        summary, key_points, high_yield_traps = await ContentService._generate_summary_with_llm(
            topic_name=topic.name,
            content_text=combined_text,
            include_high_yield=include_high_yield
        )
        
        # Get unique source references
        source_refs = list(set(
            chunk.source_pdf_path for chunk in chunks 
            if chunk.source_pdf_path
        ))
        
        return TopicSummaryResponse(
            topic_id=topic.id,
            topic_name=topic.name,
            summary=summary,
            key_points=key_points,
            high_yield_traps=high_yield_traps,
            chunk_count=len(chunks),
            source_references=source_refs
        )
    
    @staticmethod
    async def _generate_summary_with_llm(
        topic_name: str,
        content_text: str,
        include_high_yield: bool
    ) -> tuple[str, List[str], List[HighYieldTrap]]:
        """
        Generate summary using LLM.
        
        Args:
            topic_name: Name of topic
            content_text: Combined chunk text
            include_high_yield: Include high-yield traps
            
        Returns:
            tuple: (summary, key_points, high_yield_traps)
        """
        # Prepare prompt
        prompt = f"""You are a medical education expert. Summarize the following content about "{topic_name}" for medical students preparing for residency exams.

Content:
{content_text[:4000]}  # Limit to avoid token limits

Please provide:
1. A concise summary (2-3 paragraphs)
2. 5-7 key points
{'3. 3-5 high-yield clinical traps or pearls that students often miss' if include_high_yield else ''}

Format your response as JSON with keys: "summary", "key_points", and "high_yield_traps" (each trap should have "title", "description", "clinical_pearl")."""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.OPENAI_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": settings.LLM_MODEL,
                        "messages": [
                            {"role": "system", "content": "You are a medical education expert."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": settings.LLM_TEMPERATURE,
                        "max_tokens": settings.LLM_MAX_TOKENS
                    },
                    timeout=60.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Parse LLM response
                import json
                llm_content = data["choices"][0]["message"]["content"]
                
                # Try to parse as JSON
                try:
                    parsed = json.loads(llm_content)
                    summary = parsed.get("summary", "")
                    key_points = parsed.get("key_points", [])
                    high_yield_data = parsed.get("high_yield_traps", [])
                    
                    high_yield_traps = [
                        HighYieldTrap(**trap) for trap in high_yield_data
                    ] if include_high_yield else []
                    
                except json.JSONDecodeError:
                    # Fallback: use raw content
                    summary = llm_content
                    key_points = []
                    high_yield_traps = []
                
                return summary, key_points, high_yield_traps
                
        except Exception as e:
            logger.error(f"Error generating summary with LLM: {e}")
            # Return fallback summary
            return (
                f"Summary of {topic_name} based on {len(content_text)} characters of content.",
                ["Content summarization in progress"],
                []
            )
    
    @staticmethod
    async def search_content(
        search_request: ContentSearchRequest,
        db: Session
    ) -> ContentSearchResponse:
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
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate query embedding"
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
        
        return ContentSearchResponse(
            query=search_request.query,
            results=[],
            total_results=0
        )
