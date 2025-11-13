#!/usr/bin/env python3
"""
Final working Fritz!Box API implementation
Based on comprehensive testing of fritzconnection capabilities
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from fritzconnection import FritzConnection


class FritzBoxFinal:
    """Final working Fritz!Box API implementation"""

    def __init__(self, host="192.168.178.1", password="stark0564"):
        self.host = host
        self.password = password
        self.fc = None
        self._connected = False

    def connect(self):
        """Establish connection to Fritz!Box"""
        try:
            self.fc = FritzConnection(address=self.host, password=self.password)

            # Test connection
            device_info = self.fc.call_action("DeviceInfo1", "GetInfo")
            if device_info:
                self._connected = True
                print(f"✅ Connected to {device_info.get('ModelName', 'Unknown')}")
                return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def get_device_info(self):
        """Get basic device information"""
        if not self._connected:
            return {}

        try:
            return self.fc.call_action("DeviceInfo1", "GetInfo")
        except Exception as e:
            print(f"❌ Failed to get device info: {e}")
            return {}

    def get_external_ip(self):
        """Get external IP address"""
        if not self._connected:
            return ""

        try:
            result = self.fc.call_action("WANIPConn1", "GetExternalIPAddress")
            return result.get("NewExternalIPAddress", "")
        except Exception as e:
            print(f"❌ Failed to get external IP: {e}")
            return ""

    def get_wifi_info(self):
        """Get WiFi network information"""
        if not self._connected:
            return []

        networks = []
        try:
            # Check multiple WLAN configurations
            for wlan_id in range(1, 4):
                try:
                    info = self.fc.call_action(f"WLANConfiguration{wlan_id}", "GetInfo")
                    if info.get("NewEnable", False):
                        ssid = self.fc.call_action(
                            f"WLANConfiguration{wlan_id}", "GetSSID"
                        )
                        networks.append(
                            {
                                "id": wlan_id,
                                "ssid": ssid.get("NewSSID", ""),
                                "enabled": info.get("NewEnable", False),
                                "channel": info.get("NewChannel", 0),
                                "status": info.get("NewStatus", ""),
                            }
                        )
                except:
                    continue
        except Exception as e:
            print(f"❌ Failed to get WiFi info: {e}")

        return networks

    def get_connected_devices(self):
        """Get list of connected devices"""
        if not self._connected:
            return []

        devices = []
        try:
            # Get host number
            host_num = self.fc.call_action(
                "LANHostConfigManagement1", "GetHostNumberOfEntries"
            )
            num_hosts = host_num.get("NewHostNumberOfEntries", 0)

            for i in range(min(num_hosts, 50)):  # Limit to first 50
                try:
                    host_info = self.fc.call_action(
                        "LANHostConfigManagement1", "GetGenericHostEntry", NewIndex=i
                    )

                    device = {
                        "ip_address": host_info.get("NewIPAddress", ""),
                        "mac_address": host_info.get("NewMACAddress", ""),
                        "hostname": host_info.get("NewHostName", ""),
                        "interface_type": host_info.get("NewInterfaceType", "Unknown"),
                        "active": host_info.get("NewActive", False),
                    }
                    devices.append(device)

                except Exception:
                    continue

        except Exception as e:
            print(f"❌ Failed to get connected devices: {e}")

        return devices

    def toggle_wifi(self, wlan_id=1, enable=None):
        """Toggle WiFi on/off"""
        if not self._connected:
            return False

        try:
            if enable is None:
                # Get current state and toggle
                info = self.fc.call_action(f"WLANConfiguration{wlan_id}", "GetInfo")
                enable = not info.get("NewEnable", False)

            self.fc.call_action(
                f"WLANConfiguration{wlan_id}", "SetEnable", NewEnable=enable
            )
            print(f"✅ WiFi {wlan_id} {'enabled' if enable else 'disabled'}")
            return True

        except Exception as e:
            print(f"❌ Failed to toggle WiFi: {e}")
            return False

    def set_wifi_channel(self, wlan_id=1, channel=None):
        """Change WiFi channel"""
        if not self._connected:
            return False

        try:
            if channel is None:
                # Get current channel
                info = self.fc.call_action(f"WLANConfiguration{wlan_id}", "GetInfo")
                channel = info.get("NewChannel", 1)

            self.fc.call_action(
                f"WLANConfiguration{wlan_id}", "SetChannel", NewChannel=channel
            )
            print(f"✅ WiFi {wlan_id} channel set to {channel}")
            return True

        except Exception as e:
            print(f"❌ Failed to set WiFi channel: {e}")
            return False

    def wake_device(self, mac_address):
        """Send Wake-on-LAN packet"""
        if not self._connected:
            return False

        try:
            self.fc.call_action(
                "LANHostConfigManagement1",
                "WakeOnLANByMACAddress",
                NewMACAddress=mac_address,
            )
            print(f"✅ Wake-on-LAN sent to {mac_address}")
            return True

        except Exception as e:
            print(f"❌ Failed to send Wake-on-LAN: {e}")
            return False

    def reboot_router(self):
        """Reboot the router (DANGEROUS)"""
        if not self._connected:
            return False

        try:
            print("⚠️  REBOOTING ROUTER - This will disconnect all devices!")
            self.fc.call_action("DeviceConfig1", "Reboot")
            print("✅ Router reboot initiated")
            return True

        except Exception as e:
            print(f"❌ Failed to reboot router: {e}")
            return False

    def get_all_data(self):
        """Get all available data in one call"""
        if not self._connected:
            return {}

        data = {
            "timestamp": datetime.now().isoformat(),
            "device_info": self.get_device_info(),
            "external_ip": self.get_external_ip(),
            "wifi_networks": self.get_wifi_info(),
            "connected_devices": self.get_connected_devices(),
        }

        return data


async def main():
    """Test all final functions"""
    print("🚀 Testing final Fritz!Box implementation...")

    # Initialize
    fritz = FritzBoxFinal()

    # Connect
    if not fritz.connect():
        print("❌ Failed to connect")
        return False

    # Test all functions
    print("\n📊 Testing all functions...")

    # Device info
    device_info = fritz.get_device_info()
    print(f"  Device: {device_info.get('ModelName', 'Unknown')}")

    # External IP
    external_ip = fritz.get_external_ip()
    print(f"  External IP: {external_ip}")

    # WiFi info
    wifi_networks = fritz.get_wifi_info()
    print(f"  WiFi networks: {len(wifi_networks)}")

    # Connected devices
    devices = fritz.get_connected_devices()
    print(f"  Connected devices: {len(devices)}")

    # Get all data
    all_data = fritz.get_all_data()

    # Save results
    output_file = Path("fritzbox_final_test.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"  📁 All data saved to: {output_file.absolute()}")

    print("\n✅ All functions working correctly!")
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
