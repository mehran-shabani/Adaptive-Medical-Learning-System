"""
Authentication API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import OTPRequest, OTPResponse, OTPVerify, TokenResponse
from app.auth.service import AuthService
from app.config import settings
from app.db import get_db

router = APIRouter()


@router.post("/login-otp", response_model=OTPResponse)
async def request_otp(request: OTPRequest, db: Session = Depends(get_db)):
    """
    Request OTP for phone number.

    This endpoint generates and sends an OTP code to the provided phone number.
    The OTP is valid for a limited time (default: 5 minutes).

    Args:
        request: OTP request with phone number
        db: Database session

    Returns:
        OTPResponse: Success message with OTP details

    Example:
        POST /auth/login-otp
        {
            "phone_number": "09123456789"
        }
    """
    otp_code, expiry_minutes = AuthService.generate_and_send_otp(phone_number=request.phone_number, db=db)

    response = OTPResponse(
        message="OTP sent successfully", phone_number=request.phone_number, expires_in_minutes=expiry_minutes
    )

    # Include OTP in response only in development mode
    if settings.DEBUG and settings.OTP_PROVIDER == "mock":
        response.otp_code = otp_code

    return response


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(request: OTPVerify, db: Session = Depends(get_db)):
    """
    Verify OTP and get JWT access token.

    This endpoint verifies the OTP code and returns a JWT access token
    that can be used for authenticated requests.

    Args:
        request: OTP verification request with phone number and code
        db: Database session

    Returns:
        TokenResponse: JWT access token and user information

    Raises:
        HTTPException: If OTP is invalid or expired

    Example:
        POST /auth/verify-otp
        {
            "phone_number": "09123456789",
            "otp_code": "123456"
        }
    """
    # Verify OTP and get user
    user = AuthService.verify_otp(phone_number=request.phone_number, otp_code=request.otp_code, db=db)

    # Create access token with role information
    access_token, expires_in = AuthService.create_user_token(user)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        role=user.role.value if hasattr(user.role, "value") else user.role,
        expires_in=expires_in,
    )


@router.get("/me")
async def get_current_user_info(
    db: Session = Depends(get_db),  # noqa: ARG001
    # TODO: Add authentication dependency
    # current_user: User = Depends(get_current_user_dependency)
):
    """
    Get current authenticated user information.

    Requires: Bearer token in Authorization header

    Returns:
        dict: Current user information

    Example:
        GET /auth/me
        Authorization: Bearer <token>
    """
    # TODO: Implement after creating dependency
    return {"message": "This endpoint requires authentication", "note": "Use Bearer token in Authorization header"}
