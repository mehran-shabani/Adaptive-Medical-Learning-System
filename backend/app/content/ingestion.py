"""
PDF ingestion pipeline for processing medical content.
"""
from typing import List, Optional, Dict, Any
import os
from pathlib import Path
import logging
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
from sqlalchemy.orm import Session

from app.config import settings
from app.content.models import Topic, Chunk
from app.content.splitter import TextSplitter
from app.content.embedding import EmbeddingService
from app.utils.timestamps import utcnow

logger = logging.getLogger(__name__)


class PDFIngestionService:
    """
    Service for ingesting PDF files and creating searchable chunks.
    
    Pipeline:
    1. Extract text from PDF
    2. Split text into chunks
    3. Generate embeddings for chunks
    4. Store chunks in database with embeddings
    """
    
    def __init__(self, db: Session):
        """
        Initialize ingestion service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.text_splitter = TextSplitter()
        self.embedding_service = EmbeddingService()
    
    async def ingest_pdf(
        self,
        pdf_path: str,
        topic_id: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ingest a PDF file and create chunks.
        
        Args:
            pdf_path: Path to PDF file
            topic_id: Topic ID to associate chunks with
            metadata: Optional metadata for chunks
            
        Returns:
            Dict: Ingestion results with statistics
            
        Raises:
            FileNotFoundError: If PDF file not found
            ValueError: If topic not found
            
        Example:
            result = await ingestion.ingest_pdf(
                "/path/to/harrison_endocrine.pdf",
                topic_id=5,
                metadata={"source": "Harrison's 21st Edition"}
            )
        """
        # Validate inputs
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise ValueError(f"Topic not found: {topic_id}")
        
        logger.info(f"Starting ingestion of {pdf_path} for topic {topic_id}")
        
        # Step 1: Extract text from PDF
        text, page_count = self._extract_text_from_pdf(pdf_path)
        
        if not text or len(text.strip()) < 100:
            raise ValueError("Insufficient text extracted from PDF")
        
        logger.info(f"Extracted {len(text)} characters from {page_count} pages")
        
        # Step 2: Split text into chunks
        chunk_metadata = metadata or {}
        chunk_metadata.update({
            "source_pdf": os.path.basename(pdf_path),
            "page_count": page_count
        })
        
        chunks_data = self.text_splitter.split_text(text, chunk_metadata)
        logger.info(f"Created {len(chunks_data)} chunks")
        
        # Step 3: Generate embeddings
        chunk_texts = [chunk["text"] for chunk in chunks_data]
        embeddings = await self.embedding_service.create_embeddings_batch(chunk_texts)
        
        successful_embeddings = sum(1 for e in embeddings if e is not None)
        logger.info(f"Generated {successful_embeddings}/{len(embeddings)} embeddings")
        
        # Step 4: Store chunks in database
        stored_chunks = []
        for chunk_data, embedding in zip(chunks_data, embeddings):
            chunk = Chunk(
                topic_id=topic_id,
                text=chunk_data["text"],
                embedding_vector=embedding,
                source_pdf_path=pdf_path,
                page_start=1,  # TODO: Track actual page numbers
                page_end=page_count,
                metadata=str(chunk_data),  # Store as JSON string
                created_at=utcnow()
            )
            
            self.db.add(chunk)
            stored_chunks.append(chunk)
        
        self.db.commit()
        logger.info(f"Stored {len(stored_chunks)} chunks in database")
        
        return {
            "success": True,
            "pdf_path": pdf_path,
            "topic_id": topic_id,
            "page_count": page_count,
            "chunk_count": len(stored_chunks),
            "embedding_count": successful_embeddings,
            "failed_embeddings": len(embeddings) - successful_embeddings
        }
    
    def _extract_text_from_pdf(self, pdf_path: str) -> tuple[str, int]:
        """
        Extract text from PDF file.
        
        Tries PyMuPDF first (faster), falls back to pdfminer.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            tuple[str, int]: Extracted text and page count
        """
        try:
            # Try PyMuPDF first (faster and better layout preservation)
            return self._extract_with_pymupdf(pdf_path)
        except Exception as e:
            logger.warning(f"PyMuPDF extraction failed: {e}, trying pdfminer")
            try:
                return self._extract_with_pdfminer(pdf_path)
            except Exception as e2:
                logger.error(f"Both extraction methods failed: {e2}")
                raise ValueError("Failed to extract text from PDF")
    
    def _extract_with_pymupdf(self, pdf_path: str) -> tuple[str, int]:
        """Extract text using PyMuPDF (fitz)."""
        doc = fitz.open(pdf_path)
        text_parts = []
        
        for page in doc:
            text_parts.append(page.get_text())
        
        page_count = len(doc)
        doc.close()
        
        return "\n\n".join(text_parts), page_count
    
    def _extract_with_pdfminer(self, pdf_path: str) -> tuple[str, int]:
        """Extract text using pdfminer.six."""
        text = extract_text(pdf_path)
        
        # Estimate page count (rough heuristic)
        page_count = max(1, len(text) // 3000)
        
        return text, page_count


# TODO: Implement table extraction
# TODO: Implement figure/image extraction with OCR
# TODO: Add support for other document formats (DOCX, HTML)
# TODO: Implement incremental ingestion (detect already processed pages)
# TODO: Add progress tracking for long-running ingestion jobs
