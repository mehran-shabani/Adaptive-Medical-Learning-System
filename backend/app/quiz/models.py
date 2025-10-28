"""
SQLAlchemy models for quiz management.
"""

import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db import Base
from app.utils.timestamps import utcnow


class DifficultyLevel(str, enum.Enum):
    """Enum for question difficulty levels."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuizQuestion(Base):
    """
    Quiz question model for MCQ questions.

    Standard 4-option multiple choice questions at residency level.

    Attributes:
        id: Primary key
        topic_id: Foreign key to topic
        stem: Question text/clinical vignette
        option_a: First answer option
        option_b: Second answer option
        option_c: Third answer option
        option_d: Fourth answer option
        correct_option: Correct answer (A, B, C, or D)
        explanation: Explanation of correct answer
        difficulty: Question difficulty level
        source_chunk_id: Optional reference to source chunk
        created_at: Question creation timestamp
    """

    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)

    stem = Column(Text, nullable=False)
    option_a = Column(String(500), nullable=False)
    option_b = Column(String(500), nullable=False)
    option_c = Column(String(500), nullable=False)
    option_d = Column(String(500), nullable=False)
    correct_option = Column(String(1), nullable=False)  # A, B, C, or D

    explanation = Column(Text, nullable=True)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.MEDIUM, nullable=False)

    source_chunk_id = Column(Integer, ForeignKey("chunks.id"), nullable=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    # Relationships
    topic = relationship("Topic", back_populates="quiz_questions")
    answers = relationship("QuizAnswer", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<QuizQuestion(id={self.id}, topic_id={self.topic_id}, difficulty={self.difficulty})>"


class QuizAnswer(Base):
    """
    Quiz answer model for tracking student responses.

    Attributes:
        id: Primary key
        user_id: Foreign key to user
        question_id: Foreign key to quiz question
        chosen_option: Option chosen by user (A, B, C, or D)
        correct: Whether answer was correct
        response_time_sec: Time taken to answer (seconds)
        created_at: Answer timestamp
    """

    __tablename__ = "quiz_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False, index=True)

    chosen_option = Column(String(1), nullable=False)  # A, B, C, or D
    correct = Column(Boolean, nullable=False)
    response_time_sec = Column(Float, nullable=True)

    created_at = Column(DateTime, default=utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="quiz_answers")
    question = relationship("QuizQuestion", back_populates="answers")

    def __repr__(self):
        return f"<QuizAnswer(id={self.id}, user_id={self.user_id}, correct={self.correct})>"
