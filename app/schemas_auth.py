from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer, field_validator

from app.schemas import _as_utc_z, _blank


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class RegisterRequest(BaseModel):
    email: EmailStr = Field(examples=["amina@community.local"])
    display_name: str = Field(min_length=2, max_length=100, examples=["Amina Shah"])
    password: str = Field(min_length=8, max_length=128, examples=["voter1234"])

    @field_validator("display_name")
    @classmethod
    def strip_display_name(cls, value: str) -> str:
        return _blank(value)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    display_name: str
    role: UserRole
    created_at: datetime

    @field_serializer("created_at", when_used="json")
    def serialize_created_at(self, value: datetime) -> str:
        return _as_utc_z(value)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class TokenPayload(BaseModel):
    user_id: int
    role: UserRole
