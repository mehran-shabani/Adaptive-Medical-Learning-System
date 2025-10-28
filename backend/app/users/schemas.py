"""
Pydantic schemas for user management endpoints.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base schema for user data."""
    name: str = Field(..., min_length=1, max_length=100)
    study_level: str = Field(..., description="Study level: intern, resident, fellow, practicing")
    target_specialty: Optional[str] = Field(None, description="Target specialty for residency")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    phone_number: str = Field(..., description="Phone number for authentication")


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    study_level: Optional[str] = None
    target_specialty: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    phone_number: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """Detailed user profile response."""
    id: int
    phone_number: str
    name: str
    study_level: str
    target_specialty: Optional[str]
    created_at: datetime
    
    # Statistics (to be populated from related data)
    total_quizzes_taken: int = 0
    average_mastery: float = 0.0
    strong_topics: list[str] = []
    weak_topics: list[str] = []
    
    class Config:
        from_attributes = True
