# Framework Items Priority Analysis (FRM-007 through FRM-014)

## 🔴 High Priority (Immediate Action Required)

### FRM-007: Pre-commit Hook Cleanup and Standardization
- **Status**: in_progress
- **Priority**: High
- **Estimated**: 8 hours
- **Dependencies**: None
- **Why Critical**: Blocking code quality and CI/CD pipeline
- **Action**: Run `pre-commit run --all-files` and fix all failures

### FRM-008: CLI Tooling for Framework Self-Improvement
- **Status**: open
- **Priority**: High
- **Estimated**: 40 hours
- **Dependencies**: None
- **Why Critical**: Enables AI agents to improve the framework itself
- **Action**: Create CLI workflows for common framework tasks

### FRM-010: Redundancy Cleanup
- **Status**: open
- **Priority**: High
- **Estimated**: 4 hours
- **Dependencies**: None
- **Why Critical**: Reduces confusion and improves maintainability
- **Action**: Remove all files ending with ' 2.md' after review

### FRM-011: Fix Progress Metric Logic
- **Status**: open
- **Priority**: High
- **Estimated**: 8 hours
- **Dependencies**: FRM-010
- **Why Critical**: Dashboard shows misleading 100% progress
- **Action**: Refactor dashboard to use work item completion data

## 🟡 Medium Priority (Important but Less Urgent)

### FRM-009: Naming Convention Refinement
- **Status**: open
- **Priority**: Medium
- **Estimated**: 20 hours
- **Dependencies**: None
- **Why Important**: Improves code readability and AI agent comprehension
- **Action**: Create naming guidelines and enforce via linting

### FRM-012: Consolidate Tooling and Makefile
- **Status**: open
- **Priority**: Medium
- **Estimated**: 6 hours
- **Dependencies**: None
- **Why Important**: Simplifies developer experience
- **Action**: Fix Makefile and add missing dashboard-update target

### FRM-013: Project Vision Alignment Audit
- **Status**: open
- **Priority**: Medium
- **Estimated**: 12 hours
- **Dependencies**: None
- **Why Important**: Ensures strategic focus
- **Action**: Audit all projects and archive misaligned ones

### FRM-014: Update and Correct Framework Documentation
- **Status**: open
- **Priority**: Medium
- **Estimated**: 10 hours
- **Dependencies**: FRM-012
- **Why Important**: Accurate docs essential for AI agents
- **Action**: Update GEMINI.md and verify all commands

## 📋 Recommended Execution Order

1. **FRM-007** (Pre-commit cleanup) - Unblock development
2. **FRM-010** (Redundancy cleanup) - Quick win, unblocks FRM-011
3. **FRM-011** (Progress metrics) - Fix misleading dashboard
4. **FRM-008** (CLI tooling) - Strategic capability
5. **FRM-012** (Makefile consolidation) - Improves DX
6. **FRM-014** (Documentation update) - Depends on FRM-012
7. **FRM-009** (Naming conventions) - Long-term quality
8. **FRM-013** (Project audit) - Strategic alignment

## 🎯 Immediate Next Steps

1. Run pre-commit check to identify current issues
2. Start with FRM-007 to unblock development workflow
3. Quick cleanup of redundant files (FRM-010)
4. Fix dashboard metrics (FRM-011)

**Total Estimated Effort**: 108 hours (~13.5 working days)
**Critical Path Items**: FRM-007 → FRM-010 → FRM-011