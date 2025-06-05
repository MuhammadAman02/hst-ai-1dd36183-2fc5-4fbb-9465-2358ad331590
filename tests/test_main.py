"""Tests for the main application functionality"""
import pytest
from unittest.mock import AsyncMock, patch
import asyncio

from models.schemas import UserProfile, ApiResponse, ChartData
from services.business import DataService, ApiService, UserService, HealthService
from core.utils import validate_email, sanitize_input, format_timestamp


class TestDataService:
    """Test cases for DataService"""
    
    @pytest.fixture
    def data_service(self):
        return DataService()
    
    @pytest.mark.asyncio
    async def test_get_sample_data(self, data_service):
        """Test sample data generation"""
        result = await data_service.get_sample_data(count=5)
        
        assert isinstance(result, ChartData)
        assert len(result.labels) == 5
        assert len(result.values) == 5
        assert result.chart_type == "line"
        assert result.title == "Sample Data Chart"
    
    def test_cache_operations(self, data_service):
        """Test cache set and get operations"""
        # Test setting and getting cache
        test_data = {"key": "value"}
        data_service.set_cached_data("test_key", test_data, ttl_seconds=60)
        
        cached_result = asyncio.run(data_service.get_cached_data("test_key"))
        assert cached_result == test_data
        
        # Test cache miss
        missing_result = asyncio.run(data_service.get_cached_data("missing_key"))
        assert missing_result is None


class TestUserService:
    """Test cases for UserService"""
    
    @pytest.fixture
    def user_service(self):
        return UserService()
    
    def test_create_user(self, user_service):
        """Test user creation"""
        user = user_service.create_user("John Doe", "john@example.com")
        
        assert isinstance(user, UserProfile)
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.is_active is True
    
    def test_get_user(self, user_service):
        """Test user retrieval"""
        # Create a user first
        user_service.create_user("Jane Doe", "jane@example.com")
        
        # Test getting existing user
        user = user_service.get_user("jane@example.com")
        assert user is not None
        assert user.name == "Jane Doe"
        
        # Test getting non-existent user
        missing_user = user_service.get_user("missing@example.com")
        assert missing_user is None
    
    def test_update_user(self, user_service):
        """Test user update"""
        # Create a user first
        user_service.create_user("Bob Smith", "bob@example.com")
        
        # Update the user
        updated_user = user_service.update_user("bob@example.com", name="Robert Smith")
        assert updated_user is not None
        assert updated_user.name == "Robert Smith"
        
        # Test updating non-existent user
        result = user_service.update_user("missing@example.com", name="New Name")
        assert result is None


class TestHealthService:
    """Test cases for HealthService"""
    
    @pytest.fixture
    def health_service(self):
        return HealthService()
    
    def test_get_health_status(self, health_service):
        """Test health status retrieval"""
        status = health_service.get_health_status()
        
        assert status.status == "healthy"
        assert status.uptime is not None
        assert status.uptime >= 0
    
    @pytest.mark.asyncio
    async def test_check_dependencies(self, health_service):
        """Test dependency health checks"""
        with patch('services.business.ApiService') as mock_api_service:
            # Mock successful API service
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_instance.test_connection.return_value = ApiResponse(
                success=True, 
                message="Success"
            )
            mock_api_service.return_value = mock_instance
            
            checks = await health_service.check_dependencies()
            
            assert "external_api" in checks
            assert "memory" in checks
            assert "disk" in checks
            assert checks["memory"] is True
            assert checks["disk"] is True


class TestUtilityFunctions:
    """Test cases for utility functions"""
    
    def test_validate_email(self):
        """Test email validation"""
        # Valid emails
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@domain.co.uk") is True
        
        # Invalid emails
        assert validate_email("invalid-email") is False
        assert validate_email("@example.com") is False
        assert validate_email("test@") is False
        assert validate_email("") is False
        assert validate_email(None) is False
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        # Test HTML escaping
        result = sanitize_input("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result
        
        # Test length limiting
        long_text = "a" * 1500
        result = sanitize_input(long_text, max_length=1000)
        assert len(result) <= 1003  # 1000 + "..."
        assert result.endswith("...")
        
        # Test whitespace trimming
        result = sanitize_input("  test  ")
        assert result == "test"
        
        # Test non-string input
        result = sanitize_input(123)
        assert result == ""
    
    def test_format_timestamp(self):
        """Test timestamp formatting"""
        from datetime import datetime
        
        # Test with specific datetime
        dt = datetime(2023, 12, 25, 15, 30, 45)
        result = format_timestamp(dt)
        assert result == "2023-12-25 15:30:45"
        
        # Test with None (current time)
        result = format_timestamp(None)
        assert len(result) == 19  # YYYY-MM-DD HH:MM:SS format
        assert "-" in result
        assert ":" in result


class TestPydanticModels:
    """Test cases for Pydantic models"""
    
    def test_user_profile_validation(self):
        """Test UserProfile model validation"""
        # Valid user profile
        user = UserProfile(name="John Doe", email="john@example.com")
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.is_active is True
        
        # Test name validation (empty name)
        with pytest.raises(ValueError):
            UserProfile(name="", email="john@example.com")
        
        # Test name trimming
        user = UserProfile(name="  John Doe  ", email="john@example.com")
        assert user.name == "John Doe"
    
    def test_api_response_model(self):
        """Test ApiResponse model"""
        response = ApiResponse(success=True, message="Test message")
        assert response.success is True
        assert response.message == "Test message"
        assert response.data is None
        assert response.timestamp is not None
        
        # Test with data
        response = ApiResponse(
            success=True, 
            message="Success", 
            data={"key": "value"}
        )
        assert response.data == {"key": "value"}
    
    def test_chart_data_validation(self):
        """Test ChartData model validation"""
        # Valid chart data
        chart = ChartData(
            labels=["A", "B", "C"],
            values=[1.0, 2.0, 3.0],
            chart_type="bar",
            title="Test Chart"
        )
        assert len(chart.labels) == 3
        assert len(chart.values) == 3
        assert chart.chart_type == "bar"
        
        # Test empty values validation
        with pytest.raises(ValueError):
            ChartData(labels=["A"], values=[])


# Pytest configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


if __name__ == "__main__":
    pytest.main([__file__])