"""
Quiz service layer for business logic.
"""

import logging
import random

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.content.llm_client import LLMClient
from app.content.models import Chunk, Topic
from app.quiz.models import QuizAnswer, QuizQuestion
from app.quiz.schemas import (
    QuestionCreate,
    QuestionOption,
    QuizAnswerResponse,
    QuizAnswerSubmit,
    QuizGenerateRequest,
    QuizQuestionResponse,
)
from app.users.models import User
from app.utils.timestamps import utcnow

logger = logging.getLogger(__name__)


class QuizService:
    """Service class for quiz operations."""

    @staticmethod
    def get_question_by_id(question_id: int, db: Session) -> QuizQuestion | None:
        """Get question by ID."""
        return db.query(QuizQuestion).filter(QuizQuestion.id == question_id).first()

    @staticmethod
    async def generate_or_fetch_questions(request: QuizGenerateRequest, db: Session) -> list[QuizQuestionResponse]:
        """
        Generate or fetch quiz questions for a topic.

        First checks for existing questions in database.
        If insufficient, generates new questions using LLM.

        Args:
            request: Quiz generation request
            db: Database session

        Returns:
            List[QuizQuestionResponse]: List of quiz questions
        """
        # Check if topic exists
        topic = db.query(Topic).filter(Topic.id == request.topic_id).first()
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

        # Query existing questions
        query = db.query(QuizQuestion).filter(QuizQuestion.topic_id == request.topic_id)

        if request.difficulty:
            query = query.filter(QuizQuestion.difficulty == request.difficulty)

        existing_questions = query.all()

        # If we have enough questions, return random sample
        if len(existing_questions) >= request.count:
            selected = random.sample(existing_questions, request.count)
            return [QuizService._format_question_response(q) for q in selected]

        # Otherwise, generate new questions
        logger.info(f"Generating {request.count} new questions for topic {request.topic_id}")

        # Get chunks for context
        chunks = db.query(Chunk).filter(Chunk.topic_id == request.topic_id).limit(5).all()

        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No content available for this topic to generate questions",
            )

        # Generate questions using LLM
        new_questions = await QuizService._generate_questions_with_llm(
            topic=topic,
            chunks=chunks,
            count=request.count - len(existing_questions),
            difficulty=request.difficulty,
            db=db,
        )

        # Combine existing and new questions
        all_questions = existing_questions + new_questions
        selected = random.sample(all_questions, min(request.count, len(all_questions)))

        return [QuizService._format_question_response(q) for q in selected]

    @staticmethod
    async def _generate_questions_with_llm(
        topic: Topic, chunks: list[Chunk], count: int, difficulty: str | None, db: Session
    ) -> list[QuizQuestion]:
        """
        Generate questions using LLM with hallucination prevention.

        Args:
            topic: Topic for questions
            chunks: Content chunks to base questions on
            count: Number of questions to generate
            difficulty: Optional difficulty level
            db: Database session

        Returns:
            List[QuizQuestion]: Generated questions (stored in DB with question_id)
        """
        # Combine chunk texts
        context = "\n\n".join([chunk.text for chunk in chunks[:3]])  # Limit context size

        difficulty_str = difficulty or "medium"

        try:
            # Use centralized LLM client with hallucination prevention
            questions_data = await LLMClient.generate_questions(
                topic_name=topic.name, chunks_text=context, count=count, difficulty=difficulty_str
            )

            # Create question objects and save to DB
            questions = []
            for q_data in questions_data[:count]:
                question = QuizQuestion(
                    topic_id=topic.id,
                    stem=q_data["stem"],
                    option_a=q_data["option_a"],
                    option_b=q_data["option_b"],
                    option_c=q_data["option_c"],
                    option_d=q_data["option_d"],
                    correct_option=q_data["correct_option"].upper(),
                    explanation=q_data.get("explanation", ""),
                    difficulty=difficulty or "medium",
                    source_chunk_id=chunks[0].id if chunks else None,
                    created_at=utcnow(),
                )

                db.add(question)
                questions.append(question)

            db.commit()

            # Refresh to get IDs
            for q in questions:
                db.refresh(q)

            logger.info(f"Generated and stored {len(questions)} new questions with IDs")

            return questions

        except Exception as e:
            logger.error(f"Error generating questions with LLM: {e}")
            return []

    @staticmethod
    def _format_question_response(question: QuizQuestion) -> QuizQuestionResponse:
        """Format question for response (without revealing correct answer)."""
        return QuizQuestionResponse(
            id=question.id,
            topic_id=question.topic_id,
            stem=question.stem,
            options=[
                QuestionOption(label="A", text=question.option_a),
                QuestionOption(label="B", text=question.option_b),
                QuestionOption(label="C", text=question.option_c),
                QuestionOption(label="D", text=question.option_d),
            ],
            difficulty=question.difficulty.value,
        )

    @staticmethod
    def submit_answer(answer_data: QuizAnswerSubmit, db: Session) -> QuizAnswerResponse:
        """
        Submit and grade quiz answer.

        Updates mastery score based on correctness.

        Args:
            answer_data: Answer submission data
            db: Database session

        Returns:
            QuizAnswerResponse: Answer result with feedback
        """
        # Validate user
        user = db.query(User).filter(User.id == answer_data.user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Get question
        question = QuizService.get_question_by_id(answer_data.question_id, db)
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

        # Check correctness
        correct = answer_data.chosen_option == question.correct_option

        # Save answer
        quiz_answer = QuizAnswer(
            user_id=answer_data.user_id,
            question_id=answer_data.question_id,
            chosen_option=answer_data.chosen_option,
            correct=correct,
            response_time_sec=answer_data.response_time_sec,
            created_at=utcnow(),
        )

        db.add(quiz_answer)
        db.commit()
        db.refresh(quiz_answer)

        logger.info(f"User {answer_data.user_id} answered question {answer_data.question_id}: {correct}")

        # Update mastery score
        from app.mastery.service import MasteryService

        new_mastery = MasteryService.update_mastery_from_quiz(
            user_id=answer_data.user_id, topic_id=question.topic_id, correct=correct, db=db
        )

        return QuizAnswerResponse(
            answer_id=quiz_answer.id,
            correct=correct,
            correct_option=question.correct_option,
            explanation=question.explanation,
            user_answer=answer_data.chosen_option,
            topic_id=question.topic_id,
            new_mastery_score=new_mastery.mastery_score,
        )

    @staticmethod
    def create_question(question_data: QuestionCreate, db: Session) -> QuizQuestion:
        """
        Create a question manually.

        Args:
            question_data: Question data
            db: Database session

        Returns:
            QuizQuestion: Created question
        """
        question = QuizQuestion(
            topic_id=question_data.topic_id,
            stem=question_data.stem,
            option_a=question_data.option_a,
            option_b=question_data.option_b,
            option_c=question_data.option_c,
            option_d=question_data.option_d,
            correct_option=question_data.correct_option,
            explanation=question_data.explanation,
            difficulty=question_data.difficulty,
            created_at=utcnow(),
        )

        db.add(question)
        db.commit()
        db.refresh(question)

        logger.info(f"Created question: {question.id}")
        return question
