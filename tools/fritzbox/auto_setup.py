#!/usr/bin/env python3
"""
Fritz!Box Setup with Apple Keychain Integration
Automatically detects and configures Fritz!Box credentials
"""

import subprocess
import webbrowser


def print_header():
    """Print setup header"""
    print("🔧 Fritz!Box Setup with Apple Keychain Integration")
    print("=" * 55)
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


def get_keychain_credentials():
    """Get Fritz!Box credentials from Apple Keychain"""
    print("🔑 Searching Apple Keychain for Fritz!Box credentials...")

    credentials = []

    # Try different methods
    methods = [
        ("service", "fritzbox"),
        ("account", "fritz.box"),
        ("account", "admin"),
        ("account", "FRITZ!Box"),
    ]

    for method_type, value in methods:
        try:
            if method_type == "service":
                password = subprocess.check_output(
                    ["security", "find-generic-password", "-s", value, "-w"],
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).strip()
            else:  # account
                password = subprocess.check_output(
                    ["security", "find-generic-password", "-a", value, "-w"],
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).strip()

            if password:
                credentials.append(
                    {
                        "username": "admin",
                        "password": password,
                        "source": f"{method_type}: {value}",
                    }
                )
        except subprocess.CalledProcessError:
            continue

    if credentials:
        print(f"✅ Found {len(credentials)} credential sets in Keychain")
        return credentials
    else:
        print("❌ No Fritz!Box credentials found in Keychain")
        return []


def test_credentials(username, password):
    """Test Fritz!Box credentials"""
    try:
        import asyncio

        from fritzbox_api import FritzBoxAPI

        async def test():
            fritz = FritzBoxAPI(host="192.168.178.1", user=username, password=password)
            return await fritz.connect()

        return asyncio.run(test())
    except:
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
    print("6. Go to: System → FRITZ!Box Users")
    print("7. Create or update user with TR-064 permissions")
    print("8. Note the username and password you use")
    print()


def manual_setup():
    """Manual credential setup"""
    print("⚙️  Manual Setup Required")
    print("We couldn't find working credentials automatically.")
    print("Please set up your Fritz!Box credentials manually:")
    print()

    try:
        import getpass

        from secret_manager import SecretManager

        sm = SecretManager()

        print("Enter your Fritz!Box TR-064 credentials:")
        username = input("Username (usually 'admin'): ").strip()
        if not username:
            username = "admin"

        password = getpass.getpass("Password: ")

        if not password:
            print("❌ Password cannot be empty")
            return False

        if sm.store_credentials("192.168.178.1", username, password):
            print("✅ Credentials stored successfully!")

            # Test the credentials
            if test_credentials(username, password):
                print("✅ Credentials work perfectly!")
                return True
            else:
                print("❌ Credentials don't work. Please check:")
                print("• TR-064 is enabled in Fritz!Box settings")
                print("• Username and password are correct")
                print("• User has TR-064 permissions")
                return False
        else:
            print("❌ Failed to store credentials")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main setup flow"""
    print_header()

    # Step 1: Check reachability
    if not check_fritzbox_reachability():
        print("\n❌ Cannot proceed - Fritz!Box not reachable")
        return

    # Step 2: Try Keychain credentials
    credentials = get_keychain_credentials()

    working_creds = None
    if credentials:
        print("\n🧪 Testing credentials...")
        for i, cred in enumerate(credentials, 1):
            print(f"Testing {i}/{len(credentials)}: {cred['source']}")
            if test_credentials(cred["username"], cred["password"]):
                print(f"✅ Working credentials found: {cred['source']}")
                working_creds = cred
                break
            else:
                print(f"❌ Failed: {cred['source']}")

    # Step 3: If no working credentials, do manual setup
    if not working_creds:
        open_fritzbox_interface()
        print_tr064_instructions()

        print("\n" + "=" * 55)
        print("🔧 MANUAL SETUP REQUIRED")
        print("=" * 55)

        if manual_setup():
            print("\n🎉 Setup completed successfully!")
        else:
            print("\n❌ Setup failed. Please check your Fritz!Box settings.")
            return
    else:
        # Store working credentials
        try:
            from secret_manager import SecretManager

            sm = SecretManager()
            sm.store_credentials(
                "192.168.178.1", working_creds["username"], working_creds["password"]
            )
            print("✅ Working credentials stored in secret manager")
        except Exception as e:
            print(f"⚠️  Warning: Could not store credentials: {e}")

    # Step 4: Final test
    print("\n🧪 Final connection test...")
    try:
        import asyncio

        from fritzbox_api import FritzBoxAPI
        from secret_manager import SecretManager

        async def final_test():
            sm = SecretManager()
            creds = sm.get_credentials("192.168.178.1")

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

                # Get external IP
                external_ip = await fritz.get_external_ip()
                print(f"🌐 External IP: {external_ip}")

                # Get connected devices
                devices = await fritz.get_connected_devices()
                print(f"📊 Connected devices: {len(devices)}")

                return True
            else:
                return False

        if asyncio.run(final_test()):
            print("\n🎉 Fritz!Box setup completed successfully!")
            print("\nNext steps:")
            print("• Run: python fritzbox_api_examples.py --interactive")
            print("• Start MCP server: python fritzbox_mcp_server.py")
            print("• Check CONNECTED_SYSTEMS.md for integration info")
        else:
            print("\n❌ Final test failed")

    except Exception as e:
        print(f"❌ Final test error: {e}")


if __name__ == "__main__":
    main()
