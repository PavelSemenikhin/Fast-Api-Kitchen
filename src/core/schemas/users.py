import re

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserReadSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequestSchema(BaseModel):
    refresh_token: str


class TokenRefreshResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
