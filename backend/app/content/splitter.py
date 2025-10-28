"""
Text splitting utilities for chunking PDF content.
"""
from typing import List, Tuple
import re
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class TextSplitter:
    """
    Text splitter for creating semantic chunks from medical content.
    
    Splits text intelligently based on:
    - Paragraph boundaries
    - Section headers
    - Word count limits
    - Semantic coherence
    """
    
    def __init__(
        self,
        chunk_size_min: int = settings.CHUNK_SIZE_MIN,
        chunk_size_max: int = settings.CHUNK_SIZE_MAX,
        chunk_overlap: int = settings.CHUNK_OVERLAP
    ):
        """
        Initialize text splitter.
        
        Args:
            chunk_size_min: Minimum words per chunk
            chunk_size_max: Maximum words per chunk
            chunk_overlap: Word overlap between chunks
        """
        self.chunk_size_min = chunk_size_min
        self.chunk_size_max = chunk_size_max
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str, metadata: dict = None) -> List[dict]:
        """
        Split text into chunks with metadata.
        
        Args:
            text: Text to split
            metadata: Optional metadata to include with each chunk
            
        Returns:
            List[dict]: List of chunks with text and metadata
            
        Example:
            chunks = splitter.split_text(pdf_text, {"source": "harrison.pdf"})
        """
        # Clean text
        text = self._clean_text(text)
        
        # Split into paragraphs
        paragraphs = self._split_paragraphs(text)
        
        # Group paragraphs into chunks
        chunks = self._create_chunks(paragraphs)
        
        # Add metadata
        chunk_dicts = []
        for i, chunk_text in enumerate(chunks):
            chunk_dict = {
                "text": chunk_text,
                "chunk_index": i,
                "word_count": len(chunk_text.split())
            }
            
            if metadata:
                chunk_dict.update(metadata)
            
            chunk_dicts.append(chunk_dict)
        
        logger.info(f"Split text into {len(chunk_dicts)} chunks")
        return chunk_dicts
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers (common pattern: "Page 123")
        text = re.sub(r'Page\s+\d+', '', text, flags=re.IGNORECASE)
        
        # Remove headers/footers (heuristic: very short lines at start/end)
        # TODO: Implement more sophisticated header/footer detection
        
        return text.strip()
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        # Split on double newlines or section breaks
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Filter out very short paragraphs (likely artifacts)
        paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 50]
        
        return paragraphs
    
    def _create_chunks(self, paragraphs: List[str]) -> List[str]:
        """
        Group paragraphs into chunks based on size constraints.
        
        Args:
            paragraphs: List of paragraph strings
            
        Returns:
            List[str]: List of chunk strings
        """
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        for paragraph in paragraphs:
            para_words = len(paragraph.split())
            
            # If adding this paragraph exceeds max size, start new chunk
            if current_word_count + para_words > self.chunk_size_max and current_chunk:
                # Finalize current chunk
                chunks.append(' '.join(current_chunk))
                
                # Start new chunk with overlap
                overlap_text = self._get_overlap_text(current_chunk)
                current_chunk = [overlap_text, paragraph] if overlap_text else [paragraph]
                current_word_count = len(' '.join(current_chunk).split())
            else:
                current_chunk.append(paragraph)
                current_word_count += para_words
            
            # If current chunk reaches minimum size and is at a good breaking point
            if current_word_count >= self.chunk_size_min:
                # Check if next paragraph would exceed max size
                # If so, break here
                pass  # Logic handled in next iteration
        
        # Add final chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _get_overlap_text(self, paragraphs: List[str]) -> str:
        """
        Get overlap text from end of previous chunk.
        
        Args:
            paragraphs: List of paragraphs in previous chunk
            
        Returns:
            str: Overlap text
        """
        if not paragraphs:
            return ""
        
        # Take last paragraph or last N words
        last_para = paragraphs[-1]
        words = last_para.split()
        
        if len(words) <= self.chunk_overlap:
            return last_para
        
        return ' '.join(words[-self.chunk_overlap:])


# TODO: Implement more advanced splitting strategies:
# - Medical section detection (e.g., "Pathophysiology:", "Clinical Presentation:")
# - Table and figure handling
# - Reference citation preservation
# - Semantic similarity-based splitting
