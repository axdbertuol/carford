from flask import Blueprint, jsonify
from pydantic import ValidationError
from .models import Owner, Car, db
from .schemas import CarSchemaOut, OwnerSchemaIn, CarSchemaIn, OwnerSchemaOut
from flask_jwt_extended import jwt_required
from flask_pydantic import validate

main = Blueprint("main", __name__)

"""
Owners routes
"""


@main.route("/owners", methods=["POST"])
@jwt_required()
@validate(on_success_status=201)
def add_owner(body: OwnerSchemaIn):
    try:
        owner = Owner(name=body.name)
        db.session.add(owner)
        db.session.commit()
        return OwnerSchemaOut.model_validate(owner)
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500


@main.route("/owners", methods=["GET"])
@jwt_required()
@validate(on_success_status=200)
def get_all_owners():
    try:
        owners = Owner.query.all()
        owners_data = [
            OwnerSchemaOut.model_validate(owner).model_dump_json() for owner in owners
        ]
        return jsonify({"data": owners_data})
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500


@main.route("/owners/<int:owner_id>", methods=["PUT"])
@jwt_required()
@validate(on_success_status=200)
def update_owner(owner_id: int, body: OwnerSchemaIn):
    try:
        owner = Owner.query.get(owner_id)

        if not owner:
            return jsonify({"msg": "Owner not found"}), 404

        owner.name = body.name
        db.session.commit()

        return OwnerSchemaOut.model_validate(owner)
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500


@main.route("/owners/<int:owner_id>", methods=["DELETE"])
@jwt_required()
@validate()
def delete_owner(owner_id: int):
    try:
        owner = Owner.query.get(owner_id)

        if not owner:
            return jsonify({"msg": "Owner not found"}), 404

        db.session.delete(owner)
        db.session.commit()

        return jsonify({"msg": "Owner deleted!"}), 200
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500


"""
Cars routes
"""


@main.route("/cars", methods=["POST"])
@jwt_required()
@validate(on_success_status=201)
def add_car(body: CarSchemaIn):
    try:
        car = Car(owner_id=body.owner_id, color=body.color, model=body.model)
        db.session.add(car)
        db.session.commit()
        return CarSchemaOut.model_validate(car)
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500


@main.route("/cars", methods=["GET"])
@jwt_required()
@validate(on_success_status=200)
def get_all_cars():
    try:
        cars = Car.query.all()
        response = [CarSchemaOut.model_validate(car).model_dump_json() for car in cars]
        return jsonify({"data": response})
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500


@main.route("/cars/<int:car_id>", methods=["PUT"])
@jwt_required()
@validate(on_success_status=200)
def update_car(car_id: int, body: CarSchemaIn):
    try:
        car = Car.query.get(car_id)

        if not car:
            return jsonify({"msg": "Car not found"}), 404

        car.owner_id = body.owner_id
        car.color = body.color
        car.model = body.model
        db.session.commit()

        return CarSchemaOut.model_validate(car)
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500


@main.route("/cars/<int:car_id>", methods=["DELETE"])
@jwt_required()
@validate()
def delete_car(car_id: int):
    try:
        car = Car.query.get(car_id)

        if not car:
            return jsonify({"msg": "Car not found"}), 404

        db.session.delete(car)
        db.session.commit()

        return jsonify({"msg": "Car deleted!"}), 200
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500
