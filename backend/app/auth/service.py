"""
Authentication service layer.
Handles OTP generation, verification, and JWT token management.
"""
from datetime import timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.config import settings
from app.utils.security import create_access_token, generate_otp
from app.utils.timestamps import utcnow, is_expired
from app.users.models import User

logger = logging.getLogger(__name__)


# In-memory OTP storage for development (use Redis in production)
otp_storage = {}


class AuthService:
    """Service class for authentication operations."""
    
    @staticmethod
    def generate_and_send_otp(phone_number: str, db: Session) -> Tuple[str, int]:
        """
        Generate OTP and send to user's phone.
        
        Args:
            phone_number: User's phone number
            db: Database session
            
        Returns:
            Tuple[str, int]: OTP code and expiry minutes
            
        Raises:
            HTTPException: If OTP sending fails
        """
        # Generate OTP
        otp_code = generate_otp(settings.OTP_LENGTH)
        
        # Store OTP with timestamp (in production, use Redis with TTL)
        otp_storage[phone_number] = {
            "code": otp_code,
            "created_at": utcnow(),
            "verified": False
        }
        
        # Send OTP via SMS provider
        if settings.OTP_PROVIDER == "mock":
            logger.info(f"[MOCK] OTP for {phone_number}: {otp_code}")
        elif settings.OTP_PROVIDER == "kavenegar":
            # TODO: Implement Kavenegar SMS integration
            # Example:
            # api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
            # api.sms_send({
            #     'receptor': phone_number,
            #     'message': f'Your verification code: {otp_code}'
            # })
            logger.info(f"Sending OTP via Kavenegar to {phone_number}")
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OTP provider not configured"
            )
        
        return otp_code, settings.OTP_EXPIRY_MINUTES
    
    @staticmethod
    def verify_otp(phone_number: str, otp_code: str, db: Session) -> User:
        """
        Verify OTP and return user.
        
        Args:
            phone_number: User's phone number
            otp_code: OTP code to verify
            db: Database session
            
        Returns:
            User: Authenticated user
            
        Raises:
            HTTPException: If OTP is invalid or expired
        """
        # Check if OTP exists
        otp_data = otp_storage.get(phone_number)
        
        if not otp_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP not found. Please request a new OTP."
            )
        
        # Check if OTP is expired
        if is_expired(otp_data["created_at"], settings.OTP_EXPIRY_MINUTES):
            # Clean up expired OTP
            del otp_storage[phone_number]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired. Please request a new OTP."
            )
        
        # Verify OTP code
        if otp_data["code"] != otp_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP code."
            )
        
        # Mark OTP as verified
        otp_data["verified"] = True
        
        # Get or create user
        user = db.query(User).filter(User.phone_number == phone_number).first()
        
        if not user:
            # Create new user
            user = User(
                phone_number=phone_number,
                name=f"User_{phone_number[-4:]}",  # Default name
                study_level="intern",  # Default level
                created_at=utcnow()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created new user: {user.id} - {phone_number}")
        else:
            logger.info(f"Existing user logged in: {user.id} - {phone_number}")
        
        # Clean up OTP after successful verification
        del otp_storage[phone_number]
        
        return user
    
    @staticmethod
    def create_user_token(user_id: int) -> Tuple[str, int]:
        """
        Create JWT access token for user.
        
        Args:
            user_id: User ID
            
        Returns:
            Tuple[str, int]: Access token and expiry seconds
        """
        # Create token data
        token_data = {
            "sub": str(user_id),
            "type": "access"
        }
        
        # Create token with expiration
        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
        
        return access_token, expires_in
    
    @staticmethod
    def get_current_user(token: str, db: Session) -> User:
        """
        Get current user from JWT token.
        
        Args:
            token: JWT access token
            db: Database session
            
        Returns:
            User: Current authenticated user
            
        Raises:
            HTTPException: If token is invalid or user not found
        """
        from app.utils.security import decode_access_token
        
        # Decode token
        payload = decode_access_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user ID from token
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        user = db.query(User).filter(User.id == int(user_id)).first()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
