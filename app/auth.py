from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token
from flask_pydantic import validate
from pydantic import ValidationError
from werkzeug.security import check_password_hash

from app import db

from .models import User
from .schemas import UserSchema

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
@validate()
def register(body: UserSchema):
    """
    Registers a new user.

    This endpoint takes a JSON body containing a username and password,
    checks if the user already exists, and if not, creates a new user
    with the provided username and password.

    :param body: The UserSchema containing the username and password.
    :return: A JSON response with a success or error message.
    """
    try:
        if db.session.query(User).filter_by(username=body.username).first():
            return jsonify({"msg": "User already exists"}), 409

        new_user = User(username=body.username)
        new_user.set_password(body.password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered!"}), 201
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500


@auth.route("/login", methods=["POST"])
@validate()
def login(body: UserSchema):
    """
    Authenticates a user and generates a JWT token.

    This endpoint takes a JSON body containing a username and password,
    validates the credentials, and if valid, returns a JWT token.

    :param body: The UserSchema containing the username and password.
    :return: A JSON response with the JWT token or an error message.
    """
    try:
        user: User | None = (
            db.session.query(User).filter_by(username=body.username).first()
        )
        if user is None:
            return jsonify({"msg": "Wrong credentials"}), 409
        if check_password_hash(user.password_hash, body.password) is False:
            return jsonify({"msg": "Wrong credentials"}), 409

        access_token = create_access_token(identity=user.username)

        return jsonify(access_token=access_token), 200
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500
