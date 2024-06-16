from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()


def create_app(start_db: bool = True):
    app = Flask(__name__)
    if start_db:
        from app.config import Config

        app.config.from_object(Config)

        db.init_app(app)
        migrate.init_app(app, db)
    jwt.init_app(app)

    from app.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app
