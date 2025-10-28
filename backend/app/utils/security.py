"""
Security utilities for authentication and authorization.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import secrets
import string

from app.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary of data to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        str: Encoded JWT token
        
    Example:
        token = create_access_token({"sub": user_id})
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT access token.
    
    Args:
        token: JWT token string
        
    Returns:
        Optional[Dict]: Decoded token data or None if invalid
        
    Example:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def generate_otp(length: int = 6) -> str:
    """
    Generate a random OTP code.
    
    Args:
        length: Length of OTP (default: 6)
        
    Returns:
        str: Random numeric OTP code
        
    Example:
        otp = generate_otp()  # Returns something like "123456"
    """
    digits = string.digits
    return ''.join(secrets.choice(digits) for _ in range(length))


def generate_random_string(length: int = 32) -> str:
    """
    Generate a random alphanumeric string.
    
    Args:
        length: Length of string (default: 32)
        
    Returns:
        str: Random string
        
    Example:
        job_id = generate_random_string(16)
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# FastAPI Security
security = HTTPBearer()


def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Extract and validate user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials from request header
        
    Returns:
        Dict: Decoded token payload with user info
        
    Raises:
        HTTPException: If token is invalid or expired
        
    Example:
        @app.get("/protected")
        def protected_route(user = Depends(get_current_user_from_token)):
            return {"user_id": user["sub"], "role": user["role"]}
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload


def require_role(allowed_roles: List[str]):
    """
    Dependency factory for role-based access control.
    
    Args:
        allowed_roles: List of role names that are allowed access
        
    Returns:
        Dependency function that checks user role
        
    Raises:
        HTTPException: If user doesn't have required role
        
    Example:
        @app.post("/content/upload-pdf")
        def upload_pdf(user = Depends(require_role(["faculty", "admin"]))):
            # Only faculty and admin can access this endpoint
            pass
    """
    def role_checker(user: Dict[str, Any] = Depends(get_current_user_from_token)) -> Dict[str, Any]:
        user_role = user.get("role", "student")
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        
        return user
    
    return role_checker


def get_current_user_id(user: Dict[str, Any] = Depends(get_current_user_from_token)) -> int:
    """
    Extract user ID from token.
    
    Args:
        user: User payload from token
        
    Returns:
        int: User ID
        
    Example:
        @app.get("/profile")
        def get_profile(user_id: int = Depends(get_current_user_id)):
            return {"user_id": user_id}
    """
    user_id = user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )
    
    return int(user_id)
