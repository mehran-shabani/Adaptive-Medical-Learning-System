"""
User service layer for business logic.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate, UserProfile
from app.utils.timestamps import utcnow

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user operations."""
    
    @staticmethod
    def get_user_by_id(user_id: int, db: Session) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_phone(phone_number: str, db: Session) -> Optional[User]:
        """
        Get user by phone number.
        
        Args:
            phone_number: Phone number
            db: Database session
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        return db.query(User).filter(User.phone_number == phone_number).first()
    
    @staticmethod
    def create_user(user_data: UserCreate, db: Session) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User creation data
            db: Database session
            
        Returns:
            User: Created user
            
        Raises:
            HTTPException: If phone number already exists
        """
        # Check if user already exists
        existing_user = UserService.get_user_by_phone(user_data.phone_number, db)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
        
        # Create new user
        user = User(
            phone_number=user_data.phone_number,
            name=user_data.name,
            study_level=user_data.study_level,
            target_specialty=user_data.target_specialty,
            created_at=utcnow()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Created user: {user.id} - {user.phone_number}")
        return user
    
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate, db: Session) -> User:
        """
        Update user profile.
        
        Args:
            user_id: User ID
            user_data: User update data
            db: Database session
            
        Returns:
            User: Updated user
            
        Raises:
            HTTPException: If user not found
        """
        user = UserService.get_user_by_id(user_id, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        user.updated_at = utcnow()
        
        db.commit()
        db.refresh(user)
        
        logger.info(f"Updated user: {user.id}")
        return user
    
    @staticmethod
    def get_user_profile(user_id: int, db: Session) -> UserProfile:
        """
        Get detailed user profile with statistics.
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            UserProfile: User profile with statistics
            
        Raises:
            HTTPException: If user not found
        """
        user = UserService.get_user_by_id(user_id, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # TODO: Calculate statistics from related data
        # - total_quizzes_taken from quiz_answers
        # - average_mastery from masteries
        # - strong_topics and weak_topics from masteries
        
        profile = UserProfile(
            id=user.id,
            phone_number=user.phone_number,
            name=user.name,
            study_level=user.study_level.value,
            target_specialty=user.target_specialty.value if user.target_specialty else None,
            created_at=user.created_at,
            total_quizzes_taken=len(user.quiz_answers),
            average_mastery=0.0,  # TODO: Calculate
            strong_topics=[],  # TODO: Calculate
            weak_topics=[]  # TODO: Calculate
        )
        
        return profile
    
    @staticmethod
    def delete_user(user_id: int, db: Session) -> None:
        """
        Delete user account.
        
        Args:
            user_id: User ID
            db: Database session
            
        Raises:
            HTTPException: If user not found
        """
        user = UserService.get_user_by_id(user_id, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        db.delete(user)
        db.commit()
        
        logger.info(f"Deleted user: {user_id}")
