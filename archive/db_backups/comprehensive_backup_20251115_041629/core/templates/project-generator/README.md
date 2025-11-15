# 🏗️ AI Lab Project Generator

<div align="center">

![Status](https://img.shields.io/badge/status-✅%20Ready%20for%20Use-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

*Your ultimate tool for scaffolding perfectly structured AI Lab Framework projects, adhering to Agent-OS standards and best practices.*

</div>

---

## 📖 Table of Contents

*   [✨ Overview](#-overview)
*   [🚀 Available Templates](#-available-templates)
*   [⬇️ Usage](#️-usage)
*   [🎯 Key Features](#-key-features)
*   [📁 Generated Project Structure](#-generated-project-structure)
*   [🤝 Integration with Agent-OS](#-integration-with-agent-os)
*   [🙌 Contributing](#-contributing)
*   [📄 License](#-license)
*   [❓ Support](#-support)

---

## ✨ Overview

The **AI Lab Project Generator** is a powerful command-line tool designed to streamline the creation of new projects within the AI Lab Framework. It ensures that every new project starts with a perfectly structured foundation, pre-configured with best practices, Agent-OS standards, and all necessary tooling. Say goodbye to manual setup and hello to consistent, high-quality project initiation!

---

## 🚀 Available Templates

Choose from a variety of pre-defined templates to kickstart your project:

### 1. **🌐 `web-app` - Full-stack Web Application**
*   **Description**: Ideal for building comprehensive web solutions.
*   **Includes**: Frontend (React/Vue/Svelte), Backend API (FastAPI/Express), database integration, testing setup, and Docker configuration.

### 2. **⚙️ `api-service` - Backend API Service**
*   **Description**: Perfect for developing robust and scalable backend services.
*   **Includes**: FastAPI/Express framework, database models, API routes, authentication, and a complete testing suite.

### 3. **🤖 `agent-skill` - Agent-OS Compatible Skill**
*   **Description**: For extending the capabilities of your Agent-OS agents.
*   **Includes**: Standard skill structure, seamless Agent-OS integration, comprehensive documentation, and a testing framework.

### 4. **📊 `data-pipeline` - Data Processing Pipeline**
*   **Description**: Designed for efficient data ingestion, transformation, and loading.
*   **Includes**: ETL (Extract, Transform, Load) structure, data validation, monitoring, and robust logging mechanisms.

### 5. **マイクロサービス `microservice` - Microservice Template**
*   **Description**: For building decoupled and independently deployable services.
*   **Includes**: Service discovery, API gateway patterns, database integration, and health checks.

---

## ⬇️ Usage

Generate a new project with a single command. The generator will guide you through the process or allow for quick creation with specified options.

```bash
# Generate a new project (interactive mode)
./generate-project.sh

# Example: Generate a web-app project named 'my-awesome-app'
./generate-project.sh web-app my-awesome-app

# Example: Generate an API service with PostgreSQL database
./generate-project.sh api-service user-service --database postgresql

# Example: Generate an Agent-OS skill
./generate-project.sh agent-skill weather-skill --agent-os
```

---

## 🎯 Key Features

*   **✅ Agent-OS Standards Compliance**: All generated projects adhere to the strict standards of the Agent-OS framework.
*   **💡 AI Lab Guidelines Integration**: Incorporates AI Lab's best practices for code quality, structure, and documentation.
*   **📦 Automatic Dependency Management**: Pre-configured `pyproject.toml` or `package.json` for seamless dependency handling.
*   **🧪 Testing Framework Setup**: Ready-to-use testing environments with Pytest or equivalent.
*   **📚 Documentation Generation**: Basic documentation structure and templates are automatically created.
*   **🐳 Docker Support**: Includes Dockerfiles and `docker-compose.yml` for containerized development and deployment.
*   **🚀 CI/CD Pipeline Templates**: Provides starter templates for GitHub Actions or GitLab CI/CD.
*   **🌐 Multi-System Architecture Support**: Designed with awareness for complex, distributed system architectures.

---

## 📁 Generated Project Structure

All generated projects follow a consistent, well-organized structure:

```
project-name/
├── 📄 README.md                 # Comprehensive project documentation and overview
├── 🚫 .gitignore               # Standard Git ignore rules for common files
├── ⚙️ .env.example             # Template for environment variables
├── 🐳 docker-compose.yml       # Docker configuration for local development
├── 🛠️ Makefile                 # Collection of common development tasks
├── 📚 docs/                    # Project-specific documentation
├── 💻 src/                     # Main source code directory
├── 🧪 tests/                   # Automated test suite
├── 📜 scripts/                 # Utility and automation scripts
├── 🎛️ config/                  # Configuration files for the project
└── 🧠 .ai-lab/                 # AI-LAB specific metadata and configurations
    ├── project-spec.yml     # Detailed project specification
    ├── standards.yml        # Applied AI Lab and Agent-OS standards
    └── generated-by.yml     # Metadata about project generation
```

---

## 🤝 Integration with Agent-OS

All projects generated by this tool are fully compatible with the Agent-OS framework, ensuring seamless integration into your AI-driven development workflows. This includes:

*   **Standard-Compliant Directory Structure**: Ensures consistency and ease of use with Agent-OS.
*   **Agent-OS Workflow Integration**: Ready for use with Agent-OS's 6-phase workflow.
*   **Spec-Driven Development Support**: Facilitates structured development based on detailed specifications.
*   **Multi-System Architecture Awareness**: Designed to operate effectively within complex, distributed environments.

---

## 🙌 Contributing

We welcome contributions to the AI Lab Project Generator! Please refer to the main [Contributing Guidelines](core/guidelines/AGENTS.md) for the AI Lab Framework.

---

## 📄 License

This project is part of the AI Lab Framework and is licensed under the MIT License. See the main [LICENSE](README.md) file for details.

---

## ❓ Support

For issues, feature requests, or general support, please refer to the main [AI Lab Framework Documentation](README.md).
