# GitHub Auto-Sync Integration - Usage Guide

## Overview

The AI Lab Framework now provides **automatic GitHub synchronization** for work items, ideas, and tasks. Whenever you change the status or priority of an item in the local database, it automatically syncs to the corresponding GitHub Issue.

## Features

✅ **Automatic Status Sync**: Changes to `status` field automatically update GitHub issue labels  
✅ **Automatic Priority Sync**: Changes to `priority` field automatically update GitHub issue labels  
✅ **Bidirectional Sync**: Manual sync from GitHub back to local database  
✅ **Rate Limiting**: Built-in delays to respect GitHub API limits  
✅ **Error Handling**: Graceful handling of sync failures with logging  

## Setup

### 1. Environment Configuration
```bash
export GITHUB_TOKEN="your_github_token_with_workflow_scope"
export GITHUB_REPO="owner/repository"
```

### 2. Initialize Database with Auto-Sync
```python
from infrastructure.db.database import init_db
init_db()  # This now includes auto-sync setup
```

## Usage Methods

### Method 1: Helper Functions (Recommended)

Use the convenient helper functions for guaranteed sync:

```python
from infrastructure.db.sync_helpers import sync_work_item, sync_idea

# Update work item with auto-sync
sync_work_item("WORK-ITEM-001", new_status="in_progress", new_priority="high")

# Update idea with auto-sync  
sync_idea("IDEA-001", new_status="refining", new_priority="critical")
```

### Method 2: Direct Database Operations

For more control, use direct database operations:

```python
from infrastructure.db.database import SessionLocal
from infrastructure.db.models.models import WorkItem

session = SessionLocal()
work_item = session.query(WorkItem).filter(WorkItem.id == "WORK-ITEM-001").first()

# Make changes
work_item.status = "done"
work_item.priority = "low"

# Commit to trigger auto-sync (if event listeners are working)
session.commit()

# Or manually trigger sync
from infrastructure.db.auto_sync import auto_sync
auto_sync.sync_work_item_status(work_item.id, work_item.status)
auto_sync.sync_priority_change("work_item", work_item.id, work_item.priority)

session.close()
```

## Status Mappings

### Work Items
- `todo` → `status:todo` label
- `in_progress` → `status:in_progress` label  
- `review` → `status:review` label
- `done` → `status:done` label
- `blocked` → `status:blocked` label

### Ideas
- `backlog` → `status:backlog` label
- `refining` → `status:refining` label
- `ready` → `status:ready` label
- `implemented` → `status:implemented` label
- `archived` → `status:archived` label

## Priority Mappings (Both Types)
- `low` → `priority:low` label
- `medium` → `priority:medium` label
- `high` → `priority:high` label
- `critical` → `priority:critical` label

## GitHub Integration Commands

### Full Sync (Setup + Bidirectional Sync)
```bash
python -m ai_lab_framework.github_integration --action sync-all
```

### Sync to GitHub Only
```bash
python -m ai_lab_framework.github_integration --action sync-to-github
```

### Sync from GitHub Only
```bash
python -m ai_lab_framework.github_integration --action sync-from-github
```

### Setup Repository Labels
```bash
python -m ai_lab_framework.github_integration --action setup
```

## Testing

Run the test suite to verify your setup:

```bash
# Test helper functions
python test_sync_helpers.py

# Test manual sync
python test_auto_sync.py
```

## Error Handling

The sync system includes comprehensive error handling:

- **Missing GitHub Credentials**: Graceful fallback with warning
- **Network Issues**: Automatic retry with exponential backoff
- **Rate Limiting**: Built-in delays to respect GitHub limits
- **Invalid Issues**: Skips items without GitHub issue IDs

## Best Practices

1. **Use Helper Functions**: Prefer `sync_work_item()` and `sync_idea()` for guaranteed sync
2. **Check GitHub Issue ID**: Only items with `github_issue_id` will sync
3. **Monitor Logs**: Watch for sync success/failure messages
4. **Batch Updates**: Use transactions for multiple related changes
5. **Handle Failures**: Always check return values from sync functions

## Troubleshooting

### Auto-Sync Not Working
1. Check environment variables: `GITHUB_TOKEN` and `GITHUB_REPO`
2. Verify GitHub token has `repo` and `workflow` scopes
3. Ensure items have `github_issue_id` set
4. Use helper functions as fallback

### Rate Limiting
1. Built-in delays prevent most rate limiting
2. If rate limited, wait a few minutes and retry
3. Consider GitHub API limits for larger batches

### Sync Failures
1. Check network connectivity
2. Verify repository permissions
3. Check GitHub service status
4. Review error messages in logs

## Integration with Existing Code

To add auto-sync to existing code:

```python
# Before (no sync)
work_item.status = "done"
session.commit()

# After (with auto-sync)
from infrastructure.db.sync_helpers import sync_work_item
sync_work_item(work_item.id, new_status="done")
```

The sync system is designed to be non-intrusive and work alongside your existing database operations.