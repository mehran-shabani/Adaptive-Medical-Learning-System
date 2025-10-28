"""
Timestamp utilities for date and time operations.
"""

from datetime import datetime, timedelta

import pytz


def utcnow() -> datetime:
    """
    Get current UTC datetime.

    Returns:
        datetime: Current UTC datetime
    """
    return datetime.utcnow()


def format_datetime(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime to string.

    Args:
        dt: Datetime object
        format_string: Format string (default: "%Y-%m-%d %H:%M:%S")

    Returns:
        str: Formatted datetime string
    """
    return dt.strftime(format_string)


def parse_datetime(date_string: str, format_string: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Parse string to datetime.

    Args:
        date_string: Date string
        format_string: Format string (default: "%Y-%m-%d %H:%M:%S")

    Returns:
        datetime: Parsed datetime object
    """
    return datetime.strptime(date_string, format_string)


def days_ago(days: int) -> datetime:
    """
    Get datetime N days ago from now.

    Args:
        days: Number of days

    Returns:
        datetime: Datetime N days ago

    Example:
        last_week = days_ago(7)
    """
    return utcnow() - timedelta(days=days)


def hours_ago(hours: int) -> datetime:
    """
    Get datetime N hours ago from now.

    Args:
        hours: Number of hours

    Returns:
        datetime: Datetime N hours ago
    """
    return utcnow() - timedelta(hours=hours)


def days_since(dt: datetime) -> int:
    """
    Calculate number of days since given datetime.

    Args:
        dt: Past datetime

    Returns:
        int: Number of days since dt

    Example:
        days = days_since(user.last_login)
    """
    return (utcnow() - dt).days


def is_expired(dt: datetime, expiry_minutes: int) -> bool:
    """
    Check if datetime has expired.

    Args:
        dt: Datetime to check
        expiry_minutes: Expiry duration in minutes

    Returns:
        bool: True if expired, False otherwise

    Example:
        if is_expired(otp.created_at, 5):
            raise ValueError("OTP expired")
    """
    expiry_time = dt + timedelta(minutes=expiry_minutes)
    return utcnow() > expiry_time


def to_timezone(dt: datetime, timezone: str = "Asia/Tehran") -> datetime:
    """
    Convert UTC datetime to specific timezone.

    Args:
        dt: UTC datetime
        timezone: Target timezone (default: "Asia/Tehran")

    Returns:
        datetime: Datetime in target timezone
    """
    utc = pytz.utc
    target_tz = pytz.timezone(timezone)
    utc_dt = utc.localize(dt) if dt.tzinfo is None else dt
    return utc_dt.astimezone(target_tz)
