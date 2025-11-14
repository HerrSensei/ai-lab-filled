# AI Lab Framework - Connected Systems Dashboard

## 🏠 HomeServer Infrastructure

### Core Systems
- **HomeServer**: `100.78.230.92` (Tailscale VPN)
  - Proxmox VE (Port 8006)
  - Docker Containers
  - CasaOS (Port 8080)
  - System Monitoring

### Network Infrastructure
- **Fritz!Box Router**: `192.168.178.1` (fritz.box)
  - Model: AVM Fritz!Box (detected via ARP)
  - MAC: `2c:91:ab:70:41:8e`
  - Features: TR-064 API, WiFi, Port Forwarding, DHCP

### Connected Devices (from ARP table)
- **CasaOS Device**: `192.168.178.146` (incomplete entry)
- **CasaOS Device**: `192.168.178.161` (bc:24:11:6a:b:df)
- **Home Assistant**: `192.168.178.162` (2:7f:50:99:85:61)
- **AdGuard DNS**: `192.168.178.166` (bc:24:11:a1:ff:84)
- **Unknown Device**: `192.168.178.128` (54:48:10:d7:ef:2b)
- **Current Machine**: `192.168.178.155` (en0 interface)

## 🔧 Control Plane Services

### Agent Control Plane API
- **Location**: `/projects/agent-control-plane/`
- **Status**: ✅ Fully Operational
- **Endpoints**:
  - `/api/system` - System management
  - `/api/docker` - Docker container control
  - `/api/auth` - Authentication & security
  - `/api/proxmox` - VM/container management
  - `/api/adguard` - DNS management
  - `/api/hisense` - TV control

### MCP Server Integration
- **Location**: `/functional-mcp-server/`
- **Target**: HomeServer `100.78.230.92`
- **Authentication**: ED25519 SSH key
- **Available Tools**:
  - `ssh_command` - Remote command execution
  - `proxmox_status` - Proxmox cluster status
  - `docker_list_containers` - Container management
  - `casaos_status` - CasaOS monitoring
  - `system_info` - System information

## 🛠️ Tools & Utilities

### Fritz!Box API Tool
- **Location**: `/tools/fritzbox/`
- **Status**: ⚠️ Authentication required (95% complete)
- **Features**:
  - Device discovery and management
  - WiFi network control
  - Port forwarding management
  - Wake-on-LAN support
  - Connection statistics
  - Encrypted credential storage
  - MCP server integration (8 tools ready)
- **Current Issue**: TR-064 admin password needed (WiFi password `stark0564` found but doesn't work)
- **Setup**: Run `python final_setup.py` with correct admin credentials
- **MCP Server**: `fritzbox_mcp_server.py` ready after authentication
- **Status Report**: See `/tools/fritzbox/SETUP_STATUS.md`

### Hisense TV Control
- **Location**: `/tools/hisense-tv/`
- **Status**: ✅ Implemented
- **Features**:
  - MQTT-based TV control
  - Power management
  - Input/source switching
  - Volume control

## 📊 Service Status Matrix

| Service | IP/Host | Port | Status | Integration |
|---------|---------|------|--------|-------------|
| HomeServer | 100.78.230.92 | - | ✅ Active | MCP + SSH |
| Proxmox VE | 100.78.230.92 | 8006 | ✅ Active | MCP + API |
| CasaOS | 100.78.230.92 | 8080 | ✅ Active | MCP + API |
| Fritz!Box | 192.168.178.1 | 80 | ⚠️ Auth needed | TR-064 API |
| Home Assistant | 192.168.178.162 | 8123 | ✅ Active | Local API |
| AdGuard DNS | 192.168.178.166 | 3000 | ✅ Active | HTTP API |
| Agent Control Plane | localhost | 8000 | ✅ Active | FastAPI |

## 🔐 Authentication & Security

### SSH Keys
- **MCP Server**: ED25519 key for HomeServer access
- **Fritz!Box**: Username/password authentication (encrypted storage)

### Network Access
- **Tailscale VPN**: For HomeServer remote access
- **Local Network**: For Fritz!Box and local services
- **API Authentication**: JWT tokens for Agent Control Plane

## 📈 Monitoring & Logging

### System Monitoring
- **HomeServer**: Via MCP system_info tool
- **Agent Control Plane**: Structured logging with structlog
- **Fritz!Box**: Connection statistics and device monitoring

### Log Locations
- Agent Control Plane: `/projects/agent-control-plane/logs/`
- MCP Server: Console/stdio logging
- Fritz!Box Tool: Local file logging

## 🔄 Integration Workflows

### n8n Automation (Planned)
- **Service**: `fritzbox_mcp` (56ms response time)
- **Integration**: Router automation workflows
- **Status**: Planned implementation

### API Orchestration
1. **Agent OS** (Design Layer)
2. **n8n** (Orchestration Layer)
3. **MCP** (Runtime Control Layer)

## 📝 Configuration Files

### MCP Client Configuration
```json
{
  "mcpServers": {
    "ai-lab-homeserver": {
      "command": "node",
      "args": ["/Users/jns/Documents/1 | Projekte/ai-lab/functional-mcp-server/server.js"]
    },
    "fritzbox": {
      "command": "python",
      "args": ["/Users/jns/Documents/1 | Projekte/ai-lab/tools/fritzbox/fritzbox_mcp_server.py"]
    }
  }
}
```

### Fritz!Box Credentials
- **Storage**: Encrypted local storage
- **Manager**: `/tools/fritzbox/secret_manager.py`
- **Default Host**: `192.168.178.1`

## 🚀 Quick Access Commands

### Agent Control Plane
```bash
cd projects/agent-control-plane
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### MCP Server
```bash
cd functional-mcp-server
node server.js
```

### Fritz!Box Tool
```bash
cd tools/fritzbox
source venv/bin/activate  # Activate virtual environment
python final_setup.py  # Store admin credentials
python fritzbox_api_examples.py --interactive  # Interactive demo (after auth)
python fritzbox_mcp_server.py  # Start MCP server (after auth)
```

## 📋 Maintenance Tasks

### Regular Checks
- [ ] Verify SSH key connectivity to HomeServer
- [ ] Test Fritz!Box API credentials (need admin password)
- [ ] Monitor Agent Control Plane service health
- [ ] Check Tailscale VPN connection status

### Updates
- [ ] Update Fritz!Box firmware via API
- [ ] Refresh MCP server dependencies
- [ ] Update Agent Control Plane dependencies
- [ ] Rotate SSH keys as needed

---

*Last Updated: 2025-11-09*
*Framework Version: AI Lab Framework v1.0*
