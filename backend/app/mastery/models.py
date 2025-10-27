"""
SQLAlchemy models for mastery tracking.
"""
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base
from app.utils.timestamps import utcnow


class Mastery(Base):
    """
    Mastery model for tracking user proficiency per topic.
    
    Stores a score (0.0 to 1.0) representing student's mastery level.
    Updated based on quiz performance using spaced repetition principles.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to user
        topic_id: Foreign key to topic
        mastery_score: Score from 0.0 to 1.0 (0% to 100%)
        last_reviewed_at: Last time topic was studied/tested
        review_count: Number of times reviewed
        created_at: First mastery record creation
        updated_at: Last mastery update
    """
    __tablename__ = "masteries"
    __table_args__ = (
        UniqueConstraint('user_id', 'topic_id', name='unique_user_topic_mastery'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)
    
    mastery_score = Column(Float, nullable=False, default=0.0)
    last_reviewed_at = Column(DateTime, nullable=True)
    review_count = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
    
    # Relationships
    user = relationship("User", back_populates="masteries")
    topic = relationship("Topic", back_populates="masteries")
    
    def __repr__(self):
        return f"<Mastery(user_id={self.user_id}, topic_id={self.topic_id}, score={self.mastery_score:.2f})>"


class StudyPlanLog(Base):
    """
    Study plan log for tracking generated study plans.
    
    Stores JSON of recommended study plans for analysis and tracking.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to user
        plan_json: JSON string of study plan
        duration_minutes: Planned duration
        completed: Whether plan was completed
        created_at: Plan generation timestamp
    """
    __tablename__ = "study_plan_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    plan_json = Column(Text, nullable=False)  # JSON string
    duration_minutes = Column(Integer, nullable=False)
    completed = Column(Integer, default=0)  # 0 = not started, 1 = in progress, 2 = completed
    
    created_at = Column(DateTime, default=utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="study_plan_logs")
    
    def __repr__(self):
        return f"<StudyPlanLog(id={self.id}, user_id={self.user_id}, duration={self.duration_minutes}min)>"
