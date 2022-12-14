from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    full_name: str
    email: str
    address: str
    county: str


class UserRegisterRequest(UserBase):
    email: EmailStr
    password1: str = Field(min_length=8, max_length=20)
    password2: str = Field(min_length=8, max_length=20)

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    class Config:
        schema_extra = {
            "example": {
                "username": "jane_doe",
                "full_name": "Jane Doe",
                "email": "jane.doe@example.com",
                "password1": "password",
                "password2": "password",
                "address": "123 Fake Street",
                "county": "Fakeshire"
            }
        }


class UserPrivilegedRequest(UserRegisterRequest):
    is_superuser: bool | None = None
    is_staff: bool | None = None
    is_active: bool | None = None
    date_joined: datetime | None = None

    class Config:
        schema_extra = {
            "example": {
                "username": "jane_doe",
                "full_name": "Jane Doe",
                "email": "jane.doe@example.com",
                "password1": "password",
                "password2": "password",
                "address": "123 Fake Street",
                "county": "Fakeshire",
                "is_superuser": "f",
                "is_staff": "t",
                "is_active": "t",
                "date_joined": "2022-08-27 15:43:01.843467"
            }
        }


class UserResponse(UserBase):
    id: int
    date_joined: datetime | None = None

    class Config:
        schema_extra = {
            "example": {
                "id": 34,
                "username": "jane_doe",
                "full_name": "Jane Doe",
                "email": "jane.doe@example.com",
                "date_joined": "2022-08-27 15:43:01.843467",
                "address": "123 Fake Street",
                "county": "Fakeshire"
            }
        }


class UserPrivilegedResponse(UserResponse):
    is_superuser: bool | None = None
    is_staff: bool | None = None
    is_active: bool | None = None

    class Config:
        schema_extra = {
            "example": {
                "id": 34,
                "username": "jane_doe",
                "full_name": "Jane Doe",
                "email": "jane.doe@example.com",
                "is_superuser": "f",
                "is_staff": "t",
                "is_active": "t",
                "date_joined": "2022-08-27 15:43:01.843467",
                "address": "123 Fake Street",
                "county": "Fakeshire"
            }
        }
