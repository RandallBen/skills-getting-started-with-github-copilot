"""Fixtures and configuration for pytest"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


# Store original activities state for resetting between tests
ORIGINAL_ACTIVITIES = None


@pytest.fixture(scope="function", autouse=True)
def reset_activities():
    """Reset the in-memory activities database before each test.
    
    This fixture automatically runs before every test to ensure a clean state.
    """
    global ORIGINAL_ACTIVITIES
    
    # Store original state on first run
    if ORIGINAL_ACTIVITIES is None:
        import copy
        ORIGINAL_ACTIVITIES = copy.deepcopy(activities)
    
    # Reset activities to original state
    activities.clear()
    import copy
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    
    yield


@pytest.fixture(scope="function")
def client():
    """Provide a FastAPI TestClient for making requests to the app.
    
    This fixture creates a fresh client for each test.
    """
    return TestClient(app)


# Test data fixtures for common scenarios
@pytest.fixture(scope="function")
def valid_activity_name():
    """Return a valid activity name from the database."""
    return "Chess Club"


@pytest.fixture(scope="function")
def valid_email():
    """Return a valid email that is NOT pre-registered."""
    return "newstudent@mergington.edu"


@pytest.fixture(scope="function")
def registered_email():
    """Return an email that IS already registered for an activity."""
    return "michael@mergington.edu"  # Pre-registered in Chess Club


@pytest.fixture(scope="function")
def invalid_activity_name():
    """Return an activity name that does not exist."""
    return "NonExistentClub"


@pytest.fixture(scope="function")
def invalid_email():
    """Return an invalid email format."""
    return "not-an-email"


@pytest.fixture(scope="function")
def full_activity_name():
    """Return an activity that can be filled to max capacity.
    
    We'll manage this in individual tests.
    """
    return "Programming Class"
