import json
from app import create_app
from app.database import db

def setup_module(module):
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    module.client = app.test_client()

    with app.app_context():
        db.create_all()

def test_add_expense():
    data = {
        "title": "Lunch",
        "amount": 12.5,
        "category": "Food",
        "date": "2025-10-05"
    }
    response = client.post('/expenses', json=data)
    assert response.status_code == 201

def test_get_expenses():
    response = client.get('/expenses')
    assert response.status_code == 200