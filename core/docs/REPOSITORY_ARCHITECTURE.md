# AI Lab Multi-Repository Architecture & Deployment Strategy

## 🏗️ **Repository Architecture Overview**

The AI Lab ecosystem consists of multiple specialized repositories that work together to provide a complete intelligent development environment.

### **📦 Repository Structure**

#### **1. ai-lab-framework** (Core Library)
**Purpose**: Installable Python package providing core framework functionality

**Structure**:
```
ai-lab-framework/
├── src/
│   └── ai_lab_framework/
│       ├── __init__.py
│       ├── cli.py                 # Main CLI interface
│       ├── core/                  # Core framework logic
│       │   ├── profiles.py        # Three-tier profile system
│       │   ├── templates.py       # Project scaffolding
│       │   └── config.py          # Configuration management
│       ├── infrastructure/        # Database & infrastructure
│       │   ├── db/
│       │   │   ├── database.py    # SQLAlchemy configuration
│       │   │   └── models/        # ORM models
│       │   └── github/           # GitHub integration
│       └── tools/                 # Framework utilities
├── pyproject.toml                 # Package configuration
├── README.md
└── tests/
```

**Responsibilities**:
- ✅ Three-tier profile system (Basic/Standard/Advanced)
- ✅ Project template generation
- ✅ Database models and infrastructure
- ✅ GitHub integration utilities
- ✅ CLI tools for framework operations

---

#### **2. ai-lab** (Project Management Hub)
**Purpose**: Central project management and monitoring system

**Structure**:
```
ai-lab/
├── src/
│   └── ai_lab/                    # Project management application
│       ├── dashboard/             # Real-time monitoring
│       ├── management/            # Work items & ideas
│       ├── logging/               # AI session tracking
│       └── backup/                # Backup utilities
├── data/
│   ├── ai_lab.db                 # SQLite database
│   ├── schemas/                  # JSON schemas
│   └── work-items/               # Work item definitions
├── scripts/                      # Automation scripts
├── dashboard.html                # Main dashboard
└── run.py                       # Interactive CLI
```

**Responsibilities**:
- ✅ Real-time dashboard monitoring
- ✅ Work item and idea management
- ✅ AI session logging
- ✅ Backup and archival
- ✅ Project orchestration

---

#### **3. Project Repositories** (Individual Projects)
**Purpose**: Independent projects using the ai-lab-framework

**Structure**:
```
project-name/
├── .ai-lab/                      # Framework configuration
│   ├── profile.yaml             # Active profile
│   ├── config.yaml              # Project config
│   └── templates/               # Custom templates
├── src/                         # Project source code
├── docs/                        # Project documentation
├── tests/                       # Project tests
└── pyproject.toml              # Project dependencies
```

**Examples**:
- `homelab-agent-os/` - Home automation system
- `ai-lab-dashboard/` - Dashboard enhancements
- `custom-projects/` - User-specific projects

---

## 🔄 **Repository Interactions**

### **Dependency Flow**:
```
ai-lab-framework (library) 
    ↓ installed as dependency
ai-lab (management hub)
    ↓ creates/manages
project repositories
```

### **Data Flow**:
```
Project Repositories → ai-lab → Dashboard
     (work items)    (management)  (monitoring)
```

### **GitHub Integration**:
```
Project Repositories ↔ GitHub ↔ ai-lab
     (issues)            (sync)      (tracking)
```

---

## 🚀 **Deployment Strategy**

### **Phase 1: Framework Separation**
1. **Extract ai-lab-framework**:
   ```bash
   # Create framework package
   mkdir ai-lab-framework
   # Move core framework code
   # Configure as installable package
   # Publish to PyPI/private registry
   ```

2. **Refactor ai-lab**:
   ```bash
   # Remove framework code
   # Add ai-lab-framework as dependency
   # Update imports and references
   # Test functionality
   ```

### **Phase 2: Repository Setup**
1. **Create GitHub repositories**:
   - `ai-lab-framework` (public)
   - `ai-lab` (private)
   - Project repos (as needed)

2. **Configure GitHub integration**:
   - GitHub Apps for issue sync
   - Webhooks for real-time updates
   - PAT authentication for automation

### **Phase 3: Deployment Automation**
1. **CI/CD Pipelines**:
   ```yaml
   # .github/workflows/ci-cd.yml
   name: AI Lab Framework CI/CD
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Setup Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         - name: Install dependencies
           run: |
             pip install -e .
             pip install -r requirements-dev.txt
         - name: Run tests
           run: pytest --cov=src
         - name: Lint code
           run: |
             black --check .
             ruff check .
             mypy .
     deploy:
       needs: test
       if: github.ref == 'refs/heads/main'
       runs-on: ubuntu-latest
       steps:
         - name: Deploy to PyPI
           run: |
             python -m build
             twine upload dist/*
   ```

2. **Release Management**:
   ```bash
   # Semantic versioning
   # Automated changelog generation
   # GitHub releases with assets
   # Docker containerization
   ```

---

## 🔧 **Installation & Setup**

### **Framework Installation**:
```bash
# Install from PyPI
pip install ai-lab-framework

# Install from source (development)
git clone https://github.com/your-org/ai-lab-framework.git
cd ai-lab-framework
pip install -e .
```

### **Project Management Hub Setup**:
```bash
# Clone ai-lab repository
git clone https://github.com/your-org/ai-lab.git
cd ai-lab

# Install dependencies
pip install -r requirements.txt
pip install ai-lab-framework

# Initialize database
python -m ai_lab.infrastructure.db.database init_db

# Start dashboard
python run.py dashboard
```

### **New Project Creation**:
```bash
# Using framework CLI
ai-lab create-project my-new-project --profile standard

# Or using ai-lab hub
python run.py create-project --name my-new-project --template agent-os
```

---

## 📊 **Monitoring & Maintenance**

### **Dashboard Monitoring**:
- Real-time project metrics
- Work item progress tracking
- System health monitoring
- AI session analytics

### **Backup Strategy**:
```bash
# Automated daily backups
python scripts/backup.py --schedule daily

# Database backups
python scripts/backup_db.py --compress --encrypt

# Project archival
python scripts/archive_project.py --project-name old-project
```

### **Update Management**:
```bash
# Framework updates
pip install --upgrade ai-lab-framework

# Project synchronization
python run.py sync-projects --all

# Database migrations
python -m ai_lab.infrastructure.db.migrations upgrade
```

---

## 🔐 **Security Considerations**

### **Access Control**:
- GitHub repository permissions
- API key management
- Database encryption
- Backup security

### **Isolation**:
- Separate databases per project
- Containerized deployments
- Network segmentation
- Environment separation

---

## 🎯 **Success Metrics**

### **Framework Adoption**:
- Number of projects using framework
- Installation count (PyPI downloads)
- Community contributions
- Issue resolution time

### **System Health**:
- Dashboard uptime
- Database performance
- Backup success rate
- GitHub sync reliability

### **Developer Experience**:
- Project setup time
- Template usage
- Documentation quality
- Community satisfaction

---

## 📝 **Next Steps**

1. **Immediate Actions**:
   - [ ] Complete framework separation
   - [ ] Set up GitHub repositories
   - [ ] Configure CI/CD pipelines
   - [ ] Test deployment automation

2. **Short-term Goals** (1-2 weeks):
   - [ ] Migrate existing projects
   - [ ] Implement GitHub integration
   - [ ] Create documentation
   - [ ] Onboard team members

3. **Long-term Vision** (1-3 months):
   - [ ] Public framework release
   - [ ] Community building
   - [ ] Advanced features
   - [ ] Enterprise support

---

*This architecture provides a scalable, maintainable, and secure foundation for the AI Lab ecosystem while enabling rapid development and deployment of intelligent automation projects.*