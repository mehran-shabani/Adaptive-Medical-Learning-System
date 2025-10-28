"""
Recommender service layer.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
import json

from app.recommender.schemas import StudyPlanResponse, StudyBlock, QuizBlock
from app.recommender.planner import StudyPlanner
from app.mastery.models import StudyPlanLog
from app.users.models import User
from app.quiz.service import QuizService
from app.quiz.schemas import QuizGenerateRequest
from app.content.service import ContentService
from app.utils.timestamps import utcnow

logger = logging.getLogger(__name__)


class RecommenderService:
    """Service class for adaptive recommendation operations."""
    
    @staticmethod
    async def generate_study_plan(
        user_id: int,
        duration_minutes: int,
        focus_topics: Optional[List[int]],
        include_quiz: bool,
        db: Session
    ) -> StudyPlanResponse:
        """
        Generate adaptive study plan for user.
        
        Args:
            user_id: User ID
            duration_minutes: Study duration
            focus_topics: Optional specific topics to focus on
            include_quiz: Whether to include quiz questions
            db: Database session
            
        Returns:
            StudyPlanResponse: Complete study plan
            
        Raises:
            HTTPException: If user not found
        """
        # Validate user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate plan using planner
        planner = StudyPlanner(db)
        plan_data = planner.generate_study_plan(
            user_id=user_id,
            duration_minutes=duration_minutes,
            focus_topics=focus_topics
        )
        
        # Enrich blocks with actual content
        enriched_blocks = []
        total_questions = 0
        
        for block_data in plan_data["blocks"]:
            # Get summary for topic
            try:
                summary_response = await ContentService.get_topic_summary(
                    topic_id=block_data["topic_id"],
                    include_high_yield=True,
                    db=db
                )
                review_material = summary_response.summary
            except Exception as e:
                logger.warning(f"Could not get summary for topic {block_data['topic_id']}: {e}")
                review_material = f"Study materials for {block_data['topic']}"
            
            # Generate quiz questions if requested
            quiz_questions = []
            if include_quiz and block_data.get("quiz_question_count", 0) > 0:
                try:
                    quiz_request = QuizGenerateRequest(
                        topic_id=block_data["topic_id"],
                        count=block_data["quiz_question_count"],
                        difficulty=None
                    )
                    questions = await QuizService.generate_or_fetch_questions(quiz_request, db)
                    
                    for q in questions:
                        quiz_questions.append(QuizBlock(
                            question_id=q.id,
                            stem=q.stem,
                            options=[{"label": opt.label, "text": opt.text} for opt in q.options]
                        ))
                    
                    total_questions += len(quiz_questions)
                    
                except Exception as e:
                    logger.warning(f"Could not generate quiz for topic {block_data['topic_id']}: {e}")
            
            # Create enriched block
            block = StudyBlock(
                topic_id=block_data["topic_id"],
                topic=block_data["topic"],
                duration_minutes=block_data["duration_minutes"],
                review_material=review_material,
                quiz_questions=quiz_questions,
                current_mastery=block_data["current_mastery"],
                reason=block_data["reason"],
                priority=block_data["priority"]
            )
            
            enriched_blocks.append(block)
        
        # Create response
        response = StudyPlanResponse(
            user_id=user_id,
            duration_minutes=duration_minutes,
            generated_at=plan_data["generated_at"],
            blocks=enriched_blocks,
            total_topics=plan_data["total_topics"],
            total_questions=total_questions,
            average_current_mastery=round(plan_data["average_current_mastery"], 3),
            focus_areas=plan_data["focus_areas"],
            next_review_date=None  # TODO: Calculate based on spaced repetition
        )
        
        # Log the plan
        RecommenderService._log_study_plan(user_id, response, db)
        
        logger.info(f"Generated study plan for user {user_id}: {len(enriched_blocks)} blocks, {total_questions} questions")
        
        return response
    
    @staticmethod
    def _log_study_plan(user_id: int, plan: StudyPlanResponse, db: Session):
        """Log study plan for analytics."""
        try:
            # Convert plan to JSON
            plan_json = plan.model_dump_json()
            
            log = StudyPlanLog(
                user_id=user_id,
                plan_json=plan_json,
                duration_minutes=plan.duration_minutes,
                completed=0,
                created_at=utcnow()
            )
            
            db.add(log)
            db.commit()
            
            logger.debug(f"Logged study plan {log.id} for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to log study plan: {e}")
            # Don't fail the request if logging fails
