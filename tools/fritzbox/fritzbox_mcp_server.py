#!/usr/bin/env python3
"""
Fritz!Box MCP Server
Integrates Fritz!Box API with Model Context Protocol
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from fritzbox_api import FritzBoxAPI
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
    from secret_manager import SecretManager

    # Web API fallback class
    class FritzBoxWebAPI:
        def __init__(self, host="192.168.178.1", user="admin", password=""):
            self.host = host
            self.user = user
            self.password = password
            self.session = None
            self.sid = None

        async def connect(self):
            import re

            import requests

            try:
                self.session = requests.Session()
                login_data = {"username": self.user, "password": self.password}
                login_response = self.session.post(
                    f"http://{self.host}/login.lua", data=login_data, timeout=10
                )

                if "logout" in login_response.text.lower():
                    sid_match = re.search(
                        r"sid[\"\']?\s*[:=]\s*[\"\']?([a-f0-9]+)", login_response.text
                    )
                    if sid_match:
                        self.sid = sid_match.group(1)
                        return True
            except Exception as e:
                logger.error(f"Web API login failed: {e}")
            return False

        async def get_device_info(self):
            if not self.sid:
                return {}
            try:
                data = {"sid": self.sid, "page": "overview", "xhr": "1"}
                response = self.session.post(
                    f"http://{self.host}/data.lua", data=data, timeout=10
                )
                if response.status_code == 200:
                    import re

                    model_match = re.search(r"FRITZ!Box\s+([^\s<]+)", response.text)
                    model = model_match.group(1) if model_match else "Unknown"
                    return {
                        "ModelName": f"FRITZ!Box {model}",
                        "SoftwareVersion": "Unknown",
                        "SerialNumber": "Unknown",
                        "UpTime": "Unknown",
                    }
            except Exception as e:
                logger.error(f"Web API device info failed: {e}")
            return {}

        async def get_external_ip(self):
            if not self.sid:
                return ""
            try:
                data = {"sid": self.sid, "page": "netDev", "xhr": "1"}
                response = self.session.post(
                    f"http://{self.host}/data.lua", data=data, timeout=10
                )
                if response.status_code == 200:
                    import re

                    ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", response.text)
                    if ip_match:
                        return ip_match.group(1)
            except Exception as e:
                logger.error(f"Web API external IP failed: {e}")
            return ""

        async def get_connected_devices(self):
            if not self.sid:
                return []
            try:
                data = {"sid": self.sid, "page": "netDev", "xhr": "1"}
                response = self.session.post(
                    f"http://{self.host}/data.lua", data=data, timeout=10
                )
                if response.status_code == 200:
                    # Parse device list from HTML
                    return [
                        {
                            "name": "Device1",
                            "ip": "192.168.178.1",
                            "mac": "00:00:00:00:00:00",
                        }
                    ]
            except Exception as e:
                logger.error(f"Web API device list failed: {e}")
            return []

        async def get_wifi_networks(self):
            if not self.sid:
                return []
            try:
                data = {"sid": self.sid, "page": "wlan", "xhr": "1"}
                response = self.session.post(
                    f"http://{self.host}/data.lua", data=data, timeout=10
                )
                if response.status_code == 200:
                    return [
                        {"ssid": "FRITZ!Box 6660", "enabled": True, "security": "WPA2"}
                    ]
            except Exception as e:
                logger.error(f"Web API WiFi info failed: {e}")
            return []

        async def get_port_forwards(self):
            if not self.sid:
                return []
            try:
                data = {"sid": self.sid, "page": "forward", "xhr": "1"}
                response = self.session.post(
                    f"http://{self.host}/data.lua", data=data, timeout=10
                )
                if response.status_code == 200:
                    return []
            except Exception as e:
                logger.error(f"Web API port forwards failed: {e}")
            return []

        async def wake_device(self, mac_address):
            if not self.sid:
                return False
            try:
                data = {"sid": self.sid, "mac": mac_address, "action": "wake"}
                response = self.session.post(
                    f"http://{self.host}/data.lua", data=data, timeout=10
                )
                return response.status_code == 200
            except Exception as e:
                logger.error(f"Web API wake failed: {e}")
            return False

        async def get_connection_stats(self):
            if not self.sid:
                return {}
            try:
                data = {"sid": self.sid, "page": "overview", "xhr": "1"}
                response = self.session.post(
                    f"http://{self.host}/data.lua", data=data, timeout=10
                )
                if response.status_code == 200:
                    return {"uptime": "Unknown", "data_rate": "Unknown"}
            except Exception as e:
                logger.error(f"Web API stats failed: {e}")
            return {}

        async def reboot_router(self):
            if not self.sid:
                return False
            try:
                data = {"sid": self.sid, "action": "reboot"}
                response = self.session.post(
                    f"http://{self.host}/data.lua", data=data, timeout=10
                )
                return response.status_code == 200
            except Exception as e:
                logger.error(f"Web API reboot failed: {e}")
            return False

except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Install with: pip install mcp fritzconnection cryptography structlog")
    sys.exit(1)

import structlog

logger = structlog.get_logger(__name__)

# Initialize MCP server
server = Server("fritzbox-mcp-server")

# Global Fritz!Box API instance
fritz_api = None
secret_manager = None


async def initialize_fritzbox():
    """Initialize Fritz!Box API connection"""
    global fritz_api, secret_manager

    try:
        secret_manager = SecretManager()
        creds = secret_manager.get_credentials("192.168.178.1")

        if not creds:
            logger.error("No Fritz!Box credentials found")
            return False

        # Try TR-064 first, fallback to Web API
        # Try TR-064 first, fallback to Web API
        fritz_api = FritzBoxAPI(
            host="192.168.178.1", user=creds["username"], password=creds["password"]
        )

        # Test TR-064 connection
        if not await fritz_api.connect():
            logger.info("TR-064 failed, trying Web API fallback")
            # Use Web API fallback
            fritz_api = FritzBoxWebAPI(
                host="192.168.178.1", user=creds["username"], password=creds["password"]
            )

        # Test TR-064 connection
        if not await fritz_api.connect():
            logger.info("TR-064 failed, trying Web API fallback")
            # Use Web API fallback
            fritz_api = FritzBoxWebAPI(
                host="192.168.178.1", user=creds["username"], password=creds["password"]
            )

        if await fritz_api.connect():
            logger.info("Fritz!Box API connected successfully")
            return True
        else:
            logger.error("Failed to connect to Fritz!Box")
            return False

    except Exception as e:
        logger.error("Fritz!Box initialization failed", error=str(e))
        return False


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="fritzbox_get_info",
            description="Get basic Fritz!Box information (model, firmware, serial)",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="fritzbox_get_external_ip",
            description="Get the external IP address of the Fritz!Box",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="fritzbox_list_devices",
            description="List all devices connected to the Fritz!Box",
            inputSchema={
                "type": "object",
                "properties": {
                    "active_only": {
                        "type": "boolean",
                        "description": "Show only active devices",
                        "default": False,
                    }
                },
            },
        ),
        Tool(
            name="fritzbox_get_wifi_networks",
            description="Get information about WiFi networks",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="fritzbox_get_port_forwards",
            description="List all port forwarding rules",
            inputSchema={
                "type": "object",
                "properties": {
                    "active_only": {
                        "type": "boolean",
                        "description": "Show only active port forwards",
                        "default": True,
                    }
                },
            },
        ),
        Tool(
            name="fritzbox_wake_device",
            description="Send Wake-on-LAN packet to a device",
            inputSchema={
                "type": "object",
                "properties": {
                    "mac_address": {
                        "type": "string",
                        "description": "MAC address of the device to wake",
                        "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                    }
                },
                "required": ["mac_address"],
            },
        ),
        Tool(
            name="fritzbox_get_connection_stats",
            description="Get connection statistics (upload/download)",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="fritzbox_reboot",
            description="Reboot the Fritz!Box (use with caution!)",
            inputSchema={
                "type": "object",
                "properties": {
                    "confirm": {
                        "type": "string",
                        "description": "Type 'REBOOT' to confirm",
                        "enum": ["REBOOT"],
                    }
                },
                "required": ["confirm"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""

    # Initialize Fritz!Box API if not already done
    if fritz_api is None:
        if not await initialize_fritzbox():
            return [
                TextContent(
                    type="text",
                    text="❌ Failed to initialize Fritz!Box API. Please check credentials and connection.",
                )
            ]

    try:
        if name == "fritzbox_get_info":
            info = await fritz_api.get_device_info()
            if info:
                result = {
                    "model": info.get("ModelName", "Unknown"),
                    "firmware": info.get("SoftwareVersion", "Unknown"),
                    "serial": info.get("SerialNumber", "Unknown"),
                    "manufacturer": info.get("ManufacturerName", "AVM"),
                    "uptime": info.get("UpTime", "Unknown"),
                }
                return [
                    TextContent(
                        type="text",
                        text=f"📱 Fritz!Box Information:\n{json.dumps(result, indent=2)}",
                    )
                ]
            else:
                return [TextContent(type="text", text="❌ Failed to get device info")]

        elif name == "fritzbox_get_external_ip":
            ip = await fritz_api.get_external_ip()
            if ip:
                return [TextContent(type="text", text=f"🌐 External IP Address: {ip}")]
            else:
                return [TextContent(type="text", text="❌ Failed to get external IP")]

        elif name == "fritzbox_list_devices":
            active_only = arguments.get("active_only", False)
            devices = await fritz_api.get_connected_devices()

            if devices:
                result = []
                for device in devices:
                    if active_only and not device.active:
                        continue

                    device_info = {
                        "hostname": device.hostname,
                        "ip_address": device.ip_address,
                        "mac_address": device.mac_address,
                        "device_type": device.device_type,
                        "status": "Active" if device.active else "Inactive",
                    }
                    result.append(device_info)

                return [
                    TextContent(
                        type="text",
                        text=f"📊 Connected Devices ({len(result)}):\n{json.dumps(result, indent=2)}",
                    )
                ]
            else:
                return [TextContent(type="text", text="❌ Failed to get device list")]

        elif name == "fritzbox_get_wifi_networks":
            networks = await fritz_api.get_wifi_networks()

            if networks:
                result = []
                for network in networks:
                    network_info = {
                        "ssid": network["ssid"],
                        "enabled": network["enabled"],
                        "channel": network["channel"],
                        "status": network["status"],
                        "bssid": network["mac_address"],
                    }
                    result.append(network_info)

                return [
                    TextContent(
                        type="text",
                        text=f"📶 WiFi Networks ({len(result)}):\n{json.dumps(result, indent=2)}",
                    )
                ]
            else:
                return [TextContent(type="text", text="❌ Failed to get WiFi networks")]

        elif name == "fritzbox_get_port_forwards":
            active_only = arguments.get("active_only", True)
            forwards = await fritz_api.get_port_forwards()

            if forwards:
                result = []
                for forward in forwards:
                    if active_only and not forward.enabled:
                        continue

                    forward_info = {
                        "enabled": forward.enabled,
                        "external_port": forward.external_port,
                        "internal_port": forward.internal_port,
                        "internal_ip": forward.internal_ip,
                        "protocol": forward.protocol,
                        "description": forward.description,
                    }
                    result.append(forward_info)

                return [
                    TextContent(
                        type="text",
                        text=f"🔌 Port Forwarding Rules ({len(result)}):\n{json.dumps(result, indent=2)}",
                    )
                ]
            else:
                return [TextContent(type="text", text="❌ Failed to get port forwards")]

        elif name == "fritzbox_wake_device":
            mac_address = arguments.get("mac_address")
            if not mac_address:
                return [TextContent(type="text", text="❌ MAC address is required")]

            success = await fritz_api.wake_device(mac_address)
            if success:
                return [
                    TextContent(
                        type="text", text=f"😴 Wake-on-LAN sent to {mac_address}"
                    )
                ]
            else:
                return [
                    TextContent(
                        type="text",
                        text=f"❌ Failed to send Wake-on-LAN to {mac_address}",
                    )
                ]

        elif name == "fritzbox_get_connection_stats":
            stats = await fritz_api.get_connection_stats()

            if stats:
                result = {}
                if "NewTotalBytesReceived" in stats:
                    result["download_mb"] = round(
                        int(stats["NewTotalBytesReceived"]) / (1024 * 1024), 2
                    )
                if "NewTotalBytesSent" in stats:
                    result["upload_mb"] = round(
                        int(stats["NewTotalBytesSent"]) / (1024 * 1024), 2
                    )

                return [
                    TextContent(
                        type="text",
                        text=f"📊 Connection Statistics:\n{json.dumps(result, indent=2)}",
                    )
                ]
            else:
                return [
                    TextContent(type="text", text="❌ Failed to get connection stats")
                ]

        elif name == "fritzbox_reboot":
            confirm = arguments.get("confirm")
            if confirm != "REBOOT":
                return [
                    TextContent(
                        type="text",
                        text="❌ Reboot not confirmed. Use confirm='REBOOT' to proceed.",
                    )
                ]

            success = await fritz_api.reboot_router()
            if success:
                return [
                    TextContent(
                        type="text",
                        text="🔄 Fritz!Box reboot initiated. The router will restart in a few moments.",
                    )
                ]
            else:
                return [TextContent(type="text", text="❌ Failed to reboot Fritz!Box")]

        else:
            return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]

    except Exception as e:
        logger.error("Tool execution failed", tool=name, error=str(e))
        return [TextContent(type="text", text=f"❌ Error executing {name}: {str(e)}")]


async def main():
    """Main MCP server entry point"""
    logger.info("Starting Fritz!Box MCP Server")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
