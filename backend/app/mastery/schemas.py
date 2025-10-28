"""
Pydantic schemas for mastery tracking endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class MasteryScore(BaseModel):
    """Schema for single topic mastery score."""

    topic_id: int
    topic_name: str
    system_name: str | None
    mastery_score: float = Field(..., ge=0.0, le=1.0)
    last_reviewed_at: datetime | None
    review_count: int

    class Config:
        from_attributes = True


class UserMasteryDashboard(BaseModel):
    """Schema for user's mastery dashboard."""

    user_id: int
    overall_mastery: float = Field(..., description="Average mastery across all topics")
    total_topics: int
    strong_topics: list[MasteryScore] = Field(..., description="Topics with high mastery (>0.7)")
    weak_topics: list[MasteryScore] = Field(..., description="Topics with low mastery (<0.7)")
    recent_activity: list[MasteryScore] = Field(..., description="Recently reviewed topics")

    # System-level breakdown
    by_system: dict = Field(..., description="Mastery by body system")


class MasteryUpdate(BaseModel):
    """Schema for mastery update."""

    user_id: int
    topic_id: int
    old_score: float
    new_score: float
    change: float
    reason: str = Field(..., description="Reason for update (e.g., 'quiz_correct', 'quiz_incorrect')")


class TopicMasteryDetail(BaseModel):
    """Detailed mastery information for a topic."""

    topic_id: int
    topic_name: str
    mastery_score: float
    last_reviewed_at: datetime | None
    review_count: int

    # Quiz statistics for this topic
    total_questions_answered: int
    correct_answers: int
    accuracy: float

    # Recommendations
    needs_review: bool
    recommended_action: str = Field(..., description="Next recommended action")


class MasteryHistory(BaseModel):
    """Historical mastery scores for a topic."""

    topic_id: int
    topic_name: str
    history: list[dict] = Field(..., description="List of {date, score} points")
