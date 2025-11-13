#!/usr/bin/env python3
"""
Secret Manager for Fritz!Box API
Securely handles credentials and authentication
"""

import json
import os
from pathlib import Path

import structlog
from cryptography.fernet import Fernet

logger = structlog.get_logger(__name__)


class SecretManager:
    """Manages encrypted storage of Fritz!Box credentials"""

    def __init__(self, storage_path: str = None):
        self.storage_path = Path(
            storage_path or os.path.expanduser("~/.fritzbox_secrets")
        )
        self.storage_path.mkdir(exist_ok=True)
        self.key_file = self.storage_path / "key"
        self.secrets_file = self.storage_path / "secrets.enc"
        self._key: bytes | None = None
        self._cipher: Fernet | None = None

    def _ensure_key(self) -> bytes:
        """Ensure encryption key exists"""
        if self._key is None:
            if self.key_file.exists():
                self._key = self.key_file.read_bytes()
            else:
                self._key = Fernet.generate_key()
                self.key_file.write_bytes(self._key)
                self.key_file.chmod(0o600)  # Restrictive permissions

        return self._key

    def _get_cipher(self) -> Fernet:
        """Get encryption cipher"""
        if self._cipher is None:
            key = self._ensure_key()
            self._cipher = Fernet(key)
        return self._cipher

    def store_credentials(self, host: str, username: str, password: str) -> bool:
        """Store encrypted Fritz!Box credentials"""
        try:
            # Load existing secrets
            secrets = self.load_all_secrets()

            # Add/update credentials
            secrets[host] = {
                "username": username,
                "password": password,
                "updated_at": str(Path().cwd()),
            }

            # Encrypt and save
            cipher = self._get_cipher()
            encrypted_data = cipher.encrypt(json.dumps(secrets).encode())
            self.secrets_file.write_bytes(encrypted_data)
            self.secrets_file.chmod(0o600)

            logger.info("Credentials stored securely", host=host)
            return True

        except Exception as e:
            logger.error("Failed to store credentials", error=str(e))
            return False

    def get_credentials(self, host: str) -> dict[str, str] | None:
        """Retrieve credentials for specific host"""
        try:
            secrets = self.load_all_secrets()
            return secrets.get(host)

        except Exception as e:
            logger.error("Failed to retrieve credentials", host=host, error=str(e))
            return None

    def load_all_secrets(self) -> dict[str, dict]:
        """Load all stored secrets"""
        if not self.secrets_file.exists():
            return {}

        try:
            cipher = self._get_cipher()
            encrypted_data = self.secrets_file.read_bytes()
            decrypted_data = cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())

        except Exception as e:
            logger.error("Failed to load secrets", error=str(e))
            return {}

    def delete_credentials(self, host: str) -> bool:
        """Delete credentials for specific host"""
        try:
            secrets = self.load_all_secrets()
            if host in secrets:
                del secrets[host]

                # Re-encrypt remaining secrets
                cipher = self._get_cipher()
                encrypted_data = cipher.encrypt(json.dumps(secrets).encode())
                self.secrets_file.write_bytes(encrypted_data)

                logger.info("Credentials deleted", host=host)
                return True
            else:
                logger.warning("No credentials found to delete", host=host)
                return False

        except Exception as e:
            logger.error("Failed to delete credentials", host=host, error=str(e))
            return False

    def list_hosts(self) -> list:
        """List all stored hostnames"""
        secrets = self.load_all_secrets()
        return list(secrets.keys())


def main():
    """Example usage of SecretManager"""
    import getpass

    secret_manager = SecretManager()

    print("Fritz!Box Secret Manager")
    print("=" * 30)

    while True:
        print("\n1. Store credentials")
        print("2. List stored hosts")
        print("3. Retrieve credentials")
        print("4. Delete credentials")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            host = input("Fritz!Box IP/hostname (e.g., 192.168.178.1): ").strip()
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")

            if secret_manager.store_credentials(host, username, password):
                print("✅ Credentials stored successfully!")
            else:
                print("❌ Failed to store credentials")

        elif choice == "2":
            hosts = secret_manager.list_hosts()
            if hosts:
                print(f"\nStored hosts: {', '.join(hosts)}")
            else:
                print("\nNo credentials stored yet")

        elif choice == "3":
            host = input("Enter hostname to retrieve: ").strip()
            creds = secret_manager.get_credentials(host)
            if creds:
                print(f"\nUsername: {creds['username']}")
                print(f"Password: {'*' * len(creds['password'])}")
            else:
                print("\nNo credentials found for this host")

        elif choice == "4":
            host = input("Enter hostname to delete: ").strip()
            if secret_manager.delete_credentials(host):
                print("✅ Credentials deleted successfully!")
            else:
                print("❌ Failed to delete credentials")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
