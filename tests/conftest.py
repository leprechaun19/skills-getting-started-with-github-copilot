import sys
from pathlib import Path
import pytest
from copy import deepcopy
from fastapi.testclient import TestClient

# Add src directory to path to import app module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Fixture providing TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Autouse fixture to reset activities to original state after each test"""
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
