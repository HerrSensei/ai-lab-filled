#!/usr/bin/env python3
"""
Fritz!Box API Examples
Demonstrates various Fritz!Box API capabilities
"""

import asyncio
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fritzbox_api import FritzBoxAPI
from secret_manager import SecretManager


async def demo_basic_info():
    """Demo: Get basic router information"""
    print("🔍 Getting basic Fritz!Box information...")

    # Use secret manager to get credentials
    secret_manager = SecretManager()
    creds = secret_manager.get_credentials("192.168.178.1")

    if not creds:
        print(
            "❌ No credentials found. Please store them first using secret_manager.py"
        )
        return

    fritz = FritzBoxAPI(
        host="192.168.178.1", user=creds["username"], password=creds["password"]
    )

    if not await fritz.connect():
        print("❌ Failed to connect to Fritz!Box")
        return

    # Get device info
    device_info = await fritz.get_device_info()
    print(f"✅ Router Model: {device_info.get('ModelName', 'Unknown')}")
    print(f"✅ Firmware Version: {device_info.get('SoftwareVersion', 'Unknown')}")
    print(f"✅ Serial Number: {device_info.get('SerialNumber', 'Unknown')}")

    # Get external IP
    external_ip = await fritz.get_external_ip()
    print(f"✅ External IP: {external_ip}")

    print()


async def demo_device_management():
    """Demo: Device discovery and management"""
    print("📱 Discovering connected devices...")

    secret_manager = SecretManager()
    creds = secret_manager.get_credentials("192.168.178.1")

    if not creds:
        print("❌ No credentials found")
        return

    fritz = FritzBoxAPI(
        host="192.168.178.1", user=creds["username"], password=creds["password"]
    )

    if not await fritz.connect():
        print("❌ Failed to connect")
        return

    devices = await fritz.get_connected_devices()
    print(f"✅ Found {len(devices)} connected devices:")

    for i, device in enumerate(devices, 1):
        status = "🟢 Active" if device.active else "🔴 Inactive"
        print(f"  {i}. {device.hostname} ({device.ip_address}) - {status}")
        print(f"     MAC: {device.mac_address} | Type: {device.device_type}")

    print()


async def demo_wifi_management():
    """Demo: WiFi network information"""
    print("📶 Getting WiFi network information...")

    secret_manager = SecretManager()
    creds = secret_manager.get_credentials("192.168.178.1")

    if not creds:
        print("❌ No credentials found")
        return

    fritz = FritzBoxAPI(
        host="192.168.178.1", user=creds["username"], password=creds["password"]
    )

    if not await fritz.connect():
        print("❌ Failed to connect")
        return

    networks = await fritz.get_wifi_networks()
    print(f"✅ Found {len(networks)} WiFi networks:")

    for i, network in enumerate(networks, 1):
        status = "🟢 Enabled" if network["enabled"] else "🔴 Disabled"
        print(f"  {i}. {network['ssid']} - {status}")
        print(f"     Channel: {network['channel']} | BSSID: {network['mac_address']}")

    print()


async def demo_port_forwarding():
    """Demo: Port forwarding management"""
    print("🔌 Getting port forwarding rules...")

    secret_manager = SecretManager()
    creds = secret_manager.get_credentials("192.168.178.1")

    if not creds:
        print("❌ No credentials found")
        return

    fritz = FritzBoxAPI(
        host="192.168.178.1", user=creds["username"], password=creds["password"]
    )

    if not await fritz.connect():
        print("❌ Failed to connect")
        return

    forwards = await fritz.get_port_forwards()
    enabled_forwards = [f for f in forwards if f.enabled]

    print(f"✅ Found {len(enabled_forwards)} active port forwards:")

    for i, forward in enumerate(enabled_forwards, 1):
        print(
            f"  {i}. {forward.external_port} -> {forward.internal_ip}:{forward.internal_port} ({forward.protocol})"
        )
        if forward.description:
            print(f"     Description: {forward.description}")

    print()


async def demo_wake_on_lan():
    """Demo: Wake-on-LAN functionality"""
    print("😴 Wake-on-LAN Demo")

    secret_manager = SecretManager()
    creds = secret_manager.get_credentials("192.168.178.1")

    if not creds:
        print("❌ No credentials found")
        return

    fritz = FritzBoxAPI(
        host="192.168.178.1", user=creds["username"], password=creds["password"]
    )

    if not await fritz.connect():
        print("❌ Failed to connect")
        return

    # Get devices to show available targets
    devices = await fritz.get_connected_devices()
    inactive_devices = [d for d in devices if not d.active]

    if not inactive_devices:
        print("ℹ️  All devices are currently active")
        return

    print("Available devices for Wake-on-LAN:")
    for i, device in enumerate(inactive_devices, 1):
        print(f"  {i}. {device.hostname} ({device.mac_address})")

    # For demo purposes, we'll just show the capability
    print("\n💡 To wake a device, use: await fritz.wake_device('MAC_ADDRESS')")
    print()


async def demo_connection_stats():
    """Demo: Connection statistics"""
    print("📊 Getting connection statistics...")

    secret_manager = SecretManager()
    creds = secret_manager.get_credentials("192.168.178.1")

    if not creds:
        print("❌ No credentials found")
        return

    fritz = FritzBoxAPI(
        host="192.168.178.1", user=creds["username"], password=creds["password"]
    )

    if not await fritz.connect():
        print("❌ Failed to connect")
        return

    stats = await fritz.get_connection_stats()

    if stats:
        print("✅ Connection Statistics:")
        if "NewTotalBytesReceived" in stats:
            received_mb = int(stats["NewTotalBytesReceived"]) / (1024 * 1024)
            print(f"  Download: {received_mb:.2f} MB")
        if "NewTotalBytesSent" in stats:
            sent_mb = int(stats["NewTotalBytesSent"]) / (1024 * 1024)
            print(f"  Upload: {sent_mb:.2f} MB")
    else:
        print("⚠️  Statistics not available")

    print()


async def interactive_demo():
    """Interactive demo menu"""
    print("🎯 Fritz!Box API Interactive Demo")
    print("=" * 40)

    while True:
        print("\nAvailable demos:")
        print("1. Basic router information")
        print("2. Device discovery")
        print("3. WiFi networks")
        print("4. Port forwarding")
        print("5. Wake-on-LAN")
        print("6. Connection statistics")
        print("7. Run all demos")
        print("8. Exit")

        choice = input("\nSelect demo (1-8): ").strip()

        if choice == "1":
            await demo_basic_info()
        elif choice == "2":
            await demo_device_management()
        elif choice == "3":
            await demo_wifi_management()
        elif choice == "4":
            await demo_port_forwarding()
        elif choice == "5":
            await demo_wake_on_lan()
        elif choice == "6":
            await demo_connection_stats()
        elif choice == "7":
            print("\n🚀 Running all demos...\n")
            await demo_basic_info()
            await demo_device_management()
            await demo_wifi_management()
            await demo_port_forwarding()
            await demo_wake_on_lan()
            await demo_connection_stats()
            print("✅ All demos completed!")
        elif choice == "8":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


async def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        await interactive_demo()
    else:
        print("🎯 Fritz!Box API Examples")
        print("=" * 30)
        print("Use --interactive for demo menu")
        print()

        # Run basic demo
        await demo_basic_info()
        await demo_device_management()
        await demo_wifi_management()
        await demo_port_forwarding()


if __name__ == "__main__":
    asyncio.run(main())
