"""
JWT Token Management für Agent Control Plane

Verwaltet JWT Token Generation, Validation und Refresh
"""

import logging
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

logger = logging.getLogger(__name__)


class TokenManager:
    """Service für JWT Token Management"""

    def __init__(self):
        self.secret_key = "your-secret-key-change-in-production"
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        # Token blacklist für revoked tokens
        self.blacklisted_tokens: set = set()

    async def initialize(self):
        """Initialisiert den Token Manager"""
        logger.info("Initializing Token Manager...")
        # In production: Lade secret key aus secure storage
        logger.info("Token Manager initialized")

    def create_access_token(self, data: dict) -> str:
        """Erstellt JWT Access Token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        logger.info(f"Created access token for user: {data.get('sub', 'unknown')}")
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        """Erstellt JWT Refresh Token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        logger.info(f"Created refresh token for user: {data.get('sub', 'unknown')}")
        return encoded_jwt

    def verify_token(self, token: str) -> dict | None:
        """Verifiziert JWT Token"""
        if token in self.blacklisted_tokens:
            logger.warning("Token is blacklisted")
            return None

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # Prüfe ob Token abgelaufen
            if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
                logger.warning("Token has expired")
                return None

            logger.info(f"Token verified for user: {payload.get('sub', 'unknown')}")
            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("Token signature expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None

    def revoke_token(self, token: str) -> bool:
        """Setzt Token auf Blacklist"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            self.blacklisted_tokens.add(token)
            logger.info(f"Token revoked for user: {payload.get('sub', 'unknown')}")
            return True
        except jwt.InvalidTokenError:
            logger.warning("Cannot revoke invalid token")
            return False

    def refresh_access_token(self, refresh_token: str) -> str | None:
        """Erneuert Access Token mit Refresh Token"""
        try:
            payload = jwt.decode(
                refresh_token, self.secret_key, algorithms=[self.algorithm]
            )

            # Prüfe ob es ein Refresh Token ist
            if payload.get("type") != "refresh":
                logger.warning("Not a refresh token")
                return None

            # Prüfe ob Token abgelaufen
            if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
                logger.warning("Refresh token has expired")
                return None

            # Prüfe ob Token blacklisted ist
            if refresh_token in self.blacklisted_tokens:
                logger.warning("Refresh token is blacklisted")
                return None

            # Erstelle neuen Access Token
            user_data = {
                "sub": payload["sub"],
                "role": payload.get("role", "user"),
                "permissions": payload.get("permissions", []),
            }

            # Alten Refresh Token blacklisten
            self.blacklisted_tokens.add(refresh_token)

            new_token = self.create_access_token(user_data)
            logger.info(
                f"Access token refreshed for user: {payload.get('sub', 'unknown')}"
            )
            return new_token

        except jwt.InvalidTokenError:
            logger.warning("Invalid refresh token")
            return None

    def get_token_info(self, token: str) -> dict | None:
        """Holt Token Informationen ohne Validierung"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return {
                "user_id": payload.get("sub"),
                "role": payload.get("role"),
                "permissions": payload.get("permissions"),
                "expires_at": datetime.fromtimestamp(payload["exp"]).isoformat(),
                "token_type": payload.get("type"),
                "is_expired": datetime.utcnow()
                > datetime.fromtimestamp(payload["exp"]),
                "is_blacklisted": token in self.blacklisted_tokens,
            }
        except jwt.InvalidTokenError:
            return None

    def cleanup_expired_tokens(self):
        """Räumt abgelaufene Tokens aus Blacklist"""
        current_time = datetime.utcnow()
        expired_tokens = []

        for token in self.blacklisted_tokens:
            try:
                payload = jwt.decode(
                    token, self.secret_key, algorithms=[self.algorithm]
                )
                if current_time > datetime.fromtimestamp(payload["exp"]):
                    expired_tokens.append(token)
            except jwt.InvalidTokenError:
                expired_tokens.append(token)

        # Entferne abgelaufene Tokens
        for token in expired_tokens:
            self.blacklisted_tokens.discard(token)

        if expired_tokens:
            logger.info(
                f"Cleaned up {len(expired_tokens)} expired tokens from blacklist"
            )

    async def cleanup(self):
        """Cleanup beim Shutdown"""
        logger.info("Token Manager cleanup complete")
        # In production: Speichere blacklist persistently
