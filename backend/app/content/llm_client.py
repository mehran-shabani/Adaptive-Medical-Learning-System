"""
LLM client for generating content with hallucination restrictions.

This module centralizes all LLM interactions and enforces strict
guidelines to prevent hallucinations in medical content generation.
"""

import json
import logging
from typing import Any

import httpx
from fastapi import HTTPException, status

from app.config import settings

logger = logging.getLogger(__name__)


def validate_openai_config():
    """
    Validate OpenAI API configuration.

    Raises:
        HTTPException: If OpenAI API key is missing or invalid
    """
    if (
        not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY in {"", "sk-your-openai-api-key-here"}
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI API key is not configured. Please set OPENAI_API_KEY in environment variables.",
        )


# System prompt to restrict hallucinations
# This is kept as an editable string constant
MEDICAL_CONTENT_SYSTEM_PROMPT = """You are generating summaries and MCQs for Iranian medical board-style exams.

CRITICAL RULES:
1. Only use the provided chunks/content
2. Do not invent new drug names or guidelines
3. Do not add information not present in the source material
4. If information is missing in the provided chunks, answer: "INSUFFICIENT_SOURCE"
5. Be precise and clinically accurate
6. Use evidence-based medical knowledge only from the provided context

Your responses must be traceable to the source material provided."""


class LLMClient:
    """
    Centralized LLM client with hallucination prevention.

    All LLM interactions should go through this client to ensure
    consistent prompt engineering and safety measures.
    """

    @staticmethod
    async def generate_questions(
        topic_name: str, chunks_text: str, count: int, difficulty: str = "medium"
    ) -> list[dict[str, Any]]:
        """
        Generate quiz questions with strict adherence to source material.

        Args:
            topic_name: Topic name
            chunks_text: Combined text from content chunks
            count: Number of questions to generate
            difficulty: Difficulty level (easy/medium/hard)

        Returns:
            List[Dict]: List of question dictionaries

        Raises:
            HTTPException: If OpenAI API key is not configured

        Example:
            questions = await LLMClient.generate_questions(
                topic_name="DKA Management",
                chunks_text="...",
                count=5,
                difficulty="medium"
            )
        """
        # Validate OpenAI configuration
        validate_openai_config()
        user_prompt = f"""Topic: {topic_name}

Source Material:
{chunks_text[:3000]}

Generate {count} high-quality multiple choice questions based ONLY on the content provided above.

Requirements:
- Clinical vignette-style stems appropriate for Iranian medical board exams
- 4 options (A, B, C, D) per question
- Exactly one correct answer per question
- Brief explanation citing the source material
- {difficulty} difficulty level

IMPORTANT: Do not add information beyond what is in the source material.

Format response as JSON array with structure:
[
  {{
    "stem": "question text",
    "option_a": "first option",
    "option_b": "second option",
    "option_c": "third option",
    "option_d": "fourth option",
    "correct_option": "A" | "B" | "C" | "D",
    "explanation": "explanation based on source material"
  }}
]

Respond ONLY with the JSON array."""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.OPENAI_BASE_URL}/chat/completions",
                    headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}", "Content-Type": "application/json"},
                    json={
                        "model": settings.LLM_MODEL,
                        "messages": [
                            {"role": "system", "content": MEDICAL_CONTENT_SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt},
                        ],
                        "temperature": 0.7,  # Lower temperature for more deterministic output
                        "max_tokens": 2500,
                    },
                    timeout=60.0,
                )

                response.raise_for_status()
                data = response.json()

                llm_content = data["choices"][0]["message"]["content"]
                questions = json.loads(llm_content)

                logger.info(f"Generated {len(questions)} questions for {topic_name}")
                return questions[:count]

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from OpenAI API: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Invalid OpenAI API key. Please check your configuration.",
                )
            elif e.response.status_code == 429:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="OpenAI API rate limit exceeded. Please try again later.",
                )
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"OpenAI API error: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to parse LLM response. Please try again.",
            )
        except Exception as e:
            logger.error(f"Unexpected error generating questions with LLM: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error generating questions: {str(e)}"
            )

    @staticmethod
    async def generate_summary(topic_name: str, chunks_text: str, include_high_yield: bool = True) -> dict[str, Any]:
        """
        Generate topic summary with key points and high-yield traps.

        Args:
            topic_name: Topic name
            chunks_text: Combined text from content chunks
            include_high_yield: Include high-yield clinical traps

        Returns:
            Dict: Summary data with keys: summary, key_points, high_yield_traps, citations

        Raises:
            HTTPException: If OpenAI API key is not configured

        Example:
            summary = await LLMClient.generate_summary(
                topic_name="DKA Management",
                chunks_text="...",
                include_high_yield=True
            )
        """
        # Validate OpenAI configuration
        validate_openai_config()
        user_prompt = f"""Topic: {topic_name}

Source Material:
{chunks_text[:4000]}

Create a comprehensive summary based ONLY on the provided source material.

Provide:
1. Concise summary (2-3 paragraphs)
2. 5-7 key clinical points
{"3. 3-5 high-yield clinical traps or pearls" if include_high_yield else ""}

IMPORTANT: Only use information from the source material above. If a concept is mentioned, it must be traceable to the source.

Format response as JSON:
{{
  "summary": "text",
  "key_points": ["point1", "point2", ...],
  "high_yield_traps": [
    {{
      "title": "trap title",
      "description": "trap description",
      "clinical_pearl": "what to remember"
    }}
  ]
}}

Respond ONLY with the JSON."""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.OPENAI_BASE_URL}/chat/completions",
                    headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}", "Content-Type": "application/json"},
                    json={
                        "model": settings.LLM_MODEL,
                        "messages": [
                            {"role": "system", "content": MEDICAL_CONTENT_SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt},
                        ],
                        "temperature": 0.5,  # Lower temperature for factual accuracy
                        "max_tokens": 2000,
                    },
                    timeout=60.0,
                )

                response.raise_for_status()
                data = response.json()

                llm_content = data["choices"][0]["message"]["content"]
                result = json.loads(llm_content)

                logger.info(f"Generated summary for {topic_name}")
                return result

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from OpenAI API: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Invalid OpenAI API key. Please check your configuration.",
                )
            elif e.response.status_code == 429:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="OpenAI API rate limit exceeded. Please try again later.",
                )
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"OpenAI API error: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to parse LLM response. Please try again.",
            )
        except Exception as e:
            logger.error(f"Unexpected error generating summary with LLM: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error generating summary: {str(e)}"
            )
