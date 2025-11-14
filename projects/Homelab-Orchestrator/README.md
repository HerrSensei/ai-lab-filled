# 🏠 Homelab Orchestrator

<div align="center">

![Status](https://img.shields.io/badge/status-✅%20Active%20Development-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

*A comprehensive agent operating system framework for homelab environments, integrating n8n automation with local AI capabilities.*

</div>

---

## 📖 Table of Contents

*   [✨ Overview](#-overview)
*   [🏗️ Architecture](#-architecture)
*   [🚀 Features](#-features)
*   [⬇️ Quick Start](#️-quick-start)
*   [📁 Project Structure](#-project-structure)
*   [🤝 Contributing](#-contributing)
*   [📄 License](#-license)
*   [❓ Support](#-support)

---

## ✨ Overview

The **Homelab Orchestrator** is designed to be the central nervous system for your homelab. It provides a robust framework for managing and automating various services and devices, leveraging the power of agent-based systems and local AI integration. This project aims to bring intelligent automation and seamless control to your personal infrastructure.

---

## 🏗️ Architecture

The orchestrator is built upon a modular and extensible architecture:

*   **Core Agent OS**: The foundation of the system, responsible for service management, agent coordination, and overall system health.
*   **n8n Automation**: Integrates with n8n for powerful workflow automation, utilizing custom nodes for seamless communication with agents.
*   **Local AI Integration**: Leverages local AI capabilities via `gemini-cli` or `opencode` for intelligent decision-making and task execution.
*   **Containerized Deployment**: Designed for easy deployment on homeservers using Docker and Kubernetes, ensuring portability and scalability.

---

## 🚀 Features

*   **🧠 Multi-Agent Coordination**: Manage and orchestrate multiple intelligent agents to perform complex tasks across your homelab.
*   **⚙️ Workflow Automation**: Automate routine tasks and create sophisticated workflows using n8n, tailored to your homelab needs.
*   **💡 Local AI Processing**: Integrate local AI models for on-device intelligence, enhancing privacy and responsiveness.
*   **🔍 Service Discovery & Monitoring**: Automatically discover services and monitor their health, ensuring continuous operation.
*   **🎛️ Configuration Management**: Centralized management of configurations for all integrated services and devices.
*   **📊 Logging & Observability**: Comprehensive logging and monitoring tools for deep insights into system performance and agent activities.

---

## ⬇️ Quick Start

Get your Homelab Orchestrator up and running with these simple steps:

### Prerequisites
*   Docker & Docker Compose
*   Python 3.11+
*   `gemini-cli` or `opencode` (for local AI integration)

### Setup and Run

1.  **Navigate to the project directory:**
    ```bash
    cd projects/Homelab-Orchestrator
    ```
2.  **Set up the environment (if a `setup.sh` script exists and is required):**
    ```bash
    ./setup.sh
    ```
    *(Note: If `setup.sh` is not present or needed, you can skip this step.)*
3.  **Start the services using Docker Compose:**
    ```bash
    docker-compose up -d
    ```
4.  **Access the dashboards:**
    *   **n8n**: `http://localhost:5678`
    *   **Agent OS**: `http://localhost:8080` (or as configured)

---

## 📁 Project Structure

```
homelab-agent-os/
├── 🧠 agent-os/           # Core agent framework and service management
├── ⚙️ n8n-nodes/          # Custom n8n nodes for extended automation capabilities
├── 🚀 deployment/         # Docker/Kubernetes configurations for easy deployment
├── 🛠️ config/            # Centralized configuration files for the orchestrator
├── 📜 scripts/           # Utility scripts for setup, management, and automation
└── 📚 docs/              # Comprehensive documentation for the Homelab Orchestrator
```

---

## 🤝 Contributing

We welcome contributions to the Homelab Orchestrator! Please refer to the main [Contributing Guidelines](core/guidelines/AGENTS.md) for the AI Lab Framework.

---

## 📄 License

This project is part of the AI Lab Framework and is licensed under the MIT License. See the main [LICENSE](README.md) file for details.

---

## ❓ Support

For issues, feature requests, or general support, please refer to the main [AI Lab Framework Documentation](README.md).