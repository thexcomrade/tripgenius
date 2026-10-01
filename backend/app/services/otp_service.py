"""
TripGenius One-Time Passcode (OTP) Verification Service.
Manages secure generation, lifespan, and single-use validation of 6-digit
passcodes for sensitive operations like password changes.
"""

import secrets
import time
from typing import Any


class OTPService:
    def __init__(self, expiry_seconds: int = 600, cooldown_seconds: int = 30) -> None:
        self.expiry_seconds = expiry_seconds
        self.cooldown_seconds = cooldown_seconds
        # In-memory store: user_id -> dict
        self._store: dict[str, dict[str, Any]] = {}

    def generate_otp(self, user_id: str, email: str) -> tuple[str, bool]:
        """
        Generate a cryptographically secure 6-digit OTP code for a user.
        Returns: (code, is_new)
        """
        now = time.time()
        existing = self._store.get(user_id)

        # Check cooldown to prevent email bombing
        if existing and (now - existing["created_at"]) < self.cooldown_seconds:
            # Within cooldown window: return existing code without generating a new one
            return existing["code"], False

        # Generate a 6-digit numeric OTP (100000 - 999999)
        code = f"{secrets.randbelow(900000) + 100000}"

        self._store[user_id] = {
            "code": code,
            "email": email,
            "created_at": now,
            "expires_at": now + self.expiry_seconds,
            "attempts": 0,
        }

        return code, True

    def verify_otp(self, user_id: str, code: str) -> bool:
        """
        Verify the provided OTP code for a given user.
        Enforces single-use: deletes the OTP on successful verification.
        Enforces attempt limit: invalidates after 5 failed attempts.
        """
        now = time.time()
        entry = self._store.get(user_id)

        if not entry:
            return False

        # Check expiration
        if now > entry["expires_at"]:
            self._store.pop(user_id, None)
            return False

        # Check attempt count
        entry["attempts"] += 1
        if entry["attempts"] > 5:
            self._store.pop(user_id, None)
            return False

        # Constant-time comparison
        clean_code = str(code).strip()
        if secrets.compare_digest(entry["code"], clean_code):
            # Success: invalidate immediately (single-use)
            self._store.pop(user_id, None)
            return True

        return False

    def clear_otp(self, user_id: str) -> None:
        self._store.pop(user_id, None)


_otp_service_instance: OTPService | None = None


def get_otp_service() -> OTPService:
    global _otp_service_instance
    if _otp_service_instance is None:
        _otp_service_instance = OTPService()
    return _otp_service_instance
