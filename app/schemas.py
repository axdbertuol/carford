from pydantic import BaseModel, ConfigDict, Field, field_validator


class OwnerSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    model_config = ConfigDict(from_attributes=True)


class CarSchema(BaseModel):
    owner_id: int
    color: str = Field(regex="^(yellow|blue|gray)$")
    model: str = Field(regex="^(hatch|sedan|convertible)$")

    @field_validator("owner_id")
    def validate_owner_id(cls, value):
        if value <= 0:
            raise ValueError("Owner ID must be a positive integer")
        return value

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(
        min_length=8,
        max_length=50,
        # Contains at least one upper case letter, one lower case letter, one number and one special character
        regex=r"/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]",
    )

    model_config = ConfigDict(from_attributes=True)
