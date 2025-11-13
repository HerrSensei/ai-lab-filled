# AI Lab Framework

**Version:** 2.0 (Clean Rebuild)  
**Status:** ✅ Ready for Development  

## 🎯 What This Is

A clean, organized rebuild of the AI Lab Framework that preserves all valuable components while eliminating the mess that made the original project unmanageable.

## 🚀 Quick Start

```bash
# Install dependencies
poetry install

# Set up development environment
make setup

# Run tests
make test

# Create your first project
python -m ai_lab.tools.project_creator
```

## 📁 Structure

- **`src/`** - Core framework code with AI tool abstractions
- **`data/`** - JSON-based work management (schemas, work items, ideas)
- **`core/`** - Templates, documentation, and guidelines
- **`tools/`** - Specific tool implementations
- **`projects/`** - Generated projects (empty, ready for use)

## 📋 What's Included

✅ **Core Framework** - Three-tier profile system, context management, structured logging  
✅ **Data Management** - JSON schemas, 30+ work items, 11 innovation ideas  
✅ **Templates** - Complete project scaffolding for different types  
✅ **Documentation** - 20+ CLI workflows, vision, guidelines  
✅ **Tools** - FritzBox MCP server implementation  
✅ **Configuration** - Modern Python setup with Poetry, dev tools  

## 📖 Full Details

See `REBUILD_REPORT.md` for complete documentation of what was preserved and the rebuild process.

## 🎯 Next Steps

1. Run `poetry install` to set up the environment
2. Use `core/templates/` to generate new projects
3. Check `data/work-items/` for existing tasks
4. Review `core/docs/CLI_WORKFLOWS.md` for standard procedures

---

*This clean rebuild preserves 90+ valuable components while providing a maintainable structure for future development.*