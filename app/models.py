from typing import List

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, validates
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class Owner(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    sale_opportunity: Mapped[bool] = mapped_column(db.Boolean, default=True)
    cars: Mapped[List["Car"]] = db.relationship("Car", backref="owner", lazy=True)

    @hybrid_property
    def car_count(self):
        return len(self.cars)

    @validates("cars")
    def validate_cars(self, key, cars):
        if len(cars) > 3:
            raise ValueError("An owner cannot have more than 3 cars")
        return cars


class Car(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("owner.id"), nullable=False
    )

    color: Mapped[str] = mapped_column(
        db.Enum("yellow", "blue", "gray", name="car_color"), nullable=False
    )
    model: Mapped[str] = mapped_column(
        db.Enum("hatch", "sedan", "convertible", name="car_model"), nullable=False
    )

    @validates("owner_id")
    def validate_owner_id(self, key, owner_id):
        if self.query.filter_by(owner_id=owner_id).count() >= 3:
            raise ValueError("An owner cannot have more than 3 cars")
        return owner_id


class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    username: Mapped[str] = mapped_column(db.String(30), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=10)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
