"""
User Management Service für Agent Control Plane

Verwaltet Linux User Authentication und SSH Key Management
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from bcrypt import hashpw, checkpw, gensalt

logger = logging.getLogger(__name__)


class UserManager:
    """Service für Linux User Management"""

    def __init__(self):
        self.users_file = Path("config/users.json")
        self.users: dict[str, dict] = {}

    async def initialize(self):
        """Initialisiert den User Manager"""
        logger.info("Initializing User Manager...")

        # Erstelle config Verzeichnis
        self.users_file.parent.mkdir(parents=True, exist_ok=True)

        # Lade existierende User
        if self.users_file.exists():
            with open(self.users_file) as f:
                self.users = json.load(f)
                logger.info(f"Loaded {len(self.users)} users")
        else:
            # Erstelle Default Admin User
            await self.create_default_admin()

    async def create_default_admin(self):
        """Erstellt Default Admin User"""
        default_admin = {
            "username": "admin",
            "password_hash": hashpw("admin".encode('utf-8'), gensalt()).decode('utf-8'),
            "role": "admin",
            "ssh_keys": [],
            "permissions": ["*"],
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "active": True,
        }

        self.users["admin"] = default_admin
        await self.save_users()
        logger.info("Created default admin user (admin/admin)")

    async def authenticate_user(self, username: str, password: str) -> dict | None:
        """Authentifiziert User gegen Linux System"""
        if username not in self.users:
            return None

        user = self.users[username]

        # Prüfe Passwort
        if checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
            # Update last login
            user["last_login"] = datetime.now().isoformat()
            await self.save_users()

            logger.info(f"User {username} authenticated successfully")
            return {
                "username": username,
                "role": user["role"],
                "permissions": user["permissions"],
                "last_login": user["last_login"],
            }

        logger.warning(f"Failed authentication attempt for user {username}")
        return None

    async def verify_ssh_key(self, username: str, ssh_public_key: str) -> bool:
        """Verifiziert SSH Public Key"""
        if username not in self.users:
            return False

        user = self.users[username]
        return ssh_public_key in user.get("ssh_keys", [])

    async def add_ssh_key(self, username: str, ssh_public_key: str) -> bool:
        """Fügt SSH Public Key hinzu"""
        if username not in self.users:
            return False

        user = self.users[username]
        if ssh_public_key not in user.get("ssh_keys", []):
            user["ssh_keys"].append(ssh_public_key)
            await self.save_users()
            logger.info(f"Added SSH key for user {username}")
            return True

        return False

    async def remove_ssh_key(self, username: str, ssh_public_key: str) -> bool:
        """Entfernt SSH Public Key"""
        if username not in self.users:
            return False

        user = self.users[username]
        if ssh_public_key in user.get("ssh_keys", []):
            user["ssh_keys"].remove(ssh_public_key)
            await self.save_users()
            logger.info(f"Removed SSH key for user {username}")
            return True

        return False

    async def create_user(
        self,
        username: str,
        password: str,
        role: str = "user",
        permissions: list[str] = None,
    ) -> bool:
        """Erstellt neuen User"""
        if username in self.users:
            return False

        if permissions is None:
            permissions = ["read"]

        new_user = {
            "username": username,
            "password_hash": hashpw(password.encode('utf-8'), gensalt()).decode('utf-8'),
            "role": role,
            "ssh_keys": [],
            "permissions": permissions,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "active": True,
        }

        self.users[username] = new_user
        await self.save_users()
        logger.info(f"Created new user: {username}")
        return True

    async def update_user(self, username: str, updates: dict) -> bool:
        """Aktualisiert User"""
        if username not in self.users:
            return False

        user = self.users[username]

        # Erlaubte Updates
        allowed_fields = ["password", "role", "permissions", "active"]
        for field, value in updates.items():
            if field in allowed_fields:
                if field == "password":
                    user["password_hash"] = hashpw(value.encode('utf-8'), gensalt()).decode('utf-8')
                else:
                    user[field] = value

        await self.save_users()
        logger.info(f"Updated user: {username}")
        return True

    async def delete_user(self, username: str) -> bool:
        """Löscht User"""
        if username not in self.users or username == "admin":
            return False

        del self.users[username]
        await self.save_users()
        logger.info(f"Deleted user: {username}")
        return True

    async def get_user(self, username: str) -> dict | None:
        """Holt User Informationen"""
        return self.users.get(username)

    async def list_users(self) -> list[dict]:
        """Listet alle Users auf"""
        return [
            {
                "username": username,
                "role": user["role"],
                "permissions": user["permissions"],
                "created_at": user["created_at"],
                "last_login": user["last_login"],
                "active": user["active"],
            }
            for username, user in self.users.items()
        ]

    async def save_users(self):
        """Speichert User in Datei"""
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=2)

    async def cleanup(self):
        """Cleanup beim Shutdown"""
        logger.info("User Manager cleanup complete")
