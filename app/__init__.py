from flask import Flask
from .config import DATABASE_URL, JWT_SECRET_KEY
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_session import Session

db = SQLAlchemy()
jwt = JWTManager()
session = Session()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    # Use SQLAlchemy for session storage
    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["SESSION_SQLALCHEMY"] = db
    db.init_app(app)
    jwt.init_app(app)
    session.init_app(app)

    # Register blueprints
    from .controllers.user import user_controller_blueprint
    from .controllers.login import login_controller_blueprint

    app.register_blueprint(login_controller_blueprint, url_prefix='/auth')
    app.register_blueprint(user_controller_blueprint, url_prefix='/user')

    # Create tables
    with app.app_context():
        db.create_all()

    return app
