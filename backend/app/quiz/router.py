"""
Quiz API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db import get_db
from app.quiz.schemas import (
    QuizQuestionResponse, QuizGenerateRequest, QuizAnswerSubmit,
    QuizAnswerResponse, QuestionCreate, QuizQuestionDetailResponse
)
from app.quiz.service import QuizService
from app.utils.security import get_current_user_from_token

router = APIRouter()


@router.get("/generate", response_model=List[QuizQuestionResponse])
async def generate_quiz(
    topic_id: int = Query(..., description="Topic ID"),
    limit: int = Query(5, ge=1, le=20, description="Number of questions (pagination support)"),
    difficulty: Optional[str] = Query(None, regex="^(easy|medium|hard)$", description="Filter by difficulty"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Generate or fetch quiz questions for a topic.
    
    **Authentication Required**: Bearer token
    **Pagination/Filtering**: Supports limit and difficulty parameters.
    
    First checks for existing questions in database.
    If insufficient, generates new questions using AI with hallucination prevention.
    All generated questions are saved to DB with question_id for answer submission.
    
    Args:
        topic_id: Topic to generate questions for (required)
        limit: Number of questions (default: 5, max: 20)
        difficulty: Filter by difficulty (easy, medium, hard) - optional
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[QuizQuestionResponse]: List of quiz questions with question_id
        
    Example:
        GET /quiz/generate?topic_id=5&limit=10&difficulty=medium
        Authorization: Bearer <JWT>
    """
    request = QuizGenerateRequest(
        topic_id=topic_id,
        count=limit,  # Use 'limit' parameter name per Phase 2 requirements
        difficulty=difficulty
    )
    
    return await QuizService.generate_or_fetch_questions(request, db)


@router.post("/answer", response_model=QuizAnswerResponse)
async def submit_answer(
    answer_data: QuizAnswerSubmit,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Submit answer to a quiz question.
    
    **Authentication Required**: Bearer token
    
    Grades the answer, provides feedback, and updates mastery score.
    After submission:
    - QuizAnswer is saved in database
    - Mastery score for the topic is updated
    - last_reviewed_at is set to now()
    
    Args:
        answer_data: Answer submission data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        QuizAnswerResponse: Answer result with feedback and updated mastery
        
    Example:
        POST /quiz/answer
        Authorization: Bearer <JWT>
        {
            "user_id": 1,
            "question_id": 42,
            "chosen_option": "B",
            "response_time_sec": 45.5
        }
    """
    return QuizService.submit_answer(answer_data, db)


@router.post("/questions", response_model=QuizQuestionDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a quiz question manually.
    
    Useful for admin/faculty to add curated questions.
    
    Args:
        question_data: Question data
        db: Database session
        
    Returns:
        QuizQuestionDetailResponse: Created question
    """
    return QuizService.create_question(question_data, db)


@router.get("/questions/{question_id}", response_model=QuizQuestionDetailResponse)
async def get_question_detail(
    question_id: int,
    db: Session = Depends(get_db)
):
    """
    Get question details (including correct answer).
    
    Use for review after answering or for admin purposes.
    
    Args:
        question_id: Question ID
        db: Database session
        
    Returns:
        QuizQuestionDetailResponse: Full question details
    """
    question = QuizService.get_question_by_id(question_id, db)
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return question
