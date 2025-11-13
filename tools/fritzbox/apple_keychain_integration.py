#!/usr/bin/env python3
"""
Apple Keychain Integration for Fritz!Box
Automatically retrieves Fritz!Box credentials from Apple Keychain
"""

import subprocess

import structlog

logger = structlog.get_logger(__name__)


class AppleKeychainManager:
    """Manages Fritz!Box credentials from Apple Keychain"""

    @staticmethod
    def get_fritzbox_credentials() -> dict[str, str] | None:
        """Retrieve Fritz!Box credentials from Apple Keychain"""
        try:
            # Try different approaches to get Fritz!Box credentials
            credentials = []

            # Method 1: Generic password with service "fritzbox"
            try:
                password = subprocess.check_output(
                    ["security", "find-generic-password", "-s", "fritzbox", "-w"],
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).strip()
                if password:
                    credentials.append(
                        {
                            "username": "admin",
                            "password": password,
                            "source": "fritzbox service",
                        }
                    )
            except subprocess.CalledProcessError:
                pass

            # Method 2: Account "fritz.box"
            try:
                password = subprocess.check_output(
                    ["security", "find-generic-password", "-a", "fritz.box", "-w"],
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).strip()
                if password:
                    credentials.append(
                        {
                            "username": "admin",
                            "password": password,
                            "source": "fritz.box account",
                        }
                    )
            except subprocess.CalledProcessError:
                pass

            # Method 3: Search for any Fritz!Box related entries
            try:
                result = subprocess.check_output(
                    ["security", "dump-keychain"], stderr=subprocess.DEVNULL, text=True
                )

                # Look for Fritz!Box patterns
                lines = result.split("\n")
                for _i, line in enumerate(lines):
                    if "fritz" in line.lower() and "acct" in line:
                        # Extract account name
                        account = line.split('"acct"<blob>="')[-1].strip('"')
                        if account and account != "fritz.box":
                            try:
                                password = subprocess.check_output(
                                    [
                                        "security",
                                        "find-generic-password",
                                        "-a",
                                        account,
                                        "-w",
                                    ],
                                    stderr=subprocess.DEVNULL,
                                    text=True,
                                ).strip()
                                if password:
                                    credentials.append(
                                        {
                                            "username": account,
                                            "password": password,
                                            "source": f"account {account}",
                                        }
                                    )
                            except subprocess.CalledProcessError:
                                pass
            except subprocess.CalledProcessError:
                pass

            if credentials:
                logger.info(
                    f"Found {len(credentials)} Fritz!Box credential sets in Keychain"
                )
                return credentials[0]  # Return the first valid set
            else:
                logger.warning("No Fritz!Box credentials found in Apple Keychain")
                return None

        except Exception as e:
            logger.error("Error accessing Apple Keychain", error=str(e))
            return None

    @staticmethod
    def list_fritzbox_entries() -> list:
        """List all Fritz!Box related entries in Keychain"""
        try:
            result = subprocess.check_output(
                ["security", "dump-keychain"], stderr=subprocess.DEVNULL, text=True
            )

            entries = []
            lines = result.split("\n")
            current_entry = {}

            for line in lines:
                line = line.strip()
                if line.startswith("class:"):
                    if current_entry and "fritz" in str(current_entry).lower():
                        entries.append(current_entry)
                    current_entry = {"class": line.split('"')[-1]}
                elif line.startswith('"acct"'):
                    current_entry["account"] = line.split('"')[-1]
                elif line.startswith('"svce"'):
                    current_entry["service"] = line.split('"')[-1]
                elif line.startswith('"desc"'):
                    current_entry["description"] = line.split('"')[-1]

            # Add last entry if Fritz!Box related
            if current_entry and "fritz" in str(current_entry).lower():
                entries.append(current_entry)

            return entries

        except Exception as e:
            logger.error("Error listing Keychain entries", error=str(e))
            return []

    @staticmethod
    def test_credentials(username: str, password: str) -> bool:
        """Test if credentials work with Fritz!Box"""
        try:
            import asyncio

            from fritzbox_api import FritzBoxAPI

            async def test():
                fritz = FritzBoxAPI(
                    host="192.168.178.1", user=username, password=password
                )
                return await fritz.connect()

            return asyncio.run(test())

        except Exception as e:
            logger.error("Error testing credentials", error=str(e))
            return False


def main():
    """Main function for testing Keychain integration"""
    print("🔑 Apple Keychain Fritz!Box Integration")
    print("=" * 45)

    # List Fritz!Box entries
    print("\n📋 Fritz!Box entries in Keychain:")
    entries = AppleKeychainManager.list_fritzbox_entries()

    if entries:
        for i, entry in enumerate(entries, 1):
            print(f"  {i}. Service: {entry.get('service', 'N/A')}")
            print(f"     Account: {entry.get('account', 'N/A')}")
            print(f"     Description: {entry.get('description', 'N/A')}")
            print()
    else:
        print("  No Fritz!Box entries found")

    # Get credentials
    print("🔍 Retrieving Fritz!Box credentials...")
    creds = AppleKeychainManager.get_fritzbox_credentials()

    if creds:
        print(f"✅ Found credentials from: {creds['source']}")
        print(f"   Username: {creds['username']}")
        print(f"   Password: {'*' * len(creds['password'])}")

        # Test credentials
        print("\n🧪 Testing credentials...")
        if AppleKeychainManager.test_credentials(creds["username"], creds["password"]):
            print("✅ Credentials work!")

            # Store to secret manager
            try:
                from secret_manager import SecretManager

                sm = SecretManager()
                if sm.store_credentials(
                    "192.168.178.1", creds["username"], creds["password"]
                ):
                    print("✅ Credentials stored in secret manager!")
                else:
                    print("❌ Failed to store credentials")
            except Exception as e:
                print(f"❌ Error storing credentials: {e}")
        else:
            print("❌ Credentials don't work with Fritz!Box API")
    else:
        print("❌ No valid Fritz!Box credentials found in Keychain")
        print("\n💡 Suggestions:")
        print("• Check if Fritz!Box password is stored in Keychain")
        print("• Try adding Fritz!Box credentials to Keychain manually")
        print("• Use setup_helper.py for manual configuration")


if __name__ == "__main__":
    main()
