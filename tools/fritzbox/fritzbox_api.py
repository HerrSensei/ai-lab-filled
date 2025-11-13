#!/usr/bin/env python3
"""
Fritz!Box API Control Tool
Provides comprehensive control over Fritz!Box router via TR-064 API
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

try:
    from fritzconnection import FritzConnection
    from fritzconnection.core.exceptions import (
        FritzConnectionException,
        FritzSecurityError,
    )
except ImportError:
    print(
        "fritzconnection library not found. Install with: pip install fritzconnection"
    )
    exit(1)

import structlog

logger = structlog.get_logger(__name__)


class FritzService(Enum):
    """Fritz!Box TR-064 service categories"""

    DEVICE_INFO = "DeviceInfo"
    WAN_IP = "WANIPConnection"
    WAN_PPP = "WANPPPConnection"
    LAN_HOSTS = "LanDeviceHosts"
    WLAN_CONFIG = "WLANConfiguration"
    LAN_CONFIG = "LANHostConfigManagement"
    DEVICE_CONFIG = "DeviceConfig"


@dataclass
class FritzDevice:
    """Represents a network device connected to Fritz!Box"""

    ip_address: str
    mac_address: str
    hostname: str
    device_type: str
    active: bool = True


@dataclass
class FritzPortForward:
    """Represents a port forwarding rule"""

    enabled: bool
    external_port: int
    internal_port: int
    internal_ip: str
    protocol: str  # TCP/UDP
    description: str = ""


class FritzBoxAPI:
    """Main Fritz!Box API controller"""

    def __init__(
        self, host: str = "192.168.178.1", user: str = "admin", password: str = ""
    ):
        self.host = host
        self.user = user
        self.password = password
        self.fc: FritzConnection | None = None
        self._connected = False

    async def connect(self) -> bool:
        """Establish connection to Fritz!Box"""
        try:
            self.fc = FritzConnection(
                address=self.host,
                user=self.user,
                password=self.password,
                use_cache=True,
            )

            # Test connection
            info = await self.get_device_info()
            if info:
                self._connected = True
                logger.info(
                    "Connected to Fritz!Box",
                    host=self.host,
                    model=info.get("ModelName", "Unknown"),
                )
                return True

        except FritzSecurityError as e:
            logger.error("Authentication failed", error=str(e))
        except FritzConnectionException as e:
            logger.error("Connection failed", error=str(e))
        except Exception as e:
            logger.error("Unexpected error", error=str(e))

        return False

    async def get_device_info(self) -> dict[str, Any]:
        """Get basic device information"""
        if not self.fc:
            return {}

        try:
            return self.fc.call_action(FritzService.DEVICE_INFO.value, "GetInfo")
        except Exception as e:
            logger.error("Failed to get device info", error=str(e))
            return {}

    async def get_external_ip(self) -> str:
        """Get external IP address"""
        if not self.fc:
            return ""

        try:
            # Try WANIPConnection first
            result = self.fc.call_action(
                FritzService.WAN_IP.value, "GetExternalIPAddress"
            )
            return result.get("NewExternalIPAddress", "")
        except:
            try:
                # Fallback to WANPPPConnection
                result = self.fc.call_action(
                    FritzService.WAN_PPP.value, "GetExternalIPAddress"
                )
                return result.get("NewExternalIPAddress", "")
            except Exception as e:
                logger.error("Failed to get external IP", error=str(e))
                return ""

    async def get_connected_devices(self) -> list[FritzDevice]:
        """Get list of all connected devices"""
        if not self.fc:
            return []

        devices = []
        try:
            # Get host info
            host_num = self.fc.call_action(
                FritzService.LAN_HOSTS.value, "GetHostNumberOfEntries"
            )
            num_hosts = host_num.get("NewHostNumberOfEntries", 0)

            for i in range(num_hosts):
                try:
                    host_info = self.fc.call_action(
                        FritzService.LAN_HOSTS.value, "GetGenericHostEntry", NewIndex=i
                    )

                    device = FritzDevice(
                        ip_address=host_info.get("NewIPAddress", ""),
                        mac_address=host_info.get("NewMACAddress", ""),
                        hostname=host_info.get("NewHostName", ""),
                        device_type=host_info.get("NewInterfaceType", "Unknown"),
                        active=host_info.get("NewActive", False),
                    )
                    devices.append(device)

                except Exception as e:
                    logger.warning(f"Failed to get device {i}", error=str(e))
                    continue

        except Exception as e:
            logger.error("Failed to get connected devices", error=str(e))

        return devices

    async def get_wifi_networks(self) -> list[dict[str, Any]]:
        """Get WiFi network information"""
        if not self.fc:
            return []

        networks = []
        try:
            # Check multiple WLAN configurations (2.4GHz, 5GHz, etc.)
            for wlan_id in range(1, 4):  # Usually 1-3 WLAN configs
                try:
                    info = self.fc.call_action(
                        f"{FritzService.WLAN_CONFIG.value}{wlan_id}", "GetInfo"
                    )
                    if info.get("NewEnable", False):
                        networks.append(
                            {
                                "id": wlan_id,
                                "ssid": info.get("NewSSID", ""),
                                "enabled": info.get("NewEnable", False),
                                "channel": info.get("NewChannel", 0),
                                "status": info.get("NewStatus", ""),
                                "mac_address": info.get("NewBSSID", ""),
                            }
                        )
                except:
                    continue

        except Exception as e:
            logger.error("Failed to get WiFi networks", error=str(e))

        return networks

    async def get_port_forwards(self) -> list[FritzPortForward]:
        """Get current port forwarding rules"""
        if not self.fc:
            return []

        forwards = []
        try:
            # Get number of forwarded entries
            port_mapping_num = self.fc.call_action(
                FritzService.WAN_IP.value, "GetPortMappingNumberOfEntries"
            )
            num_mappings = port_mapping_num.get("NewPortMappingNumberOfEntries", 0)

            for i in range(num_mappings):
                try:
                    mapping = self.fc.call_action(
                        FritzService.WAN_IP.value,
                        "GetGenericPortMappingEntry",
                        NewPortMappingIndex=i,
                    )

                    forward = FritzPortForward(
                        enabled=mapping.get("NewEnabled", False),
                        external_port=mapping.get("NewExternalPort", 0),
                        internal_port=mapping.get("NewInternalPort", 0),
                        internal_ip=mapping.get("NewInternalClient", ""),
                        protocol=mapping.get("NewProtocol", ""),
                        description=mapping.get("NewPortMappingDescription", ""),
                    )
                    forwards.append(forward)

                except Exception as e:
                    logger.warning(f"Failed to get port mapping {i}", error=str(e))
                    continue

        except Exception as e:
            logger.error("Failed to get port forwards", error=str(e))

        return forwards

    async def wake_device(self, mac_address: str) -> bool:
        """Send Wake-on-LAN packet to device"""
        if not self.fc:
            return False

        try:
            self.fc.call_action(
                FritzService.LAN_HOSTS.value,
                "WakeOnLANByMACAddress",
                NewMACAddress=mac_address,
            )
            logger.info("Wake-on-LAN sent", mac=mac_address)
            return True
        except Exception as e:
            logger.error("Failed to send Wake-on-LAN", mac=mac_address, error=str(e))
            return False

    async def reboot_router(self) -> bool:
        """Reboot the Fritz!Box"""
        if not self.fc:
            return False

        try:
            self.fc.call_action(FritzService.DEVICE_CONFIG.value, "Reboot")
            logger.info("Fritz!Box reboot initiated")
            return True
        except Exception as e:
            logger.error("Failed to reboot router", error=str(e))
            return False

    async def get_connection_stats(self) -> dict[str, Any]:
        """Get WAN connection statistics"""
        if not self.fc:
            return {}

        stats = {}
        try:
            # Try WANIPConnection first
            try:
                stats = self.fc.call_action(
                    FritzService.WAN_IP.value, "GetTotalBytesReceived"
                )
                stats.update(
                    self.fc.call_action(FritzService.WAN_IP.value, "GetTotalBytesSent")
                )
            except:
                # Fallback to WANPPPConnection
                stats = self.fc.call_action(
                    FritzService.WAN_PPP.value, "GetTotalBytesReceived"
                )
                stats.update(
                    self.fc.call_action(FritzService.WAN_PPP.value, "GetTotalBytesSent")
                )

        except Exception as e:
            logger.error("Failed to get connection stats", error=str(e))

        return stats


async def main():
    """Example usage of Fritz!Box API"""
    logging.basicConfig(level=logging.INFO)

    # Initialize API client
    fritz = FritzBoxAPI(
        host="192.168.178.1",
        user="admin",  # Replace with actual username
        password="your_password",  # Replace with actual password
    )

    # Connect to router
    if not await fritz.connect():
        print("Failed to connect to Fritz!Box")
        return

    # Get device info
    device_info = await fritz.get_device_info()
    print(f"Router Model: {device_info.get('ModelName', 'Unknown')}")
    print(f"Firmware: {device_info.get('SoftwareVersion', 'Unknown')}")

    # Get external IP
    external_ip = await fritz.get_external_ip()
    print(f"External IP: {external_ip}")

    # Get connected devices
    devices = await fritz.get_connected_devices()
    print(f"\nConnected Devices ({len(devices)}):")
    for device in devices:
        status = "Active" if device.active else "Inactive"
        print(f"  {device.hostname} ({device.ip_address}) - {status}")

    # Get WiFi networks
    wifi_networks = await fritz.get_wifi_networks()
    print(f"\nWiFi Networks ({len(wifi_networks)}):")
    for network in wifi_networks:
        print(f"  {network['ssid']} - Channel {network['channel']}")

    # Get port forwards
    port_forwards = await fritz.get_port_forwards()
    print(f"\nPort Forwards ({len(port_forwards)}):")
    for forward in port_forwards:
        if forward.enabled:
            print(
                f"  {forward.external_port} -> {forward.internal_ip}:{forward.internal_port} ({forward.protocol})"
            )


if __name__ == "__main__":
    asyncio.run(main())
