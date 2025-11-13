# AI-LAB Project Generator

## Overview

The AI-LAB Project Generator creates perfectly structured projects based on Agent-OS standards and AI-LAB guidelines.

## Available Templates

### 1. **web-app** - Full-stack web application
- Frontend (React/Vue/Svelte)
- Backend API (FastAPI/Express)
- Database integration
- Testing setup
- Docker configuration

### 2. **api-service** - Backend API service
- FastAPI/Express framework
- Database models
- API routes
- Authentication
- Testing suite

### 3. **agent-skill** - Agent-OS compatible skill
- Skill structure
- Agent-OS integration
- Documentation
- Testing framework

### 4. **data-pipeline** - Data processing pipeline
- ETL structure
- Data validation
- Monitoring
- Logging

### 5. **microservice** - Microservice template
- Service discovery
- API gateway
- Database integration
- Health checks

## Usage

```bash
# Generate a new project
./generate-project.sh <template-name> <project-name> [options]

# Examples:
./generate-project.sh web-app my-awesome-app
./generate-project.sh api-service user-service --database postgresql
./generate-project.sh agent-skill weather-skill --agent-os
```

## Features

- ✅ Agent-OS standards compliance
- ✅ AI-LAB guidelines integration
- ✅ Automatic dependency management
- ✅ Testing framework setup
- ✅ Documentation generation
- ✅ Docker support
- ✅ CI/CD pipeline templates
- ✅ Multi-system architecture support

## Generated Structure

All generated projects include:

```
project-name/
├── README.md                 # Project documentation
├── .gitignore               # Git ignore rules
├── .env.example             # Environment variables
├── docker-compose.yml       # Docker configuration
├── Makefile                 # Common tasks
├── docs/                    # Documentation
├── src/                     # Source code
├── tests/                   # Test suite
├── scripts/                 # Utility scripts
├── config/                  # Configuration files
└── .ai-lab/                 # AI-LAB metadata
    ├── project-spec.yml     # Project specification
    ├── standards.yml        # Applied standards
    └── generated-by.yml     # Generation metadata
```

## Integration with Agent-OS

All generated projects are Agent-OS compatible and include:

- Standard-compliant directory structure
- Agent-OS workflow integration
- Spec-driven development support
- Multi-system architecture awareness
