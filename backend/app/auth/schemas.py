"""
Pydantic schemas for authentication endpoints.
"""

import re

from pydantic import BaseModel, Field, validator


class OTPRequest(BaseModel):
    """Request schema for OTP generation."""

    phone_number: str = Field(..., description="User's mobile phone number", example="09123456789")

    @validator("phone_number")
    def validate_phone_number(cls, v):
        """Validate Iranian phone number format."""
        # Remove any spaces or special characters
        v = re.sub(r"[^\d+]", "", v)

        # Check Iranian mobile format: 09xxxxxxxxx or +989xxxxxxxxx
        if not (re.match(r"^09\d{9}$", v) or re.match(r"^\+989\d{9}$", v)):
            raise ValueError("Invalid Iranian phone number format")

        return v


class OTPVerify(BaseModel):
    """Request schema for OTP verification."""

    phone_number: str = Field(..., description="User's mobile phone number", example="09123456789")

    otp_code: str = Field(..., description="OTP code sent to user", min_length=6, max_length=6, example="123456")


class TokenResponse(BaseModel):
    """Response schema for successful authentication."""

    access_token: str = Field(..., description="JWT access token")

    token_type: str = Field(default="bearer", description="Token type")

    user_id: int = Field(..., description="User ID")

    role: str = Field(..., description="User role (student, faculty, admin)")

    expires_in: int = Field(..., description="Token expiration time in seconds")


class OTPResponse(BaseModel):
    """Response schema for OTP request."""

    message: str = Field(..., description="Success message")

    phone_number: str = Field(..., description="Phone number where OTP was sent")

    expires_in_minutes: int = Field(..., description="OTP expiration time in minutes")

    # Only include in development/debug mode
    otp_code: str | None = Field(None, description="OTP code (only in development mode)")
