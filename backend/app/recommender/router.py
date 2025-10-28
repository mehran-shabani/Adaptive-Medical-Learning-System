"""
Recommender API endpoints.
"""

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.recommender.schemas import StudyPlanRequest, StudyPlanResponse
from app.recommender.service import RecommenderService
from app.utils.security import get_current_user_from_token

router = APIRouter()


@router.get("/{user_id}/plan", response_model=StudyPlanResponse)
async def get_study_plan(
    user_id: int = Path(..., description="User ID"),
    duration_minutes: int = Query(120, ge=30, le=300, description="Study duration in minutes"),
    focus_topics: str | None = Query(None, description="Comma-separated topic IDs to focus on"),
    include_quiz: bool = Query(True, description="Include quiz questions in plan"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token),  # noqa: ARG001
):
    """
    Generate personalized study plan for user.

    **Authentication Required**: Bearer token

    Creates an adaptive 2-hour (or custom duration) study plan based on:
    - Current mastery levels (prioritizes weak areas with spaced repetition)
    - Time since last review (uses spaced repetition algorithm)
    - Never-studied topics
    - Optional focus topics

    The plan includes:
    - Ordered study blocks with time allocation and priority
    - Content summaries for each topic
    - Practice quiz questions (if include_quiz=true)
    - Spaced repetition reasoning

    After generation, the plan is logged in StudyPlanLog for tracking.

    Args:
        user_id: User ID
        duration_minutes: Desired study duration (default: 120 min)
        focus_topics: Optional comma-separated topic IDs (e.g., "1,5,12")
        include_quiz: Include quiz questions (default: true)
        db: Database session
        current_user: Current authenticated user

    Returns:
        StudyPlanResponse: Complete personalized study plan

    Example:
        GET /recommender/1/plan?duration_minutes=120&include_quiz=true
        Authorization: Bearer <JWT>
    """
    # Parse focus topics
    focus_topic_list = None
    if focus_topics:
        try:
            focus_topic_list = [int(t.strip()) for t in focus_topics.split(",")]
        except ValueError:
            focus_topic_list = None

    return await RecommenderService.generate_study_plan(
        user_id=user_id,
        duration_minutes=duration_minutes,
        focus_topics=focus_topic_list,
        include_quiz=include_quiz,
        db=db,
    )


@router.post("/{user_id}/plan", response_model=StudyPlanResponse)
async def generate_study_plan_post(request: StudyPlanRequest, db: Session = Depends(get_db)):
    """
    Generate study plan (POST version with body).

    Alternative to GET endpoint, accepts JSON body for more complex requests.

    Args:
        request: Study plan request parameters
        db: Database session

    Returns:
        StudyPlanResponse: Complete personalized study plan

    Example:
        POST /recommender/1/plan
        {
            "user_id": 1,
            "duration_minutes": 120,
            "focus_topics": [5, 7, 9],
            "include_quiz": true
        }
    """
    return await RecommenderService.generate_study_plan(
        user_id=request.user_id,
        duration_minutes=request.duration_minutes,
        focus_topics=request.focus_topics,
        include_quiz=request.include_quiz,
        db=db,
    )
