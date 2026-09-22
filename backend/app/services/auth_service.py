from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.auth_schema import LoginRequest, RegisterRequest

from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def register_user(self, payload: RegisterRequest) -> User:

        existing_user = self.get_user_by_email(payload.email)

        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            full_name=payload.full_name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
        )

        self.db.add(user)

        self.db.commit()

        self.db.refresh(user)

        return user

    def authenticate_user(self, payload: LoginRequest) -> User:

        user = self.get_user_by_email(payload.email)

        if not user:
            raise ValueError("Invalid email or password")

        is_valid = verify_password(payload.password, user.hashed_password)

        if not is_valid:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Account is disabled")

        return user

    def login_user(self, payload: LoginRequest) -> dict:

        user = self.authenticate_user(payload)

        access_token = create_access_token(subject=user.id)

        return {"access_token": access_token, "token_type": "Bearer", "user": user}

    def change_password(
        self, user_id: str, current_password: str, new_password: str
    ) -> bool:

        user = self.get_user_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        is_valid = verify_password(current_password, user.hashed_password)

        if not is_valid:
            raise ValueError("Current password is incorrect")

        user.hashed_password = hash_password(new_password)

        self.db.commit()

        return True

    def activate_user(self, user_id: str) -> User:

        user = self.get_user_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        user.is_active = True

        self.db.commit()

        self.db.refresh(user)

        return user

    def deactivate_user(self, user_id: str) -> User:

        user = self.get_user_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        user.is_active = False

        self.db.commit()

        self.db.refresh(user)

        return user

    def verify_user(self, user_id: str) -> User:

        user = self.get_user_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        user.is_verified = True

        self.db.commit()

        self.db.refresh(user)

        return user

    def update_eco_score(self, user_id: str, points: int) -> User:

        user = self.get_user_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        user.eco_travel_score += points

        self.db.commit()

        self.db.refresh(user)

        return user

    def increment_trip_count(self, user_id: str) -> User:

        user = self.get_user_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        user.total_trips += 1

        self.db.commit()

        self.db.refresh(user)

        return user

    def get_authenticated_profile(self, user_id: str) -> User:

        user = self.get_user_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        return user
