from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token
from flask_pydantic import validate
from pydantic import ValidationError
from werkzeug.security import check_password_hash

from app import db
from app.models import User

from .schemas import UserSchema

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
@validate()
def register(body: UserSchema):
    try:
        if User.query.filter_by(username=body.username).first():
            return jsonify({"msg": "User already exists"}), 409

        new_user = User(username=body.username)
        new_user.set_password(body.password)

        global db
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
