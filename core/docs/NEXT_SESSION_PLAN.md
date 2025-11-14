# AI Lab Framework - Next Session Plan

**Session Goal:** Properly separate ai-lab from ai-lab-framework and fix all database issues

**Date:** Next Session  
**Priority:** CRITICAL

---

## 🎯 **Architecture Clarification**

### **Current State (WRONG):**
- ❌ ai-lab and ai-lab-framework are mixed together
- ❌ Database infrastructure broken
- ❌ No clear separation of concerns

### **Target State (CORRECT):**

#### **ai-lab-framework** (Foundation/Library)
- ✅ Installable/deployable package
- ✅ Core framework functionality only
- ✅ Database infrastructure working
- ✅ No project-specific code
- ✅ Can be deployed to any project repo

#### **ai-lab** (Project Management Hub)
- ✅ GitHub integration and project management
- ✅ Tools for ecosystem operations
- ✅ Backup system for all projects
- ✅ Project orchestration and monitoring
- ✅ Uses ai-lab-framework as dependency

#### **Project Repositories** (e.g., homelab-agent-os)
- ✅ Independent repositories
- ✅ Own project folders inside ai-lab
- ✅ Use ai-lab-framework as foundation
- ✅ Managed through ai-lab hub

---

## 🔧 **Critical Fixes Needed**

### **1. Database Infrastructure Fix**
```bash
# Install missing dependencies
pip install sqlalchemy PyGithub structlog

# Fix database models and connections
# Test all database operations
# Migrate JSON work items to database
```

### **2. Separate ai-lab-framework**
- Remove project-specific code from framework
- Make framework installable package
- Fix all database dependencies
- Create deployment scripts for framework
- Test framework as standalone package

### **3. Restructure ai-lab**
- Keep only project management tools
- Implement GitHub integration properly
- Add project orchestration features
- Create backup system for all projects
- Use ai-lab-framework as dependency

### **4. Project Structure Fix**
```
ai-lab-framework/          # Installable framework package
├── src/ai_lab_framework/
├── pyproject.toml          # Package configuration
├── README.md              # Framework documentation
└── tests/                 # Framework tests

ai-lab/                    # Project management hub
├── projects/               # Project folders
│   ├── homelab-agent-os/  # Independent project
│   ├── mobile-app-kit/      # Another project
│   └── ...
├── tools/                  # Management tools
├── scripts/                # Orchestration scripts
└── uses ai-lab-framework as dependency
```

---

## 📋 **Next Session Tasks**

### **Phase 1: Database Fix (1 hour)**
1. Install missing dependencies
2. Fix SQLAlchemy imports and connections
3. Test database operations
4. Migrate JSON work items to database
5. Verify all database functionality

### **Phase 2: Framework Separation (2 hours)**
1. Create clean ai-lab-framework structure
2. Move framework code to proper location
3. Remove project-specific code from framework
4. Make framework installable package
5. Test framework deployment

### **Phase 3: ai-lab Restructuring (2 hours)**
1. Clean up ai-lab repository
2. Keep only project management tools
3. Implement proper GitHub integration
4. Add project orchestration features
5. Set up backup system

### **Phase 4: Project Setup (1 hour)**
1. Create proper project structure
2. Set up homelab-agent-os as independent project
3. Configure project to use ai-lab-framework
4. Test project management through ai-lab
5. Verify backup and orchestration

---

## 🎯 **Success Criteria**

### **ai-lab-framework:**
- ✅ Installable via pip/poetry
- ✅ Database operations working
- ✅ No project-specific dependencies
- ✅ Can be deployed to any repo
- ✅ All tests passing

### **ai-lab:**
- ✅ Clean project management interface
- ✅ GitHub integration working
- ✅ Project orchestration functional
- ✅ Backup system operational
- ✅ Uses framework as dependency

### **Projects:**
- ✅ Independent repositories
- ✅ Proper folder structure
- ✅ Framework integration working
- ✅ Managed through ai-lab hub

---

## 🚀 **Implementation Commands**

### **Database Fix:**
```bash
# Install dependencies
pip install sqlalchemy PyGithub structlog

# Test database
python -c "from sqlalchemy import create_engine; print('✅ DB OK')"

# Migrate data
python scripts/migrate_work_items_sqlalchemy.py --force-update
```

### **Framework Separation:**
```bash
# Create clean framework
git checkout -b feature/framework-separation
# Move framework code
# Update pyproject.toml
# Test installation
pip install -e ./ai-lab-framework
```

### **Project Setup:**
```bash
# Restructure ai-lab
git checkout -b feature/ai-lab-restructure
# Move project management code
# Update dependencies
# Test orchestration
```

---

## 📊 **Expected Outcome**

After this session:
- ✅ Database infrastructure fully functional
- ✅ Clear separation of concerns
- ✅ Installable framework package
- ✅ Proper project management hub
- ✅ Scalable architecture for multiple projects
- ✅ All CI/CD pipelines working
- ✅ Foundation for future project creation

---

**🎯 This is a critical architectural refactoring that will fix all current issues and establish a solid foundation for the entire ecosystem!**