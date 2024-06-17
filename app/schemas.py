import string
from typing import List
from flask_pydantic.exceptions import JsonBodyParsingError
from pydantic import BaseModel, ConfigDict, Field, field_validator


class OwnerSchemaIn(BaseModel):
    """
    Schema for input validation of owner data.

    Attributes:
        name (str): The name of the owner, must be between 1 and 100 characters.
    """

    name: str = Field(min_length=1, max_length=100)

    model_config = ConfigDict(from_attributes=True)


class OwnerSchemaOut(BaseModel):
    """
    Schema for output representation of owner data.

    Attributes:
        id (int): The ID of the owner.
        name (str): The name of the owner.
        cars (List["CarSchemaOut"]): A list of cars owned by the owner.
    """

    id: int
    name: str
    cars: List["CarSchemaOut"]

    model_config = ConfigDict(from_attributes=True)


class CarSchemaIn(BaseModel):
    """
    Schema for input validation of car data.

    Attributes:
        owner_id (int): The ID of the owner, must be a positive integer.
        color (str): The color of the car, must be one of 'yellow', 'blue', or 'gray'.
        model (str): The model of the car, must be one of 'hatch', 'sedan', or 'convertible'.
    """

    owner_id: int
    color: str = Field(pattern="^(yellow|blue|gray)$")
    model: str = Field(pattern="^(hatch|sedan|convertible)$")

    @field_validator("owner_id")
    def validate_owner_id(cls, value):
        """
        Validates that the owner ID is a positive integer.

        Raises:
            JsonBodyParsingError: If the owner ID is not a positive integer.
        """
        if value <= 0:
            raise JsonBodyParsingError("Owner ID must be a positive integer")
        return value

    model_config = ConfigDict(from_attributes=True)


class CarSchemaOut(BaseModel):
    """
    Schema for output representation of car data.

    Attributes:
        id (int): The ID of the car.
        owner_id (int): The ID of the owner.
        color (str): The color of the car.
        model (str): The model of the car.
    """

    id: int
    owner_id: int
    color: str
    model: str

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    """
    Schema for input validation of user data.

    Attributes:
        username (str): The username, must be between 3 and 30 characters.
        password (str): The password, must be between 8 and 50 characters and
                        contain at least one upper case letter, one lower case letter,
                        one number, and one special character.
    """

    username: str = Field(min_length=3, max_length=30)
    password: str = Field(
        min_length=8,
        max_length=50,
        # Contains at least one upper case letter, one lower case letter, one number and one special character
    )

    @field_validator("password")
    def validate_password(cls, value):
        """
        Validates that the password contains at least one upper case letter,
        one lower case letter, one number, and one special character.

        Raises:
            JsonBodyParsingError: If the password does not meet the criteria.
        """
        if (
            not any(c.isupper() for c in value)
            or not any(c.islower() for c in value)
            or not any(c.isdigit() for c in value)
            or not any(c in string.punctuation for c in value)
        ):
            raise JsonBodyParsingError(
                "Password must contain at least one upper case letter, one lower case letter, one number and one special character"
            )
        return value

    model_config = ConfigDict(from_attributes=True)
