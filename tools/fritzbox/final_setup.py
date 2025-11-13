#!/usr/bin/env python3
"""
Final Fritz!Box Setup
Simple credential setup after TR-064 is enabled
"""


def main():
    print("🔧 Final Fritz!Box Setup")
    print("=" * 30)
    print()
    print("✅ TR-064 port 49000 is open")
    print("✅ TR-064 is enabled")
    print("❌ Just need correct admin credentials")
    print()

    print("📝 Please enter your Fritz!Box ADMIN credentials:")
    print("(This is the SAME password you use to login to fritz.box)")
    print()

    try:
        import getpass

        from secret_manager import SecretManager

        sm = SecretManager()

        username = input("Username (usually 'admin'): ").strip()
        if not username:
            username = "admin"

        password = getpass.getpass("Admin Password: ")

        if not password:
            print("❌ Password cannot be empty")
            return

        print("\n📝 Storing credentials:")
        print(f"   Username: {username}")
        print(f"   Password: {'*' * len(password)}")

        if sm.store_credentials("192.168.178.1", username, password):
            print("✅ Credentials stored successfully!")

            # Test immediately
            print("\n🧪 Testing credentials...")
            import asyncio

            from fritzbox_api import FritzBoxAPI

            async def test():
                fritz = FritzBoxAPI(
                    host="192.168.178.1", user=username, password=password
                )

                if await fritz.connect():
                    print("✅ SUCCESS! Connection works!")

                    # Get device info
                    device_info = await fritz.get_device_info()
                    if device_info:
                        print(
                            f"📱 Router Model: {device_info.get('ModelName', 'Unknown')}"
                        )
                        print(
                            f"🔧 Firmware: {device_info.get('SoftwareVersion', 'Unknown')}"
                        )

                    # Get external IP
                    external_ip = await fritz.get_external_ip()
                    print(f"🌐 External IP: {external_ip}")

                    # Get connected devices
                    devices = await fritz.get_connected_devices()
                    print(f"📊 Connected devices: {len(devices)}")

                    print("\n🎉 Fritz!Box setup is COMPLETE!")
                    print("\nNext steps:")
                    print("• Run: python fritzbox_api_examples.py --interactive")
                    print("• Start MCP server: python fritzbox_mcp_server.py")
                    print("• Check CONNECTED_SYSTEMS.md for integration info")

                    return True
                else:
                    print("❌ Credentials don't work")
                    print("\n💡 Please check:")
                    print("• Using admin password (not WiFi password)")
                    print("• TR-064 permissions are enabled for user")
                    print("• Try restarting Fritz!Box after changes")
                    return False

            result = asyncio.run(test())

            if not result:
                print("\n⚙️  To try different credentials:")
                print('python -c "')
                print("from secret_manager import SecretManager")
                print("import getpass")
                print("sm = SecretManager()")
                print("username = input('Username: ').strip()")
                print("password = getpass.getpass('Password: ')")
                print("sm.store_credentials('192.168.178.1', username, password)")
                print('"')
        else:
            print("❌ Failed to store credentials")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
