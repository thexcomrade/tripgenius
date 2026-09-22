from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database.db import get_db

from app.core.security import get_token_subject

from app.services.auth_service import AuthService

from app.schemas.auth_schema import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    ChangePasswordRequest,
    CurrentUserResponse,
    AuthenticationStatusResponse,
    LogoutResponse,
)


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:

    return AuthService(db)


def get_current_user_id(authorization: Annotated[str | None, Header()] = None) -> str:

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

    token = authorization.replace("Bearer ", "")

    try:
        return get_token_subject(token)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


@router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
def register_user(
    payload: RegisterRequest, service: AuthService = Depends(get_auth_service)
) -> RegisterResponse:

    try:
        user = service.register_user(payload)

        return RegisterResponse(
            message="User registered successfully", user_id=user.id, email=user.email
        )

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/login", response_model=LoginResponse)
def login_user(
    payload: LoginRequest, service: AuthService = Depends(get_auth_service)
) -> LoginResponse:

    try:
        result = service.login_user(payload)

        return LoginResponse(
            message="Login successful",
            access_token=result["access_token"],
            token_type=result["token_type"],
        )

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


@router.get("/profile", response_model=CurrentUserResponse)
def get_profile(
    user_id: str = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service),
) -> CurrentUserResponse:

    try:
        user = service.get_authenticated_profile(user_id)

        return CurrentUserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            eco_travel_score=user.eco_travel_score,
            total_trips=user.total_trips,
            created_at=user.created_at,
        )

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    user_id: str = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service),
) -> dict:

    try:
        service.change_password(
            user_id=user_id,
            current_password=payload.current_password,
            new_password=payload.new_password,
        )

        return {"message": "Password updated successfully"}

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/status", response_model=AuthenticationStatusResponse)
def authentication_status(
    user_id: str = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service),
) -> AuthenticationStatusResponse:

    try:
        user = service.get_authenticated_profile(user_id)

        return AuthenticationStatusResponse(
            authenticated=True, user_id=user.id, email=user.email
        )

    except Exception:
        return AuthenticationStatusResponse(authenticated=False)


@router.post("/logout", response_model=LogoutResponse)
def logout() -> LogoutResponse:

    return LogoutResponse(message="Logout successful")
