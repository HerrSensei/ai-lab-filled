#!/usr/bin/env python3
"""
Fritz!Box TR-064 Setup Checker
Helps verify TR-064 configuration
"""

import webbrowser


def print_header():
    print("🔧 Fritz!Box TR-064 Setup Checker")
    print("=" * 40)
    print()


def check_tr064_status():
    """Check TR-064 status with different methods"""
    print("🔍 Checking TR-064 status...")

    try:
        from fritzconnection import FritzConnection

        # Test 1: Check if TR-064 port is open
        print("1. Testing TR-064 port (49000)...")
        import socket

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(("192.168.178.1", 49000))
        sock.close()

        if result == 0:
            print("✅ TR-064 port 49000 is open")
        else:
            print("❌ TR-064 port 49000 is closed")
            return False

        # Test 2: Try to get device info without auth
        print("2. Testing unauthenticated access...")
        try:
            fc = FritzConnection(address="192.168.178.1")
            info = fc.call_action("DeviceInfo", "GetInfo")
            print("✅ TR-064 responds without authentication")
            print(f"   Model: {info.get('ModelName', 'Unknown')}")
            return True
        except Exception as e:
            print(f"❌ Authentication required: {str(e)}")

        # Test 3: Try with stored credentials
        print("3. Testing with stored credentials...")
        try:
            from secret_manager import SecretManager

            sm = SecretManager()
            creds = sm.get_credentials("192.168.178.1")

            if creds:
                fc = FritzConnection(
                    address="192.168.178.1",
                    user=creds["username"],
                    password=creds["password"],
                )
                info = fc.call_action("DeviceInfo", "GetInfo")
                print("✅ Stored credentials work!")
                print(f"   Model: {info.get('ModelName', 'Unknown')}")
                return True
            else:
                print("❌ No stored credentials found")
        except Exception as e:
            print(f"❌ Stored credentials failed: {str(e)}")

        return False

    except ImportError:
        print("❌ fritzconnection not available")
        return False


def print_detailed_instructions():
    """Print detailed TR-064 setup instructions"""
    print("\n📋 DETAILED TR-064 SETUP INSTRUCTIONS:")
    print("=" * 50)
    print()
    print("1️⃣  Open Fritz!Box Web Interface:")
    print("   • Go to http://fritz.box or http://192.168.178.1")
    print("   • Login with your admin password")
    print()
    print("2️⃣  Enable TR-064 Access:")
    print("   • Navigate to: Home Network → Network → Network Settings")
    print("   • Scroll down to 'Access for applications'")
    print("   • CHECK 'Allow access for applications'")
    print("   • Optional: CHECK 'Allow access from the Internet'")
    print("   • Click 'Apply' or 'OK'")
    print()
    print("3️⃣  Configure User Permissions:")
    print("   • Navigate to: System → FRITZ!Box Users")
    print("   • Select your admin user or create a new one")
    print("   • Ensure the user has 'TR-064' permissions")
    print("   • For admin user: 'All permissions' should include TR-064")
    print("   • Click 'Apply' or 'OK'")
    print()
    print("4️⃣  Important Notes:")
    print("   • TR-064 uses port 49000 (must be open)")
    print("   • The password is the SAME as your web interface login")
    print("   • Username is usually 'admin' unless you created a different user")
    print("   • Changes may require a Fritz!Box restart")
    print()
    print("5️⃣  Common Issues:")
    print("   • 'Allow access for applications' is NOT checked")
    print("   • User doesn't have TR-064 permissions")
    print("   • Using WiFi password instead of admin password")
    print("   • Firewall blocking port 49000")
    print("   • Fritz!Box needs restart after changes")


def open_fritzbox_interface():
    """Open Fritz!Box web interface"""
    print("🌐 Opening Fritz!Box web interface...")
    webbrowser.open("http://fritz.box")
    print("✅ Opened in browser")


def test_after_setup():
    """Test connection after user makes changes"""
    print("\n🧪 Ready to test your changes?")
    print("After completing the setup above, press Enter to test...")
    input()

    print("\n🔄 Testing TR-064 connection...")
    if check_tr064_status():
        print("🎉 SUCCESS! TR-064 is working!")
        print("\nNext steps:")
        print("• Run: python fritzbox_api_examples.py --interactive")
        print("• Start MCP server: python fritzbox_mcp_server.py")
        return True
    else:
        print("❌ Still not working. Please double-check:")
        print("• TR-064 is enabled")
        print("• User has TR-064 permissions")
        print("• Using correct admin password (not WiFi password)")
        print("• Try restarting Fritz!Box")
        return False


def main():
    print_header()

    # Check current status
    if check_tr064_status():
        print("\n🎉 TR-064 is already working!")
        return

    # Show detailed instructions
    print_detailed_instructions()

    # Open interface
    open_fritzbox_interface()

    # Test after setup
    test_after_setup()


if __name__ == "__main__":
    main()
