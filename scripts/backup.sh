#!/bin/bash
# AI Lab Framework - Backup Script
# Creates comprehensive backup of the framework

set -e

BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="ai-lab-backup-${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

echo "🔄 Creating AI Lab Framework backup..."

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Create backup archive
echo "📦 Packing framework files..."
tar -czf "${BACKUP_PATH}.tar.gz" \
    --exclude='backups' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.pytest_cache' \
    --exclude='node_modules' \
    --exclude='.git' \
    .

# Create backup metadata
echo "📋 Creating backup metadata..."
cat > "${BACKUP_DIR}/backup-${TIMESTAMP}.json" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "backup_name": "${BACKUP_NAME}",
    "backup_file": "${BACKUP_PATH}.tar.gz",
    "framework_version": "2.0.0",
    "description": "AI Lab Framework automated backup",
    "includes": [
        "src/",
        "data/",
        "core/",
        "projects/",
        "templates/",
        "scripts/",
        "dashboard/",
        "ai-logs/",
        "docs/",
        "*.md",
        "*.json",
        "*.toml",
        "Makefile"
    ],
    "excludes": [
        "backups/",
        "__pycache__/",
        "*.pyc",
        ".pytest_cache/",
        "node_modules/",
        ".git/"
    ]
}
EOF

echo "✅ Backup completed successfully!"
echo "📁 Backup location: ${BACKUP_PATH}.tar.gz"
echo "📊 Size: $(du -h "${BACKUP_PATH}.tar.gz" | cut -f1)"
echo "📋 Metadata: ${BACKUP_DIR}/backup-${TIMESTAMP}.json"

# Cleanup old backups (keep last 5)
echo "🧹 Cleaning up old backups..."
cd "${BACKUP_DIR}"
ls -t backup-*.json | tail -n +6 | xargs -r rm
ls -t ai-lab-backup-*.tar.gz | tail -n +6 | xargs -r rm

echo "🎯 Backup process completed!"