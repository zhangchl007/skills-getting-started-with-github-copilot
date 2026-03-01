import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture providing a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Fixture to reset activities state before each test"""
    # Store original state
    original_activities = {
        k: {
            "description": v["description"],
            "schedule": v["schedule"],
            "max_participants": v["max_participants"],
            "participants": v["participants"].copy()
        }
        for k, v in activities.items()
    }
    
    yield
    
    # Restore original state after test
    for activity_name, data in original_activities.items():
        activities[activity_name] = data.copy()
        activities[activity_name]["participants"] = data["participants"].copy()
