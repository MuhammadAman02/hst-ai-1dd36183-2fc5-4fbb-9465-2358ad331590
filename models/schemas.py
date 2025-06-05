"""Pydantic models for data validation"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserProfile(BaseModel):
    """User profile data model"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class ApiResponse(BaseModel):
    """Standard API response model"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ChartData(BaseModel):
    """Chart data model"""
    labels: List[str]
    values: List[float]
    chart_type: str = "line"
    title: Optional[str] = None
    
    @validator('values')
    def validate_values(cls, v):
        if not v:
            raise ValueError('Values cannot be empty')
        return v


class FormData(BaseModel):
    """Generic form data model"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    confirm_password: Optional[str] = None
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class FileUpload(BaseModel):
    """File upload model"""
    filename: str
    content_type: str
    size: int = Field(..., gt=0, le=10_000_000)  # Max 10MB
    
    @validator('filename')
    def validate_filename(cls, v):
        if not v or '/' in v or '\\' in v:
            raise ValueError('Invalid filename')
        return v


class AppSettings(BaseModel):
    """Application settings model"""
    theme: str = "blue"
    notifications_enabled: bool = True
    language: str = "en"
    timezone: str = "UTC"
    
    @validator('theme')
    def validate_theme(cls, v):
        allowed_themes = ["blue", "green", "purple", "orange", "red"]
        if v not in allowed_themes:
            raise ValueError(f'Theme must be one of {allowed_themes}')
        return v


class HealthCheck(BaseModel):
    """Health check response model"""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"
    uptime: Optional[float] = None