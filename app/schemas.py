import string
from typing import List

from flask_pydantic.exceptions import JsonBodyParsingError
from pydantic import BaseModel, ConfigDict, Field, field_validator


class OwnerSchemaIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    model_config = ConfigDict(from_attributes=True)


class OwnerSchemaOut(BaseModel):
    id: int
    name: str
    cars: List["CarSchemaOut"]
    model_config = ConfigDict(from_attributes=True)


class CarSchemaIn(BaseModel):
    owner_id: int
    color: str = Field(pattern="^(yellow|blue|gray)$")
    model: str = Field(pattern="^(hatch|sedan|convertible)$")

    @field_validator("owner_id")
    def validate_owner_id(cls, value):
        if value <= 0:
            raise JsonBodyParsingError("Owner ID must be a positive integer")
        return value

    model_config = ConfigDict(from_attributes=True)


class CarSchemaOut(BaseModel):
    id: int
    owner_id: int
    color: str
    model: str

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(
        min_length=8,
        max_length=50,
        # Contains at least one upper case letter, one lower case letter, one number and one special character
    )

    @field_validator("password")
    def validate_password(cls, value):
        if (
            not any(c.isupper() for c in value)
            or not any(c.islower() for c in value)
            or not any(c.isdigit() for c in value)
            or not any(c in string.punctuation for c in value)
        ):
            raise JsonBodyParsingError(
                "Password must contains at least one upper case letter, one lower case letter, one number and one special character"
            )
        return value

    model_config = ConfigDict(from_attributes=True)
