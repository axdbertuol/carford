from pydantic import BaseModel, Field, field_validator


class OwnerSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class CarSchema(BaseModel):
    owner_id: int
    color: str = Field(regex="^(yellow|blue|gray)$")
    model: str = Field(regex="^(hatch|sedan|convertible)$")

    @field_validator("owner_id")
    def validate_owner_id(cls, value):
        if value <= 0:
            raise ValueError("Owner ID must be a positive integer")
        return value
