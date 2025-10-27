"""
SQLAlchemy models for user management.
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
import enum

from app.db import Base
from app.utils.timestamps import utcnow


class StudyLevel(str, enum.Enum):
    """Enum for medical student study levels."""
    INTERN = "intern"
    RESIDENT = "resident"
    FELLOW = "fellow"
    PRACTICING = "practicing"


class TargetSpecialty(str, enum.Enum):
    """Enum for target medical specialties."""
    CARDIOLOGY = "cardiology"
    RADIOLOGY = "radiology"
    INTERNAL_MEDICINE = "internal_medicine"
    SURGERY = "surgery"
    EMERGENCY_MEDICINE = "emergency_medicine"
    PEDIATRICS = "pediatrics"
    NEUROLOGY = "neurology"
    GENERAL = "general"


class User(Base):
    """
    User model representing a medical student.
    
    Attributes:
        id: Primary key
        phone_number: Unique phone number for authentication
        name: User's full name
        study_level: Current study level (intern, resident, etc.)
        target_specialty: Target specialty for residency
        created_at: Account creation timestamp
        updated_at: Last profile update timestamp
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    study_level = Column(
        Enum(StudyLevel),
        default=StudyLevel.INTERN,
        nullable=False
    )
    target_specialty = Column(
        Enum(TargetSpecialty),
        default=TargetSpecialty.GENERAL,
        nullable=True
    )
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
    
    # Relationships
    quiz_answers = relationship("QuizAnswer", back_populates="user", cascade="all, delete-orphan")
    masteries = relationship("Mastery", back_populates="user", cascade="all, delete-orphan")
    study_plan_logs = relationship("StudyPlanLog", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone_number}, name={self.name})>"
