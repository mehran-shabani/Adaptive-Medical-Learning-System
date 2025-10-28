"""
User management API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.users.schemas import UserResponse, UserUpdate, UserProfile
from app.users.service import UserService

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user by ID.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        UserResponse: User information
        
    Raises:
        HTTPException: If user not found
    """
    user = UserService.get_user_by_id(user_id, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed user profile with statistics.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        UserProfile: Detailed user profile
    """
    return UserService.get_user_profile(user_id, db)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user profile.
    
    Args:
        user_id: User ID
        user_data: User update data
        db: Database session
        
    Returns:
        UserResponse: Updated user information
    """
    return UserService.update_user(user_id, user_data, db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete user account.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        None: 204 No Content on success
    """
    UserService.delete_user(user_id, db)
    return None
