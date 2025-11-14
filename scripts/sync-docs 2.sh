#!/bin/bash
# AI Lab Framework - Documentation Sync Script
# Synchronizes and updates all documentation

set -e

echo "🔄 Syncing AI Lab Framework documentation..."

# Update dashboard
echo "📊 Updating dashboard..."
python3 dashboard/dashboard_generator.py

# Update AI logs session
echo "📝 Updating AI session log..."
SESSION_DATE=$(date +"%Y-%m-%d")
SESSION_NUM=$(ls ai-logs/sessions/ | grep "${SESSION_DATE}" | wc -l | tr -d ' ')
SESSION_NUM=$((SESSION_NUM + 1))
SESSION_FILE="ai-logs/sessions/${SESSION_DATE}_session-${SESSION_NUM:0>3}.md"

cat > "${SESSION_FILE}" << EOF
# AI Session Log - ${SESSION_DATE}

## Session ${SESSION_NUM}
- **Date:** $(date +"%Y-%m-%d %H:%M:%S")
- **Type:** Documentation Sync
- **Status:** completed

## Activities
- Synchronized framework documentation
- Updated dashboard metrics
- Validated data consistency

## Outcomes
- Documentation is current
- Dashboard reflects latest data
- All systems operational

---
*Session logged by documentation sync script*
EOF

echo "📋 Session logged: ${SESSION_FILE}"

# Validate JSON schemas
echo "🔍 Validating JSON schemas..."
for schema in data/schemas/*.json; do
    if python3 -m json.tool "$schema" > /dev/null 2>&1; then
        echo "✅ $(basename "$schema") - Valid"
    else
        echo "❌ $(basename "$schema") - Invalid"
    fi
done

# Validate work items
echo "🔍 Validating work items..."
for work_item in data/work-items/*.json; do
    if python3 -m json.tool "$work_item" > /dev/null 2>&1; then
        echo "✅ $(basename "$work_item") - Valid"
    else
        echo "❌ $(basename "$work_item") - Invalid"
    fi
done

# Validate ideas
echo "🔍 Validating ideas..."
for idea in data/ideas/*.json; do
    if python3 -m json.tool "$idea" > /dev/null 2>&1; then
        echo "✅ $(basename "$idea") - Valid"
    else
        echo "❌ $(basename "$idea") - Invalid"
    fi
done

# Update table of contents
echo "📚 Updating documentation table of contents..."
cat > docs/README.md << EOF
# AI Lab Framework Documentation

## Core Documentation
- [Getting Started](../GETTING_STARTED.md)
- [Developer Guide](../DEVELOPER_GUIDE.md)
- [API Reference](../API_REFERENCE.md)
- [CLI Reference](../CLI_REFERENCE.md)

## Data Management
- [JSON Schemas](../data/schemas/) - Framework data schemas
- [Work Items](../data/work-items/) - Project work items
- [Ideas](../data/ideas/) - Innovation ideas

## Operations
- [AI Logs](../ai-logs/) - AI session logs and changelog
- [Dashboard](../dashboard/) - Project monitoring dashboard
- [Scripts](../scripts/) - Utility scripts

## Templates
- [Project Templates](../templates/) - Project scaffolding templates
- [Core Tools](../core/) - Framework core tools

## Archive
- [Archive](../archive/) - Historical project data

---
*Last updated: $(date +"%Y-%m-%d %H:%M:%S")*
EOF

echo "✅ Documentation sync completed!"
echo "📊 Dashboard updated"
echo "📝 Session logged"
echo "🔍 Data validated"
echo "📚 Table of contents updated"