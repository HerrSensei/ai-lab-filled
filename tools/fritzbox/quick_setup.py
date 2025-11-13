#!/usr/bin/env python3
"""
Quick Fritz!Box Setup Script
Simple manual setup for Fritz!Box API
"""

import subprocess
import webbrowser


def main():
    print("🔧 Quick Fritz!Box Setup")
    print("=" * 30)
    print()

    # Check reachability
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
        else:
            print("❌ Fritz!Box not reachable")
            return
    except:
        print("❌ Could not ping Fritz!Box")
        return

    # Open web interface
    print("🌐 Opening Fritz!Box web interface...")
    webbrowser.open("http://fritz.box")

    print("\n📋 Setup Instructions:")
    print("1. Fritz!Box interface opened in browser")
    print("2. Login with your admin password")
    print("3. Go to: Home Network → Network → Network Settings")
    print("4. Enable 'Allow access for applications'")
    print("5. Go to: System → FRITZ!Box Users")
    print("6. Create user with TR-064 permissions or enable for admin")
    print()

    print("⚙️  After setup, run:")
    print("cd tools/fritzbox")
    print("source venv/bin/activate")
    print('python -c "')
    print("from secret_manager import SecretManager")
    print("import getpass")
    print("sm = SecretManager()")
    print("username = input('Username: ').strip()")
    print("password = getpass.getpass('Password: ')")
    print("sm.store_credentials('192.168.178.1', username, password)")
    print('"')
    print()
    print("Then test with:")
    print("python fritzbox_api_examples.py --interactive")


if __name__ == "__main__":
    main()
