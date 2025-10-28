"""
Text embedding utilities using OpenAI embedding models.
"""

import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating text embeddings using OpenAI API.

    Uses text-embedding-3-small model (1536 dimensions) by default.
    """

    def __init__(
        self,
        api_key: str = settings.OPENAI_API_KEY,
        model: str = settings.EMBEDDING_MODEL,
        base_url: str = settings.OPENAI_BASE_URL,
    ):
        """
        Initialize embedding service.

        Args:
            api_key: OpenAI API key
            model: Embedding model name
            base_url: OpenAI API base URL
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.embedding_endpoint = f"{base_url}/embeddings"

    async def create_embedding(self, text: str) -> list[float] | None:
        """
        Create embedding for single text.

        Args:
            text: Input text to embed

        Returns:
            Optional[List[float]]: Embedding vector or None on error

        Example:
            embedding = await service.create_embedding("Diabetic ketoacidosis is...")
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.embedding_endpoint,
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json={"input": text, "model": self.model},
                    timeout=30.0,
                )

                response.raise_for_status()
                data = response.json()

                embedding = data["data"][0]["embedding"]
                return embedding

        except httpx.HTTPError as e:
            logger.error(f"HTTP error creating embedding: {e}")
            return None
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            return None

    async def create_embeddings_batch(self, texts: list[str], batch_size: int = 100) -> list[list[float] | None]:
        """
        Create embeddings for multiple texts in batches.

        Args:
            texts: List of input texts
            batch_size: Number of texts per batch

        Returns:
            List[Optional[List[float]]]: List of embedding vectors

        Example:
            embeddings = await service.create_embeddings_batch(chunk_texts)
        """
        embeddings = []

        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        self.embedding_endpoint,
                        headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                        json={"input": batch, "model": self.model},
                        timeout=60.0,
                    )

                    response.raise_for_status()
                    data = response.json()

                    # Extract embeddings in order
                    batch_embeddings = [item["embedding"] for item in data["data"]]
                    embeddings.extend(batch_embeddings)

                    logger.info(f"Created embeddings for batch {i // batch_size + 1}")

            except httpx.HTTPError as e:
                logger.error(f"HTTP error creating embeddings batch: {e}")
                # Add None for failed embeddings
                embeddings.extend([None] * len(batch))
            except Exception as e:
                logger.error(f"Error creating embeddings batch: {e}")
                embeddings.extend([None] * len(batch))

        return embeddings

    def get_embedding_dimension(self) -> int:
        """
        Get embedding dimension for current model.

        Returns:
            int: Embedding dimension
        """
        # Model dimension mapping
        dimensions = {"text-embedding-3-small": 1536, "text-embedding-3-large": 3072, "text-embedding-ada-002": 1536}

        return dimensions.get(self.model, 1536)


# TODO: Implement caching mechanism for embeddings
# TODO: Add retry logic with exponential backoff
# TODO: Support alternative embedding providers (e.g., local models, Cohere)
