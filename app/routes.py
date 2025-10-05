from flask import Blueprint, request, jsonify
from app.models import Expense
from app.database import db
from models import Expense
from database import db

expense_bp = Blueprint('expense_bp', __name__)

# CREATE
@expense_bp.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(
        title=data['title'],
        amount=data['amount'],
        category=data['category'],
        date=data['date']
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully"}), 201

# READ
@expense_bp.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([e.to_dict() for e in expenses]), 200

# UPDATE
@expense_bp.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    data = request.get_json()
    expense.title = data.get('title', expense.title)
    expense.amount = data.get('amount', expense.amount)
    expense.category = data.get('category', expense.category)
    expense.date = data.get('date', expense.date)
    db.session.commit()
    return jsonify({"message": "Expense updated successfully"}), 200

# DELETE
@expense_bp.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully"}), 200

# HEALTH CHECK
@expense_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200