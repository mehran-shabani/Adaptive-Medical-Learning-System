"""
Mastery tracking API endpoints.
"""

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.db import get_db
from app.mastery.schemas import TopicMasteryDetail, UserMasteryDashboard
from app.mastery.service import MasteryService
from app.utils.security import get_current_user_from_token

router = APIRouter()


@router.get("/{user_id}", response_model=UserMasteryDashboard)
async def get_user_mastery(
    user_id: int = Path(..., description="User ID"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token),  # noqa: ARG001
):
    """
    Get mastery dashboard for user.

    **Authentication Required**: Bearer token

    Returns comprehensive view of user's proficiency across all topics:
    - Overall mastery percentage
    - Strong topics (mastery >= 70%)
    - Weak topics (mastery < 70%)
    - Recent activity
    - Breakdown by body system

    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        UserMasteryDashboard: Complete mastery dashboard

    Example:
        GET /mastery/1
        Authorization: Bearer <JWT>
    """
    return MasteryService.get_user_mastery_dashboard(user_id, db)


@router.get("/{user_id}/topic/{topic_id}", response_model=TopicMasteryDetail)
async def get_topic_mastery(
    user_id: int = Path(..., description="User ID"),
    topic_id: int = Path(..., description="Topic ID"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token),  # noqa: ARG001
):
    """
    Get detailed mastery information for a specific topic.

    **Authentication Required**: Bearer token

    Includes:
    - Current mastery score
    - Quiz statistics (total answered, accuracy)
    - Last review date
    - Recommendation for next action

    Args:
        user_id: User ID
        topic_id: Topic ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        TopicMasteryDetail: Detailed mastery information

    Example:
        GET /mastery/1/topic/5
        Authorization: Bearer <JWT>
    """
    return MasteryService.get_topic_mastery_detail(user_id, topic_id, db)
