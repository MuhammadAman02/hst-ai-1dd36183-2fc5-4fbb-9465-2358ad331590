"""Pytest configuration and shared fixtures"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
import tempfile
import os

from services.business import DataService, UserService, HealthService, ApiService


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing"""
    original_env = os.environ.copy()
    test_env = {
        "PORT": "8000",
        "HOST": "0.0.0.0",
        "DEBUG": "true",
        "APP_NAME": "Test App",
        "APP_VERSION": "1.0.0-test"
    }
    
    os.environ.update(test_env)
    yield test_env
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "role": "user",
        "is_active": True
    }


@pytest.fixture
def sample_chart_data():
    """Sample chart data for testing"""
    return {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
        "values": [10.5, 20.3, 15.7, 25.1, 18.9],
        "chart_type": "line",
        "title": "Monthly Sales"
    }


@pytest.fixture
def mock_api_service():
    """Mock API service for testing"""
    service = AsyncMock(spec=ApiService)
    service.__aenter__.return_value = service
    service.__aexit__.return_value = None
    return service


@pytest.fixture
def mock_data_service():
    """Mock data service for testing"""
    service = MagicMock(spec=DataService)
    service.cache = {}
    service.cache_ttl = {}
    return service


@pytest.fixture
def mock_user_service():
    """Mock user service for testing"""
    service = MagicMock(spec=UserService)
    service.users = {}
    return service


@pytest.fixture
def mock_health_service():
    """Mock health service for testing"""
    service = MagicMock(spec=HealthService)
    return service


@pytest.fixture
def sample_api_response():
    """Sample API response data"""
    return {
        "success": True,
        "message": "Operation successful",
        "data": {
            "id": 123,
            "name": "Test Item",
            "created_at": "2023-12-25T10:00:00Z"
        }
    }


@pytest.fixture
def sample_error_response():
    """Sample error response data"""
    return {
        "success": False,
        "message": "Operation failed",
        "error_details": "Invalid input parameters",
        "error_type": "validation"
    }


# Async test helpers
@pytest.fixture
def async_test_client():
    """Create an async test client for API testing"""
    # This would typically use httpx.AsyncClient or similar
    # For now, we'll use a mock
    client = AsyncMock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.put = AsyncMock()
    client.delete = AsyncMock()
    return client


# Database fixtures (if needed in the future)
@pytest.fixture
def mock_database():
    """Mock database connection for testing"""
    db = MagicMock()
    db.execute = AsyncMock()
    db.fetch = AsyncMock()
    db.fetchrow = AsyncMock()
    db.fetchval = AsyncMock()
    return db


# Configuration for pytest
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Add 'unit' marker to all tests by default
        if not any(marker.name in ['integration', 'slow'] for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)
        
        # Add 'slow' marker to tests that might be slow
        if 'api' in item.name.lower() or 'integration' in item.name.lower():
            item.add_marker(pytest.mark.slow)


# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup after each test"""
    yield
    # Perform any necessary cleanup here
    # For example, clearing global state, closing connections, etc.
    pass