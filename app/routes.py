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
    """
    Add a new owner.

    This endpoint creates a new owner with the provided name.

    :param body: The OwnerSchemaIn containing the owner's name.
    :return: A JSON response with the created owner's details or an error message.
    """
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
    """
    Retrieve all owners.

    This endpoint retrieves all owners from the database.

    :return: A JSON response with a list of all owners or an error message.
    """
    try:
        owners = db.session.query(Owner).all()
        owners_data = [
            OwnerSchemaOut.model_validate(owner).model_dump() for owner in owners
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
    """
    Update an existing owner.

    This endpoint updates the details of an existing owner based on the provided owner ID.

    :param owner_id: The ID of the owner to update.
    :param body: The OwnerSchemaIn containing the updated owner's name.
    :return: A JSON response with the updated owner's details or an error message.
    """
    try:
        owner = db.session.query(Owner).get(owner_id)

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
    """
    Delete an owner.

    This endpoint deletes an owner based on the provided owner ID.

    :param owner_id: The ID of the owner to delete.
    :return: A JSON response with a success message or an error message.
    """
    try:
        owner = db.session.query(Owner).get(owner_id)

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
    """
    Add a new car.

    This endpoint creates a new car with the provided owner ID, color, and model.

    :param body: The CarSchemaIn containing the car's details.
    :return: A JSON response with the created car's details or an error message.
    """
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
    """
    Retrieve all cars.

    This endpoint retrieves all cars from the database.

    :return: A JSON response with a list of all cars or an error message.
    """
    try:
        cars = db.session.query(Car).all()
        response = [CarSchemaOut.model_validate(car).model_dump() for car in cars]
        return jsonify({"data": response})
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500


@main.route("/cars/<int:car_id>", methods=["PUT"])
@jwt_required()
@validate(on_success_status=200)
def update_car(car_id: int, body: CarSchemaIn):
    """
    Update an existing car.

    This endpoint updates the details of an existing car based on the provided car ID.

    :param car_id: The ID of the car to update.
    :param body: The CarSchemaIn containing the updated car's details.
    :return: A JSON response with the updated car's details or an error message.
    """
    try:
        car = db.session.query(Car).get(car_id)

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
    """
    Delete a car.

    This endpoint deletes a car based on the provided car ID.

    :param car_id: The ID of the car to delete.
    :return: A JSON response with a success message or an error message.
    """
    try:
        car = db.session.query(Car).get(car_id)

        if not car:
            return jsonify({"msg": "Car not found"}), 404

        db.session.delete(car)
        db.session.commit()

        return jsonify({"msg": "Car deleted!"}), 200
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500
