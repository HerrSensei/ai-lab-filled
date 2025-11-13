#!/bin/bash

# AI-LAB Project Generator
# Creates perfectly structured projects based on Agent-OS standards and AI-LAB guidelines

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/templates"
PROJECT_NAME=""
TEMPLATE_TYPE=""
DATABASE=""
FRONTEND=""
AGENT_OS=""
HELP=false

# Available templates
AVAILABLE_TEMPLATES=("web-app" "api-service" "agent-skill" "data-pipeline" "microservice")

# Function to print colored output
print_color() {
    local color=$1
    shift
    echo -e "${color}$*${NC}"
}

# Function to print help
print_help() {
    cat << EOF
AI-LAB Project Generator

USAGE:
    $0 <template> <project-name> [OPTIONS]

TEMPLATES:
    web-app        Full-stack web application
    api-service    Backend API service
    agent-skill    Agent-OS compatible skill
    data-pipeline  Data processing pipeline
    microservice   Microservice template

OPTIONS:
    --database <db>     Database type (postgresql, mysql, sqlite, mongodb)
    --frontend <fw>     Frontend framework (react, vue, svelte, angular)
    --agent-os          Include Agent-OS integration
    --help              Show this help message

EXAMPLES:
    $0 web-app my-awesome-app
    $0 api-service user-service --database postgresql
    $0 agent-skill weather-skill --agent-os
    $0 web-app fullstack-app --database postgresql --frontend react --agent-os

EOF
}

# Function to validate template type
validate_template() {
    local template=$1
    for available in "${AVAILABLE_TEMPLATES[@]}"; do
        if [[ "$template" == "$available" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to create directory structure
create_directory_structure() {
    local project_path=$1
    local template=$2

    print_color $BLUE "Creating directory structure..."

    # Base directories for all projects
    mkdir -p "$project_path"/{src,tests,docs,scripts,config,.ai-lab}

    # Template-specific directories
    case $template in
        "web-app")
            mkdir -p "$project_path"/src/{frontend,backend,shared}
            mkdir -p "$project_path"/src/backend/{api,models,services,utils}
            mkdir -p "$project_path"/src/frontend/{components,pages,hooks,utils,assets}
            mkdir -p "$project_path"/tests/{unit,integration,e2e}
            ;;
        "api-service")
            mkdir -p "$project_path"/src/{api,models,services,utils,middleware}
            mkdir -p "$project_path"/tests/{unit,integration}
            ;;
        "agent-skill")
            mkdir -p "$project_path"/src/{skill,agents,utils,tests}
            mkdir -p "$project_path"/docs/{specifications,examples}
            ;;
        "data-pipeline")
            mkdir -p "$project_path"/src/{extract,transform,load,monitoring,utils}
            mkdir -p "$project_path"/tests/{unit,integration}
            mkdir -p "$project_path"/config/{schemas,environments}
            ;;
        "microservice")
            mkdir -p "$project_path"/src/{api,services,models,utils,health}
            mkdir -p "$project_path"/tests/{unit,integration}
            mkdir -p "$project_path"/config/{kubernetes,docker}
            ;;
    esac

    print_color $GREEN "✓ Directory structure created"
}

# Function to generate project configuration
generate_config() {
    local project_path=$1
    local project_name=$2
    local template=$3

    print_color $BLUE "Generating project configuration..."

    # Generate .ai-lab/project-spec.yml
    cat > "$project_path/.ai-lab/project-spec.yml" << EOF
# AI-LAB Project Specification
project:
  name: "$project_name"
  type: "$template"
  version: "1.0.0"
  created: "$(date -Iseconds)"
  generator: "ai-lab-project-generator v1.0"

# Template configuration
template:
  type: "$template"
  database: "${DATABASE:-none}"
  frontend: "${FRONTEND:-none}"
  agent_os: $([ "$AGENT_OS" = "true" ] && echo "true" || echo "false")

# Applied standards
standards:
  - "ai-lab-coding-style"
  - "ai-lab-conventions"
  - "ai-lab-validation"
  $([ "$AGENT_OS" = "true" ] && echo '- "agent-orchestration"')
  $([ "$DATABASE" != "none" ] && echo '- "database-standards"')

# Multi-system architecture support
architecture:
  multi_system: true
  target_systems:
    - "development"
    - "staging"
    - "production"
  deployment:
    docker: true
    kubernetes: $([ "$template" = "microservice" ] && echo "true" || echo "false")

# Development workflow
workflow:
  version_control: "git"
  ci_cd: "github-actions"
  testing: "pytest"
  documentation: "markdown"
  agent_os: $([ "$AGENT_OS" = "true" ] && echo "true" || echo "false")
EOF

    # Generate .ai-lab/standards.yml
    cat > "$project_path/.ai-lab/standards.yml" << EOF
# Applied AI-LAB Standards
standards:
  coding_style:
    python:
      line_length: 88
      import_order: "isort"
      formatter: "black"
      linter: "flake8"
    javascript:
      style: "standard"
      formatter: "prettier"
      linter: "eslint"

  conventions:
    naming: "snake_case"
    commit_messages: "conventional"
    documentation: "google_style"

  validation:
    type_checking: true
    input_validation: true
    error_handling: "comprehensive"

  testing:
    coverage_threshold: 80
    test_types: ["unit", "integration"]
    framework: "pytest"
EOF

    # Generate .ai-lab/generated-by.yml
    cat > "$project_path/.ai-lab/generated-by.yml" << EOF
# Generation Metadata
generator:
  name: "AI-LAB Project Generator"
  version: "1.0.0"
  timestamp: "$(date -Iseconds)"
  user: "$(whoami)"
  system: "$(uname -s)"

parameters:
  template: "$template"
  project_name: "$project_name"
  database: "${DATABASE:-none}"
  frontend: "${FRONTEND:-none}"
  agent_os: $([ "$AGENT_OS" = "true" ] && echo "true" || echo "false")
EOF

    print_color $GREEN "✓ Project configuration generated"
}

# Function to generate base files
generate_base_files() {
    local project_path=$1
    local project_name=$2
    local template=$3

    print_color $BLUE "Generating base files..."

    # Generate README.md
    cat > "$project_path/README.md" << EOF
# $project_name

Generated with AI-LAB Project Generator

## Overview

This is a $template project generated with AI-LAB standards and Agent-OS integration.

$([ "$AGENT_OS" = "true" ] && echo "## Agent-OS Integration

This project is Agent-OS compatible and includes:
- Agent-OS workflow integration
- Spec-driven development support
- Multi-system architecture awareness

")

## Quick Start

\`\`\`bash
# Install dependencies
make install

# Run development server
make dev

# Run tests
make test
\`\`\`

## Project Structure

\`\`\`
$project_name/
├── src/                    # Source code
├── tests/                  # Test suite
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── config/                 # Configuration files
├── .ai-lab/                # AI-LAB metadata
└── README.md               # This file
\`\`\`

## Development

### Prerequisites

- Python 3.9+
- Node.js 16+ $([ "$FRONTEND" != "none" ] && echo "(for frontend development)")
- Docker $([ "$DATABASE" != "none" ] && echo "(for database)")

### Setup

\`\`\`bash
# Clone and setup
git clone <repository-url>
cd $project_name
make install
\`\`\`

### Commands

- \`make install\` - Install dependencies
- \`make dev\` - Start development server
- \`make test\` - Run tests
- \`make lint\` - Run linting
- \`make build\` - Build for production
- \`make deploy\` - Deploy to production

## Standards Compliance

This project follows AI-LAB standards:
- ✅ Coding standards
- ✅ Documentation standards
- ✅ Testing standards
- ✅ Security standards
$([ "$AGENT_OS" = "true" ] && echo "- ✅ Agent-OS integration standards")

## Architecture

$([ "$DATABASE" != "none" ] && echo "### Database
- Type: $DATABASE
- Migrations: \`make db-migrate\`
- Seeding: \`make db-seed\`

")
$([ "$FRONTEND" != "none" ] && echo "### Frontend
- Framework: $FRONTEND
- Build tool: Vite
- Testing: Jest

")

## Contributing

1. Follow AI-LAB coding standards
2. Write tests for new features
3. Update documentation
4. Use conventional commit messages

## License

MIT License - see LICENSE file for details.
EOF

    # Generate .gitignore
    cat > "$project_path/.gitignore" << EOF
# Python
__pycache__/
*.py[cod]
*\$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
.venv/
.env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Node.js $([ "$FRONTEND" != "none" ] && echo "
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.eslintcache
")

# Build outputs
dist/
build/
out/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# AI-LAB specific
.ai-lab/local/
.ai-lab/cache/
.ai-lab/temp/
EOF

    # Generate Makefile
    cat > "$project_path/Makefile" << EOF
# AI-LAB Project Makefile

.PHONY: help install dev test lint clean build deploy

# Default target
help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  dev         Start development server"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  clean       Clean build artifacts"
	@echo "  build       Build for production"
	@echo "  deploy      Deploy to production"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	$([ "$FRONTEND" != "none" ] && echo "	cd src/frontend && npm install")
	$([ "$AGENT_OS" = "true" ] && echo "	@echo \"Installing Agent-OS dependencies...\"")

# Development
dev:
	@echo "Starting development server..."
	python -m src.main

# Testing
test:
	@echo "Running tests..."
	pytest tests/ -v --cov=src

# Linting
lint:
	@echo "Running linting..."
	flake8 src/
	black --check src/
	isort --check-only src/
	$([ "$FRONTEND" != "none" ] && echo "	cd src/frontend && npm run lint")

# Format code
format:
	@echo "Formatting code..."
	black src/
	isort src/
	$([ "$FRONTEND" != "none" ] && echo "	cd src/frontend && npm run format")

# Clean
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build
build:
	@echo "Building for production..."
	docker build -t $project_name .

# Deploy
deploy:
	@echo "Deploying to production..."
	@echo "Deployment configuration needed"
EOF

    # Generate requirements.txt
    cat > "$project_path/requirements.txt" << EOF
# AI-LAB Base Requirements
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0

# Code quality
black>=23.0.0
flake8>=6.0.0
isort>=5.12.0

# Utilities
python-multipart>=0.0.6
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
structlog>=23.2.0

$([ "$DATABASE" = "postgresql" ] && echo "# PostgreSQL
asyncpg>=0.29.0
sqlalchemy[asyncio]>=2.0.0
alembic>=1.13.0")

$([ "$DATABASE" = "mysql" ] && echo "# MySQL
aiomysql>=0.2.0
sqlalchemy[asyncio]>=2.0.0
alembic>=1.13.0")

$([ "$DATABASE" = "sqlite" ] && echo "# SQLite
sqlalchemy[asyncio]>=2.0.0
aiosqlite>=0.19.0")

$([ "$DATABASE" = "mongodb" ] && echo "# MongoDB
motor>=3.3.0
pymongo>=4.6.0")

$([ "$AGENT_OS" = "true" ] && echo "# Agent-OS
agent-os>=1.0.0
pyyaml>=6.0.1")
EOF

    # Generate .env.example
    cat > "$project_path/.env.example" << EOF
# Environment Configuration
DEBUG=true
LOG_LEVEL=INFO

# Application
APP_NAME=$project_name
APP_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000

$([ "$DATABASE" != "none" ] && echo "# Database
DATABASE_URL=$([ "$DATABASE" = "postgresql" ] && echo "postgresql://user:password@localhost/dbname" || [ "$DATABASE" = "mysql" ] && echo "mysql://user:password@localhost/dbname" || [ "$DATABASE" = "sqlite" ] && echo "sqlite:///./app.db" || [ "$DATABASE" = "mongodb" ] && echo "mongodb://localhost:27017/dbname")
")

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI-LAB
AI_LAB_ENVIRONMENT=development
AI_LAB_PROJECT_TYPE=$template
$([ "$AGENT_OS" = "true" ] && echo "AGENT_OS_ENABLED=true")
EOF

    print_color $GREEN "✓ Base files generated"
}

# Function to generate template-specific files
generate_template_files() {
    local project_path=$1
    local project_name=$2
    local template=$3

    print_color $BLUE "Generating template-specific files..."

    case $template in
        "web-app")
            generate_web_app_files "$project_path" "$project_name"
            ;;
        "api-service")
            generate_api_service_files "$project_path" "$project_name"
            ;;
        "agent-skill")
            generate_agent_skill_files "$project_path" "$project_name"
            ;;
        "data-pipeline")
            generate_data_pipeline_files "$project_path" "$project_name"
            ;;
        "microservice")
            generate_microservice_files "$project_path" "$project_name"
            ;;
    esac

    print_color $GREEN "✓ Template-specific files generated"
}

# Function to generate web app files
generate_web_app_files() {
    local project_path=$1
    local project_name=$2

    # Backend main.py
    cat > "$project_path/src/backend/main.py" << EOF
"""
Backend main application for $project_name
Generated with AI-LAB Project Generator
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import routes
from src.core.config import settings

app = FastAPI(
    title="$project_name API",
    description="Backend API for $project_name",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "$project_name"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

    # Backend config
    mkdir -p "$project_path/src/backend/core"
    cat > "$project_path/src/backend/core/config.py" << EOF
"""
Configuration settings for $project_name
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "$project_name"
    debug: bool = True
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "dev-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()
EOF

    # Frontend package.json (if frontend specified)
    if [[ "$FRONTEND" != "none" ]]; then
        cat > "$project_path/src/frontend/package.json" << EOF
{
  "name": "$project_name-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
    "format": "prettier --write ."
  },
  "dependencies": {
    $([ "$FRONTEND" = "react" ] && echo "\"react\": \"^18.2.0\",
    \"react-dom\": \"^18.2.0\",
    \"react-router-dom\": \"^6.8.0\"")
    $([ "$FRONTEND" = "vue" ] && echo "\"vue\": \"^3.3.0\",
    \"vue-router\": \"^4.2.0\"")
    $([ "$FRONTEND" = "svelte" ] && echo "\"@sveltejs/kit\": \"^1.20.0\"")
  },
  "devDependencies": {
    $([ "$FRONTEND" = "react" ] && echo "\"@types/react\": \"^18.2.0\",
    \"@types/react-dom\": \"^18.2.0\",
    \"@vitejs/plugin-react\": \"^4.0.0\"")
    $([ "$FRONTEND" = "vue" ] && echo "\"@vitejs/plugin-vue\": \"^4.4.0\"")
    $([ "$FRONTEND" = "svelte" ] && echo "\"@sveltejs/adapter-auto\": \"^2.1.0\",
    \"@sveltejs/kit\": \"^1.20.0\",
    \"svelte\": \"^4.0.0\"")
    "vite": "^4.4.0",
    "eslint": "^8.45.0",
    "prettier": "^3.0.0"
  }
}
EOF
    fi
}

# Function to generate API service files
generate_api_service_files() {
    local project_path=$1
    local project_name=$2

    cat > "$project_path/src/main.py" << EOF
"""
Main application for $project_name API Service
Generated with AI-LAB Project Generator
"""

from fastapi import FastAPI
from src.api import routes
from src.core.config import settings

app = FastAPI(
    title="$project_name API",
    description="API service for $project_name",
    version="1.0.0"
)

# Include routers
app.include_router(routes.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "$project_name"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
}

# Function to generate agent skill files
generate_agent_skill_files() {
    local project_path=$1
    local project_name=$2

    cat > "$project_path/src/skill/main.py" << EOF
"""
Agent-OS Skill: $project_name
Generated with AI-LAB Project Generator
"""

from agent_os import Skill, Context
from src.skill.handlers import main_handler

class $(echo "$project_name" | sed 's/^./\U&/' | sed 's/-\([a-z]\)/\U\1/g')Skill(Skill):
    """Agent-OS compatible skill for $project_name"""

    def __init__(self):
        super().__init__(
            name="$project_name",
            description="AI-LAB generated skill",
            version="1.0.0"
        )

    async def execute(self, context: Context) -> dict:
        """Execute the skill logic"""
        return await main_handler(context)

# Register skill
skill = $(echo "$project_name" | sed 's/^./\U&/' | sed 's/-\([a-z]\)/\U\1/g')Skill()
EOF
}

# Function to generate data pipeline files
generate_data_pipeline_files() {
    local project_path=$1
    local project_name=$2

    cat > "$project_path/src/main.py" << EOF
"""
Data Pipeline: $project_name
Generated with AI-LAB Project Generator
"""

import asyncio
from src.extract.extractors import main_extractor
from src.transform.transformers import main_transformer
from src.load.loaders import main_loader

async def run_pipeline():
    """Run the complete data pipeline"""
    # Extract
    raw_data = await main_extractor()

    # Transform
    processed_data = await main_transformer(raw_data)

    # Load
    await main_loader(processed_data)

    print("Pipeline completed successfully")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
EOF
}

# Function to generate microservice files
generate_microservice_files() {
    local project_path=$1
    local project_name=$2

    cat > "$project_path/src/main.py" << EOF
"""
Microservice: $project_name
Generated with AI-LAB Project Generator
"""

from fastapi import FastAPI
from src.api import routes
from src.health.health_checker import health_router

app = FastAPI(
    title="$project_name Microservice",
    description="Microservice for $project_name",
    version="1.0.0"
)

# Include routers
app.include_router(routes.router, prefix="/api/v1")
app.include_router(health_router, prefix="/health")

@app.get("/")
async def root():
    return {"service": "$project_name", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
}

# Function to generate Docker files
generate_docker_files() {
    local project_path=$1
    local template=$2

    print_color $BLUE "Generating Docker configuration..."

    cat > "$project_path/Dockerfile" << EOF
# AI-LAB Generated Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "-m", "src.main"]
EOF

    cat > "$project_path/docker-compose.yml" << EOF
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

$([ "$DATABASE" = "postgresql" ] && cat << POSTGRES_DB

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  postgres_data:
POSTGRES_DB
)

$([ "$DATABASE" = "mysql" ] && cat << MYSQL_DB

  db:
    image: mysql:8
    environment:
      MYSQL_DATABASE: app
      MYSQL_USER: app
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
    restart: unless-stopped

volumes:
  mysql_data:
MYSQL_DB
)

$([ "$DATABASE" = "mongodb" ] && cat << MONGO_DB

  db:
    image: mongo:7
    environment:
      MONGO_INITDB_ROOT_USERNAME: app
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongo_data:/data/db
    ports:
      - "27017:27017"
    restart: unless-stopped

volumes:
  mongo_data:
MONGO_DB
)

$([ "$DATABASE" = "redis" ] && cat << REDIS

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
REDIS
)
EOF

    # Generate .dockerignore
    cat > "$project_path/.dockerignore" << EOF
# Git
.git
.gitignore

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment
.env
.env.local

# Development
tests/
docs/
*.md

# AI-LAB
.ai-lab/local/
.ai-lab/cache/
EOF

    print_color $GREEN "✓ Docker configuration generated"
}

# Function to generate GitHub Actions workflow
generate_github_actions() {
    local project_path=$1
    local template=$2

    print_color $BLUE "Generating GitHub Actions workflow..."

    mkdir -p "$project_path/.github/workflows"

    cat > "$project_path/.github/workflows/ci.yml" << EOF
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python \${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: \${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Lint with flake8
      run: |
        flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 src/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

    - name: Format check with black
      run: black --check src/

    - name: Import sort check with isort
      run: isort --check-only src/

    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=src --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v4

    - name: Build Docker image
      run: docker build -t \${{ github.repository }}:\${{ github.sha }} .

    - name: Run security scan
      run: |
        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \\
          -v \${{ github.workspace }}:/root/.cache/ aquasec/trivy:latest \\
          image \${{ github.repository }}:\${{ github.sha }}
EOF

    print_color $GREEN "✓ GitHub Actions workflow generated"
}

# Function to validate project creation
validate_project() {
    local project_path=$1

    print_color $BLUE "Validating generated project..."

    # Check if all required directories exist
    local required_dirs=("src" "tests" "docs" "scripts" "config" ".ai-lab")
    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$project_path/$dir" ]]; then
            print_color $RED "✗ Missing directory: $dir"
            return 1
        fi
    done

    # Check if all required files exist
    local required_files=("README.md" ".gitignore" "Makefile" "requirements.txt" ".env.example")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$project_path/$file" ]]; then
            print_color $RED "✗ Missing file: $file"
            return 1
        fi
    done

    # Check AI-LAB metadata
    local ai_lab_files=(".ai-lab/project-spec.yml" ".ai-lab/standards.yml" ".ai-lab/generated-by.yml")
    for file in "${ai_lab_files[@]}"; do
        if [[ ! -f "$project_path/$file" ]]; then
            print_color $RED "✗ Missing AI-LAB metadata: $file"
            return 1
        fi
    done

    print_color $GREEN "✓ Project validation passed"
    return 0
}

# Function to print success message
print_success() {
    local project_path=$1
    local project_name=$2
    local template=$3

    print_color $GREEN "🎉 Project '$project_name' created successfully!"
    echo
    print_color $BLUE "Next steps:"
    echo "  1. cd $project_path"
    echo "  2. make install"
    echo "  3. make dev"
    echo
    print_color $BLUE "Project location: $project_path"
    print_color $BLUE "Template: $template"
    if [[ "$DATABASE" != "none" ]]; then
        print_color $BLUE "Database: $DATABASE"
    fi
    if [[ "$FRONTEND" != "none" ]]; then
        print_color $BLUE "Frontend: $FRONTEND"
    fi
    if [[ "$AGENT_OS" = "true" ]]; then
        print_color $BLUE "Agent-OS: Enabled"
    fi
    echo
    print_color $YELLOW "Remember to:"
    echo "  - Update .env with your configuration"
    echo "  - Set up your database $([ "$DATABASE" != "none" ] && echo "connection")"
    echo "  - Configure your CI/CD pipeline"
    echo "  - Read the AI-LAB guidelines"
}

# Main function
main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help)
                HELP=true
                shift
                ;;
            --database)
                DATABASE="$2"
                shift 2
                ;;
            --frontend)
                FRONTEND="$2"
                shift 2
                ;;
            --agent-os)
                AGENT_OS=true
                shift
                ;;
            -*)
                print_color $RED "Unknown option: $1"
                print_help
                exit 1
                ;;
            *)
                if [[ -z "$TEMPLATE_TYPE" ]]; then
                    TEMPLATE_TYPE="$1"
                elif [[ -z "$PROJECT_NAME" ]]; then
                    PROJECT_NAME="$1"
                else
                    print_color $RED "Too many arguments"
                    print_help
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Show help if requested
    if [[ "$HELP" = true ]]; then
        print_help
        exit 0
    fi

    # Validate required arguments
    if [[ -z "$TEMPLATE_TYPE" || -z "$PROJECT_NAME" ]]; then
        print_color $RED "Missing required arguments"
        print_help
        exit 1
    fi

    # Validate template type
    if ! validate_template "$TEMPLATE_TYPE"; then
        print_color $RED "Invalid template type: $TEMPLATE_TYPE"
        print_color $YELLOW "Available templates: ${AVAILABLE_TEMPLATES[*]}"
        exit 1
    fi

    # Validate project name
    if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        print_color $RED "Invalid project name: $PROJECT_NAME"
        print_color $YELLOW "Project name must contain only letters, numbers, hyphens, and underscores"
        exit 1
    fi

    # Check if project directory already exists
    if [[ -d "$PROJECT_NAME" ]]; then
        print_color $RED "Directory '$PROJECT_NAME' already exists"
        exit 1
    fi

    # Validate options
    if [[ -n "$DATABASE" && "$DATABASE" != "postgresql" && "$DATABASE" != "mysql" && "$DATABASE" != "sqlite" && "$DATABASE" != "mongodb" ]]; then
        print_color $RED "Invalid database type: $DATABASE"
        print_color $YELLOW "Supported databases: postgresql, mysql, sqlite, mongodb"
        exit 1
    fi

    if [[ -n "$FRONTEND" && "$FRONTEND" != "react" && "$FRONTEND" != "vue" && "$FRONTEND" != "svelte" && "$FRONTEND" != "angular" ]]; then
        print_color $RED "Invalid frontend framework: $FRONTEND"
        print_color $YELLOW "Supported frameworks: react, vue, svelte, angular"
        exit 1
    fi

    # Create project
    print_color $BLUE "Creating AI-LAB project: $PROJECT_NAME"
    print_color $BLUE "Template: $TEMPLATE_TYPE"

    local project_path="$(pwd)/$PROJECT_NAME"

    # Create project structure
    create_directory_structure "$project_path" "$TEMPLATE_TYPE"

    # Generate configuration
    generate_config "$project_path" "$PROJECT_NAME" "$TEMPLATE_TYPE"

    # Generate base files
    generate_base_files "$project_path" "$PROJECT_NAME" "$TEMPLATE_TYPE"

    # Generate template-specific files
    generate_template_files "$project_path" "$PROJECT_NAME" "$TEMPLATE_TYPE"

    # Generate Docker files
    generate_docker_files "$project_path" "$TEMPLATE_TYPE"

    # Generate GitHub Actions
    generate_github_actions "$project_path" "$TEMPLATE_TYPE"

    # Validate project
    if validate_project "$project_path"; then
        print_success "$project_path" "$PROJECT_NAME" "$TEMPLATE_TYPE"
    else
        print_color $RED "Project validation failed"
        exit 1
    fi
}

# Run main function
main "$@"
