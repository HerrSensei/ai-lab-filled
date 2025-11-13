# Fritz!Box API Tool

Comprehensive Python tool for controlling Fritz!Box routers via TR-064 API.

## Features

### 🔍 Device Discovery
- List all connected devices with IP, MAC, hostname, and status
- Real-time device monitoring
- Device type identification

### 📶 WiFi Management
- View all WiFi networks (2.4GHz, 5GHz, guest networks)
- Network status and configuration
- Channel and signal information

### 🔌 Port Forwarding
- List all port forwarding rules
- Enable/disable port mappings
- Protocol-specific forwarding (TCP/UDP)

### 😴 Device Management
- Wake-on-LAN support
- Device status monitoring
- Network topology information

### 📊 Network Monitoring
- External IP address tracking
- Connection statistics (upload/download)
- Bandwidth monitoring

### 🔐 Security Features
- Encrypted credential storage
- Secure authentication
- Permission-based access control

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install individual packages
pip install fritzconnection cryptography structlog
```

## Quick Start

### 1. Store Credentials
```bash
python secret_manager.py
# Select option 1 to store credentials
# Enter your Fritz!Box IP (usually 192.168.178.1)
# Enter username and password
```

### 2. Basic Usage
```python
import asyncio
from fritzbox_api import FritzBoxAPI

async def main():
    fritz = FritzBoxAPI(
        host="192.168.178.1",
        user="admin",
        password="your_password"
    )

    if await fritz.connect():
        # Get router info
        info = await fritz.get_device_info()
        print(f"Router: {info['ModelName']}")

        # Get external IP
        ip = await fritz.get_external_ip()
        print(f"External IP: {ip}")

        # List devices
        devices = await fritz.get_connected_devices()
        for device in devices:
            print(f"{device.hostname} - {device.ip_address}")

asyncio.run(main())
```

### 3. Run Examples
```bash
# Interactive demo
python fritzbox_api_examples.py --interactive

# Or run all demos
python fritzbox_api_examples.py
```

## API Reference

### FritzBoxAPI Class

#### Connection
- `connect()` - Establish connection to router
- `get_device_info()` - Get router model, firmware, serial number

#### Network Information
- `get_external_ip()` - Get current external IP address
- `get_connection_stats()` - Get upload/download statistics

#### Device Management
- `get_connected_devices()` - List all connected devices
- `wake_device(mac_address)` - Send Wake-on-LAN packet

#### WiFi Management
- `get_wifi_networks()` - List all WiFi networks and status

#### Port Forwarding
- `get_port_forwards()` - List all port forwarding rules

#### System Control
- `reboot_router()` - Reboot the Fritz!Box

### Data Models

#### FritzDevice
```python
@dataclass
class FritzDevice:
    ip_address: str
    mac_address: str
    hostname: str
    device_type: str
    active: bool
```

#### FritzPortForward
```python
@dataclass
class FritzPortForward:
    enabled: bool
    external_port: int
    internal_port: int
    internal_ip: str
    protocol: str
    description: str
```

## Security

### Credential Management
The tool uses encrypted storage for credentials:
- AES-256 encryption via Fernet
- Local key storage with restrictive permissions (0o600)
- No passwords in plain text or configuration files

### Network Security
- TR-064 protocol works only from local network
- Session-based authentication
- No external API exposure

## Examples

### Device Discovery
```python
devices = await fritz.get_connected_devices()
for device in devices:
    if device.active:
        print(f"🟢 {device.hostname} ({device.ip_address})")
    else:
        print(f"🔴 {device.hostname} - Offline")
```

### Wake-on-LAN
```python
# Wake up a specific device
success = await fritz.wake_device("00:11:22:33:44:55")
if success:
    print("Wake-on-LAN sent successfully")
```

### Port Forwarding Management
```python
forwards = await fritz.get_port_forwards()
active_forwards = [f for f in forwards if f.enabled]

for forward in active_forwards:
    print(f"{forward.external_port} -> {forward.internal_ip}:{forward.internal_port}")
```

## Integration with AI Lab Framework

The Fritz!Box tool integrates with the AI Lab Framework's MCP architecture:

### MCP Integration
```json
{
  "mcpServers": {
    "fritzbox": {
      "command": "python",
      "args": ["/path/to/fritzbox_mcp_server.py"]
    }
  }
}
```

### Available MCP Tools
- `fritzbox_list_devices` - Get connected devices
- `fritzbox_get_info` - Get router information
- `fritzbox_wake_device` - Wake-on-LAN functionality
- `fritzbox_port_forwards` - List port forwarding rules
- `fritzbox_wifi_networks` - Get WiFi network info

## Troubleshooting

### Connection Issues
1. Verify Fritz!Box IP address (usually 192.168.178.1)
2. Check username/password credentials
3. Ensure TR-064 is enabled in Fritz!Box settings
4. Verify network connectivity

### Permission Issues
1. Run with appropriate user permissions
2. Check file permissions for credential storage
3. Ensure firewall allows local network access

### API Limitations
- Some features may require admin privileges
- Certain Fritz!Box models have limited TR-064 support
- Firmware version affects available features

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
ruff check --fix .
mypy .
```

## License

This tool is part of the AI Lab Framework and follows the same licensing terms.

## Support

For issues and feature requests, please refer to the AI Lab Framework documentation.
