"""Utility functions for the application"""
import asyncio
import logging
from typing import Any, Dict, Optional
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format a datetime object as a human-readable string"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get a value from a dictionary"""
    try:
        return data.get(key, default)
    except (AttributeError, TypeError):
        return default


async def async_retry(func, max_retries: int = 3, delay: float = 1.0):
    """Retry an async function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Function failed after {max_retries} attempts: {e}")
                raise
            
            wait_time = delay * (2 ** attempt)
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
            await asyncio.sleep(wait_time)


def validate_email(email: str) -> bool:
    """Basic email validation"""
    if not email or not isinstance(email, str):
        return False
    return "@" in email and "." in email.split("@")[-1]


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input"""
    if not isinstance(text, str):
        return ""
    
    # Remove potentially dangerous characters
    sanitized = text.replace("<", "&lt;").replace(">", "&gt;")
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized.strip()