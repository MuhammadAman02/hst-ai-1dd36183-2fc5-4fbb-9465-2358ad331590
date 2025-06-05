"""Business logic services"""
import asyncio
import httpx
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

from models.schemas import ApiResponse, ChartData, UserProfile, HealthCheck
from core.utils import async_retry, safe_get

logger = logging.getLogger(__name__)


class DataService:
    """Service for handling data operations"""
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.cache_ttl: Dict[str, datetime] = {}
    
    async def get_sample_data(self, count: int = 10) -> ChartData:
        """Generate sample chart data"""
        labels = [f"Point {i+1}" for i in range(count)]
        values = [random.uniform(10, 100) for _ in range(count)]
        
        return ChartData(
            labels=labels,
            values=values,
            chart_type="line",
            title="Sample Data Chart"
        )
    
    async def get_cached_data(self, key: str, ttl_seconds: int = 300) -> Optional[Any]:
        """Get data from cache with TTL"""
        if key in self.cache:
            if key in self.cache_ttl:
                if datetime.now() < self.cache_ttl[key]:
                    return self.cache[key]
                else:
                    # Cache expired
                    del self.cache[key]
                    del self.cache_ttl[key]
        return None
    
    def set_cached_data(self, key: str, data: Any, ttl_seconds: int = 300):
        """Set data in cache with TTL"""
        self.cache[key] = data
        self.cache_ttl[key] = datetime.now() + timedelta(seconds=ttl_seconds)


class ApiService:
    """Service for external API interactions"""
    
    def __init__(self):
        self.client = None
        self.base_timeout = 10.0
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=self.base_timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    async def test_connection(self) -> ApiResponse:
        """Test external API connection"""
        try:
            async def make_request():
                if not self.client:
                    raise RuntimeError("Client not initialized")
                
                response = await self.client.get("https://httpbin.org/json")
                response.raise_for_status()
                return response.json()
            
            data = await async_retry(make_request, max_retries=3, delay=1.0)
            
            return ApiResponse(
                success=True,
                message="API connection successful",
                data=data
            )
        
        except Exception as e:
            logger.error(f"API connection failed: {e}")
            return ApiResponse(
                success=False,
                message=f"API connection failed: {str(e)}"
            )
    
    async def fetch_external_data(self, url: str) -> ApiResponse:
        """Fetch data from external URL"""
        try:
            if not self.client:
                raise RuntimeError("Client not initialized")
            
            response = await self.client.get(url)
            response.raise_for_status()
            
            return ApiResponse(
                success=True,
                message="Data fetched successfully",
                data=response.json()
            )
        
        except Exception as e:
            logger.error(f"Failed to fetch data from {url}: {e}")
            return ApiResponse(
                success=False,
                message=f"Failed to fetch data: {str(e)}"
            )


class UserService:
    """Service for user management"""
    
    def __init__(self):
        self.users: Dict[str, UserProfile] = {}
    
    def create_user(self, name: str, email: str) -> UserProfile:
        """Create a new user profile"""
        user = UserProfile(name=name, email=email)
        self.users[email] = user
        return user
    
    def get_user(self, email: str) -> Optional[UserProfile]:
        """Get user by email"""
        return self.users.get(email)
    
    def update_user(self, email: str, **kwargs) -> Optional[UserProfile]:
        """Update user profile"""
        if email in self.users:
            user_data = self.users[email].dict()
            user_data.update(kwargs)
            self.users[email] = UserProfile(**user_data)
            return self.users[email]
        return None
    
    def list_users(self) -> List[UserProfile]:
        """List all users"""
        return list(self.users.values())


class HealthService:
    """Service for health monitoring"""
    
    def __init__(self):
        self.start_time = datetime.now()
    
    def get_health_status(self) -> HealthCheck:
        """Get current health status"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return HealthCheck(
            status="healthy",
            uptime=uptime
        )
    
    async def check_dependencies(self) -> Dict[str, bool]:
        """Check health of external dependencies"""
        checks = {}
        
        # Check external API
        try:
            async with ApiService() as api_service:
                result = await api_service.test_connection()
                checks["external_api"] = result.success
        except Exception:
            checks["external_api"] = False
        
        # Add more dependency checks as needed
        checks["memory"] = True  # Placeholder
        checks["disk"] = True   # Placeholder
        
        return checks


# Global service instances
data_service = DataService()
user_service = UserService()
health_service = HealthService()