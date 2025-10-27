"""
Pydantic schemas for recommender endpoints.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class QuizBlock(BaseModel):
    """Quiz block in study plan."""
    question_id: int
    stem: str
    options: List[dict]


class StudyBlock(BaseModel):
    """Single study block in recommended plan."""
    topic_id: int
    topic: str = Field(..., description="Topic name")
    duration_minutes: int = Field(..., description="Recommended study duration")
    
    # Content to study
    review_material: Optional[str] = Field(None, description="Summary or key points to review")
    
    # Quiz questions
    quiz_questions: List[QuizBlock] = Field(default_factory=list, description="Practice questions")
    
    # Metadata
    current_mastery: float = Field(..., description="Current mastery score")
    reason: str = Field(..., description="Why this topic is recommended")
    priority: str = Field(..., description="Priority level: high, medium, low")


class StudyPlanResponse(BaseModel):
    """Complete study plan response."""
    user_id: int
    duration_minutes: int = Field(..., description="Total plan duration")
    generated_at: datetime
    
    blocks: List[StudyBlock] = Field(..., description="Ordered study blocks")
    
    # Summary
    total_topics: int
    total_questions: int
    average_current_mastery: float
    
    # Recommendations
    focus_areas: List[str] = Field(..., description="Main focus areas for this session")
    next_review_date: Optional[datetime] = Field(None, description="When to do next review")


class StudyPlanRequest(BaseModel):
    """Request parameters for study plan generation."""
    user_id: int
    duration_minutes: int = Field(120, ge=30, le=300, description="Desired study duration")
    focus_topics: Optional[List[int]] = Field(None, description="Optional: focus on specific topics")
    include_quiz: bool = Field(True, description="Include quiz questions in plan")
