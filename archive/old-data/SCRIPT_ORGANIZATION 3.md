# AI Lab Framework - Script & Tool Organization

## 📁 New Directory Structure

### 🚀 Executable Scripts (`bin/`)
**Purpose**: System-level executable scripts and utilities
```bash
bin/
├── backup.sh           # Framework backup utility
└── sync-docs.sh        # Documentation synchronization
```

### 🔧 Development Tools (`dev-tools/`)
**Purpose**: AI tools and development utilities
```bash
dev-tools/
├── dataprocessor_tool.py    # Generated AI tool (DataProcessor)
├── mytool_tool.py          # Generated AI tool (MyTool)
└── test_dataprocessor_tool.py  # Test utility
```

### 🛠️ Utility Scripts (`utils/`)
**Purpose**: Helper scripts and utilities
```bash
utils/
└── list_ideas.py          # Ideas listing utility
```

### 📦 Standalone Tools (`tools/`)
**Purpose**: Independent, specialized tools
```bash
tools/
├── fritzbox/             # Fritz!Box API tool
└── hisense-tv/           # Hisense TV control tool
```

## 🔄 Migration Summary

### Before Cleanup
- Scripts scattered in root and `scripts/`
- Development tools in root directory
- Inconsistent organization
- Mixed naming conventions

### After Cleanup
- **Logical grouping** by function and purpose
- **Clear separation** of concerns
- **Consistent naming** (kebab-case)
- **Proper permissions** for executables

## 📋 Usage Instructions

### Executable Scripts
```bash
# Run backup
./bin/backup.sh

# Sync documentation
./bin/sync-docs.sh
```

### Development Tools
```bash
# Run AI tools (from framework root)
python3 dev-tools/dataprocessor_tool.py
python3 dev-tools/mytool_tool.py
python3 dev-tools/test_dataprocessor_tool.py
```

### Utility Scripts
```bash
# List ideas (updated in Makefile)
make idea-list
# or directly:
python3 utils/list_ideas.py
```

## 🎯 Benefits

### Organization
- **Clear purpose** for each directory
- **Logical grouping** of related tools
- **Easy navigation** and discovery

### Maintenance
- **Reduced clutter** in root directory
- **Consistent structure** for new tools
- **Simplified backup** and deployment

### Development
- **Separate concerns** for different tool types
- **Scalable structure** for future growth
- **Clear import paths** and dependencies

## 🔄 Updated References

### Makefile Updates
- `scripts/list_ideas.py` → `utils/list_ideas.py` ✓

### Documentation Updates
- Framework structure documentation updated
- Tool READMEs to reference new locations
- Getting started guide updated

### Import Path Updates
- Development tools may need import path adjustments
- Framework integration paths verified

---
**Organization completed: 2025-11-09**
**Status**: ✅ Complete
**Impact**: Cleaner, more maintainable structure
