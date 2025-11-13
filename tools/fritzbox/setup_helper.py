#!/usr/bin/env python3
"""
Fritz!Box Setup Helper
Helps configure Fritz!Box API access
"""

import subprocess
import webbrowser


def print_header():
    """Print setup header"""
    print("🔧 Fritz!Box API Setup Helper")
    print("=" * 40)
    print()


def check_fritzbox_reachability():
    """Check if Fritz!Box is reachable"""
    print("📡 Checking Fritz!Box reachability...")
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "192.168.178.1"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            print("✅ Fritz!Box is reachable")
            return True
        else:
            print("❌ Fritz!Box not reachable")
            return False
    except:
        print("❌ Could not ping Fritz!Box")
        return False


def open_fritzbox_interface():
    """Open Fritz!Box web interface"""
    print("🌐 Opening Fritz!Box web interface...")
    try:
        webbrowser.open("http://fritz.box")
        print("✅ Fritz!Box interface opened in browser")
        return True
    except:
        print("❌ Could not open browser")
        return False


def print_tr064_instructions():
    """Print TR-064 setup instructions"""
    print("\n📋 TR-064 Setup Instructions:")
    print("1. Open Fritz!Box web interface (should open automatically)")
    print("2. Login to your Fritz!Box")
    print("3. Go to: Home Network → Network → Network Settings")
    print("4. Enable 'Allow access for applications'")
    print("5. Enable 'Allow access from the Internet' (optional)")
    print("6. Note down your username and password")
    print("7. Go to: System → FRITZ!Box Users")
    print("8. Create or update user with TR-064 permissions")
    print()


def print_password_help():
    """Print password finding help"""
    print("🔑 Password Help:")
    print("• Default password is usually on the bottom of the router")
    print("• Check your Fritz!Box manual for default credentials")
    print("• Common usernames: admin, fritz, root")
    print("• Common passwords: password from router bottom, fritz, admin")
    print("• If you changed it, use your custom password")
    print()


def setup_credentials_interactive():
    """Interactive credential setup"""
    print("⚙️  Credential Setup:")
    print("You'll need to enter your Fritz!Box credentials now.")
    print("Make sure TR-064 is enabled in your Fritz!Box settings.")
    print()

    try:
        import getpass

        from secret_manager import SecretManager

        sm = SecretManager()

        # Get user input
        username = input("Fritz!Box username (usually 'admin'): ").strip()
        if not username:
            username = "admin"

        password = getpass.getpass("Fritz!Box password: ")

        if not password:
            print("❌ Password cannot be empty")
            return False

        # Store credentials
        if sm.store_credentials("192.168.178.1", username, password):
            print("✅ Credentials stored successfully!")
            return True
        else:
            print("❌ Failed to store credentials")
            return False

    except KeyboardInterrupt:
        print("\n❌ Setup cancelled")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_connection():
    """Test the connection"""
    print("\n🧪 Testing Connection...")

    try:
        import asyncio

        from fritzbox_api import FritzBoxAPI
        from secret_manager import SecretManager

        async def run_test():
            sm = SecretManager()
            creds = sm.get_credentials("192.168.178.1")

            if not creds:
                print("❌ No credentials found")
                return False

            fritz = FritzBoxAPI(
                host="192.168.178.1", user=creds["username"], password=creds["password"]
            )

            if await fritz.connect():
                print("✅ Connection successful!")

                # Get device info
                device_info = await fritz.get_device_info()
                if device_info:
                    print(f"📱 Router Model: {device_info.get('ModelName', 'Unknown')}")
                    print(
                        f"🔧 Firmware: {device_info.get('SoftwareVersion', 'Unknown')}"
                    )
                    print(f"🔢 Serial: {device_info.get('SerialNumber', 'Unknown')}")

                return True
            else:
                print("❌ Connection failed")
                return False

        return asyncio.run(run_test())

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main setup flow"""
    print_header()

    # Step 1: Check reachability
    if not check_fritzbox_reachability():
        print("\n❌ Cannot proceed - Fritz!Box not reachable")
        print("Please check your network connection and try again.")
        return

    # Step 2: Open web interface
    open_fritzbox_interface()

    # Step 3: Show instructions
    print_tr064_instructions()
    print_password_help()

    # Step 4: Interactive setup
    input("\nPress Enter when you're ready to enter credentials...")

    if setup_credentials_interactive():
        # Step 5: Test connection
        if test_connection():
            print("\n🎉 Setup completed successfully!")
            print("You can now use the Fritz!Box API tools.")
            print("\nNext steps:")
            print("• Run: python fritzbox_api_examples.py --interactive")
            print("• Check CONNECTED_SYSTEMS.md for integration info")
        else:
            print(
                "\n❌ Setup failed - please check your credentials and TR-064 settings"
            )
    else:
        print("\n❌ Setup cancelled")


if __name__ == "__main__":
    main()
