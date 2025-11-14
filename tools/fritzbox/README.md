# 🌐 Fritz!Box API Tool

<div align="center">

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Fritz!Box](https://img.shields.io/badge/Fritz!Box-TR--064%20API-orange.svg)

*Comprehensive Python tool for controlling Fritz!Box routers via TR-064 API, integrated with the AI Lab Framework.*

</div>

---

## 📖 Table of Contents

*   [✨ Features](#-features)
*   [⬇️ Installation](#️-installation)
*   [🚀 Quick Start](#-quick-start)
*   [📚 API Reference](#-api-reference)
*   [🔒 Security](#-security)
*   [💡 Examples](#-examples)
*   [🤝 Integration with AI Lab Framework](#-integration-with-ai-lab-framework)
*   [⚠️ Troubleshooting](#️-troubleshooting)
*   [🛠️ Development](#️-development)
*   [🙌 Contributing](#-contributing)
*   [📄 License](#-license)
*   [❓ Support](#-support)

---

## ✨ Features

This tool provides a rich set of functionalities to manage your Fritz!Box router:

*   **🔍 Device Discovery**: List all connected devices with detailed information (IP, MAC, hostname, status) and real-time monitoring.
*   **📶 WiFi Management**: View and manage all WiFi networks (2.4GHz, 5GHz, guest networks), including status and configuration.
*   **🔌 Port Forwarding**: List, enable, and disable port forwarding rules with protocol-specific configurations (TCP/UDP).
*   **😴 Device Management**: Wake-on-LAN support and comprehensive device status monitoring.
*   **📊 Network Monitoring**: Track external IP address, connection statistics (upload/download), and bandwidth usage.
*   **🔐 Security Features**: Encrypted credential storage, secure authentication, and permission-based access control.

---

## ⬇️ Installation

To get started with the Fritz!Box API Tool, follow these steps:

1.  **Clone the AI Lab Framework repository:**
    ```bash
    git clone https://github.com/HerrSensei/ai-lab.git
    cd ai-lab
    ```
2.  **Navigate to the Fritz!Box tool directory:**
    ```bash
    cd tools/fritzbox
    ```
3.  **Install dependencies using Poetry (recommended for AI Lab Framework projects):**
    ```bash
    poetry install
    ```
    Alternatively, you can install individual packages:
    ```bash
    pip install fritzconnection cryptography structlog
    ```

---

## 🚀 Quick Start

Follow these steps to quickly set up and use the Fritz!Box API Tool:

### 1. Store Credentials Securely

Use the `secret_manager.py` script to store your Fritz!Box credentials. This ensures your username and password are encrypted.

```bash
python secret_manager.py
# Select option 1 to store credentials
# Enter your Fritz!Box IP (usually 192.168.178.1)
# Enter username and password
```

### 2. Basic Usage Example

Here's a simple Python script demonstrating how to connect to your Fritz!Box and retrieve basic information:

```python
import asyncio
from fritzbox_api import FritzBoxAPI

async def main():
    # Replace with your actual Fritz!Box host, username, and password
    # For secure credential retrieval, integrate with AI Lab Framework's secret management
    fritz = FritzBoxAPI(
        host="192.168.178.1",
        user="admin",
        password="your_password" # Consider using environment variables or a secure vault
    )

    if await fritz.connect():
        # Get router information
        info = await fritz.get_device_info()
        print(f"Router Model: {info.get('ModelName', 'N/A')}")
        print(f"Firmware Version: {info.get('SoftwareVersion', 'N/A')}")

        # Get external IP address
        ip = await fritz.get_external_ip()
        print(f"External IP: {ip}")

        # List connected devices
        devices = await fritz.get_connected_devices()
        print("\nConnected Devices:")
        for device in devices:
            print(f"  - {device.hostname} ({device.ip_address}) - {'Active' if device.active else 'Inactive'}")
    else:
        print("Failed to connect to Fritz!Box.")

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Run Interactive Examples

Explore the full capabilities of the tool using the interactive demo:

```bash
python fritzbox_api_examples.py --interactive
```
Or run all predefined examples:
```bash
python fritzbox_api_examples.py
```

---

## 📚 API Reference

The `FritzBoxAPI` class provides the primary interface for interacting with your Fritz!Box.

### `FritzBoxAPI` Class

#### Connection Methods
*   `async connect() -> bool`: Establishes a connection to the Fritz!Box router. Returns `True` on success, `False` otherwise.
*   `async get_device_info() -> dict`: Retrieves detailed information about the router, including model, firmware, and serial number.

#### Network Information Methods
*   `async get_external_ip() -> str`: Fetches the current external IP address of your internet connection.
*   `async get_connection_stats() -> dict`: Provides statistics on upload and download usage.

#### Device Management Methods
*   `async get_connected_devices() -> List[FritzDevice]`: Lists all devices currently connected to your network.
*   `async wake_device(mac_address: str) -> bool`: Sends a Wake-on-LAN packet to a specified device.

#### WiFi Management Methods
*   `async get_wifi_networks() -> List[FritzWiFiNetwork]`: Retrieves information about all configured WiFi networks and their status.

#### Port Forwarding Methods
*   `async get_port_forwards() -> List[FritzPortForward]`: Lists all active port forwarding rules.

#### System Control Methods
*   `async reboot_router() -> bool`: Initiates a reboot of the Fritz!Box router.

### Data Models

The API utilizes the following dataclasses for structured data representation:

#### `FritzDevice`
```python
@dataclass
class FritzDevice:
    ip_address: str
    mac_address: str
    hostname: str
    device_type: str
    active: bool
```
Represents a connected device on the network.

#### `FritzPortForward`
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
Represents a configured port forwarding rule.

---

## 🔒 Security

Security is a paramount concern for network tools. This tool incorporates several measures:

*   **Credential Management**: Utilizes AES-256 encryption via Fernet for secure storage of Fritz!Box credentials. Keys are stored locally with restrictive permissions (`0o600`), ensuring no plain-text passwords in configuration files.
*   **Network Security**: The TR-064 protocol operates exclusively within your local network, preventing external exposure.
*   **Authentication**: Employs session-based authentication for secure interactions with the router.

---

## 💡 Examples

Here are some practical examples demonstrating the tool's capabilities:

### Device Discovery
```python
devices = await fritz.get_connected_devices()
for device in devices:
    if device.active:
        print(f"🟢 {device.hostname} ({device.ip_address}) - Active")
    else:
        print(f"🔴 {device.hostname} - Offline")
```

### Wake-on-LAN
```python
# Example: Wake up a specific device by its MAC address
success = await fritz.wake_device("00:11:22:33:44:55") # Replace with actual MAC
if success:
    print("Wake-on-LAN packet sent successfully!")
else:
    print("Failed to send Wake-on-LAN packet.")
```

### Port Forwarding Management
```python
forwards = await fritz.get_port_forwards()
active_forwards = [f for f in forwards if f.enabled]

print("\nActive Port Forwards:")
for forward in active_forwards:
    print(f"  - External Port: {forward.external_port}, Internal IP: {forward.internal_ip}, Internal Port: {forward.internal_port}, Protocol: {forward.protocol}")
```

---

## 🤝 Integration with AI Lab Framework

The Fritz!Box API Tool is designed for seamless integration with the AI Lab Framework's Model Context Protocol (MCP) architecture, enabling advanced automation and control within your homelab environment.

### MCP Integration Configuration
To integrate with an MCP server, configure your `mcpServers` as follows:
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
The following functionalities are exposed as MCP tools for framework-level orchestration:
*   `fritzbox_list_devices`: Retrieve a list of all connected devices.
*   `fritzbox_get_info`: Obtain detailed router information.
*   `fritzbox_wake_device`: Trigger Wake-on-LAN for a specified device.
*   `fritzbox_port_forwards`: List all configured port forwarding rules.
*   `fritzbox_wifi_networks`: Get information about WiFi networks.

---

## ⚠️ Troubleshooting

Encountering issues? Here are some common problems and their solutions:

*   **Connection Issues**:
    1.  Verify your Fritz!Box IP address (default is `192.168.178.1`).
    2.  Double-check your username and password credentials.
    3.  Ensure TR-064 is enabled in your Fritz!Box settings.
    4.  Confirm network connectivity between your system and the Fritz!Box.
*   **Permission Issues**:
    1.  Run scripts with appropriate user permissions.
    2.  Check file permissions for credential storage (`secret_manager.py`).
    3.  Ensure your firewall allows local network access to the Fritz!Box.
*   **API Limitations**:
    1.  Some advanced features may require administrator privileges on the Fritz!Box.
    2.  Certain Fritz!Box models or firmware versions may have limited TR-064 support.

---

## 🛠️ Development

For developers looking to contribute or extend this tool:

### Running Tests
Execute the test suite to ensure functionality and prevent regressions:
```bash
pytest tests/
```

### Code Quality
Maintain high code quality standards using:
```bash
black .             # Code formatting
ruff check --fix .  # Linting and auto-fixing
mypy .              # Static type checking
```

---

## 🙌 Contributing

We welcome contributions to the Fritz!Box API Tool! Please refer to the main [Contributing Guidelines](core/guidelines/AGENTS.md) for the AI Lab Framework.

---

## 📄 License

This tool is part of the AI Lab Framework and is licensed under the MIT License. See the main [LICENSE](LICENSE) file for details.

---

## ❓ Support

For issues, feature requests, or general support, please refer to the main [AI Lab Framework Documentation](README.md).
