import pytest
from app import __init__ as app_module

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = app_module.create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home route '/'."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Expense Tracker API"}
