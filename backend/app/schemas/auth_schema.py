from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)

    email: EmailStr

    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str

    token_type: str = "Bearer"


class LoginResponse(BaseModel):
    message: str

    access_token: str

    token_type: str = "Bearer"


class RegisterResponse(BaseModel):
    message: str

    user_id: str

    email: EmailStr


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirmRequest(BaseModel):
    token: str

    new_password: str = Field(min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)

    new_password: str = Field(min_length=8, max_length=128)


class EmailVerificationRequest(BaseModel):
    token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str

    token_type: str = "Bearer"


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str

    full_name: str

    email: EmailStr

    is_active: bool

    is_verified: bool

    eco_travel_score: int

    total_trips: int

    created_at: datetime


class LogoutResponse(BaseModel):
    message: str


class AuthenticationStatusResponse(BaseModel):
    authenticated: bool

    user_id: str | None = None

    email: str | None = None
