# app/__init__.py

from flask import Flask
from .database import init_db     # ✅ relative import
from .routes import expense_bp    # ✅ relative import

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    init_db(app)

    # Register routes (blueprint)
    app.register_blueprint(expense_bp)

    @app.route('/')
    def home():
        return {"message": "Welcome to the Expense Tracker API"}

    return app

# Only needed if running this file directly
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
