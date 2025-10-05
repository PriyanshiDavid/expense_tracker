import pytest
from app import create_app
from app.database import db as _db
from app.models import Expense

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # in-memory DB
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
    with app.app_context():
        _db.create_all()  # create tables
    yield app
    with app.app_context():
        _db.drop_all()  # clean up after tests

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_expense(client):
    response = client.post('/expenses', json={
        "title": "Lunch",
        "amount": 12.5,
        "category": "Food",
        "date": "2025-10-05"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Expense added successfully"

def test_get_expenses(client):
    # First, add an expense
    client.post('/expenses', json={
        "title": "Dinner",
        "amount": 20.0,
        "category": "Food",
        "date": "2025-10-05"
    })
    response = client.get('/expenses')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Dinner"

def test_update_expense(client):
    # Add expense
    resp = client.post('/expenses', json={
        "title": "Coffee",
        "amount": 5.0,
        "category": "Drink",
        "date": "2025-10-05"
    })
    # Update it
    response = client.put('/expenses/1', json={"amount": 6.0})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Expense updated successfully"
    # Verify update
    resp = client.get('/expenses')
    assert resp.get_json()[0]["amount"] == 6.0

def test_delete_expense(client):
    # Add expense
    client.post('/expenses', json={
        "title": "Snack",
        "amount": 3.0,
        "category": "Food",
        "date": "2025-10-05"
    })
    # Delete it
    response = client.delete('/expenses/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Expense deleted successfully"
    # Verify deletion
    resp = client.get('/expenses')
    assert resp.get_json() == []
