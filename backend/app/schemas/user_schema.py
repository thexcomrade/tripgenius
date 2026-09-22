from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator


class UserRegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)

    email: EmailStr

    password: str = Field(min_length=8, max_length=128)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Full name cannot be empty")

        return value


class UserLoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(min_length=8, max_length=128)


class UserProfileUpdateRequest(BaseModel):
    profile_image: str | None = None

    bio: str | None = Field(default=None, max_length=1000)

    country: str | None = Field(default=None, max_length=100)

    preferred_budget: str | None = Field(default=None, max_length=50)

    preferred_travel_style: str | None = Field(default=None, max_length=100)

    favourite_destination: str | None = Field(default=None, max_length=150)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    full_name: str

    email: EmailStr

    profile_image: str | None

    bio: str | None

    country: str | None

    preferred_budget: str | None

    preferred_travel_style: str | None

    favourite_destination: str | None

    eco_travel_score: int

    total_trips: int

    is_active: bool

    is_verified: bool

    created_at: datetime

    updated_at: datetime


class UserPublicProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    full_name: str

    profile_image: str | None

    bio: str | None

    country: str | None

    preferred_travel_style: str | None

    favourite_destination: str | None

    eco_travel_score: int

    total_trips: int


class AuthTokenResponse(BaseModel):
    access_token: str

    token_type: str = "Bearer"


class AuthResponse(BaseModel):
    message: str

    user: UserResponse

    access_token: str

    token_type: str = "Bearer"


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)

    new_password: str = Field(min_length=8, max_length=128)


class UserStatisticsResponse(BaseModel):
    total_trips: int

    eco_travel_score: int

    favourite_destination: str | None

    preferred_travel_style: str | None


class UserPreferenceResponse(BaseModel):
    preferred_budget: str | None

    preferred_travel_style: str | None

    favourite_destination: str | None

    country: str | None


class MessageResponse(BaseModel):
    message: str
