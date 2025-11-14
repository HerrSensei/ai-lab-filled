# Homelab Agent OS Framework

## Overview
A comprehensive agent operating system framework for homelab environments, integrating n8n automation with local AI capabilities via gemini-cli/opencode.

## Architecture
- **Core**: Agent OS framework with service management
- **Automation**: n8n with custom nodes for agent communication
- **AI Integration**: Local gemini-cli/opencode setup
- **Deployment**: Homeserver-ready containerized services

## Features
- Multi-agent coordination and management
- Workflow automation via n8n
- Local AI processing with Gemini
- Service discovery and health monitoring
- Configuration management
- Logging and observability

## Quick Start
```bash
# Setup environment
./setup.sh

# Start services
docker-compose up -d

# Access dashboards
# n8n: http://localhost:5678
# Agent OS: http://localhost:8080
```

## Project Structure
```
homelab-agent-os/
├── agent-os/           # Core agent framework
├── n8n-nodes/          # Custom n8n nodes
├── deployment/         # Docker/K8s configs
├── config/            # Configuration files
├── scripts/           # Setup and management
└── docs/              # Documentation
```