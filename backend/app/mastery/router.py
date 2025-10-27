"""
Mastery tracking API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from app.db import get_db
from app.mastery.schemas import UserMasteryDashboard, TopicMasteryDetail
from app.mastery.service import MasteryService

router = APIRouter()


@router.get("/{user_id}", response_model=UserMasteryDashboard)
async def get_user_mastery(
    user_id: int = Path(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """
    Get mastery dashboard for user.
    
    Returns comprehensive view of user's proficiency across all topics:
    - Overall mastery percentage
    - Strong topics (mastery >= 70%)
    - Weak topics (mastery < 70%)
    - Recent activity
    - Breakdown by body system
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        UserMasteryDashboard: Complete mastery dashboard
        
    Example:
        GET /mastery/1
    """
    return MasteryService.get_user_mastery_dashboard(user_id, db)


@router.get("/{user_id}/topic/{topic_id}", response_model=TopicMasteryDetail)
async def get_topic_mastery(
    user_id: int = Path(..., description="User ID"),
    topic_id: int = Path(..., description="Topic ID"),
    db: Session = Depends(get_db)
):
    """
    Get detailed mastery information for a specific topic.
    
    Includes:
    - Current mastery score
    - Quiz statistics (total answered, accuracy)
    - Last review date
    - Recommendation for next action
    
    Args:
        user_id: User ID
        topic_id: Topic ID
        db: Database session
        
    Returns:
        TopicMasteryDetail: Detailed mastery information
        
    Example:
        GET /mastery/1/topic/5
    """
    return MasteryService.get_topic_mastery_detail(user_id, topic_id, db)
