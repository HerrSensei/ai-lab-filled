# Analysis Workflow Template

This document outlines the standard workflow for conducting analyses that result in actionable work items. This process ensures that analyses are thorough, well-documented, and lead to clear, actionable plans.

## 1. Define the High-Level Analysis Task

- **Objective:** Clearly state the goal of the analysis.
- **Work Item:** Create a high-level work item (e.g., `FRM-XXX-1: Analyze [Topic]`) in the project management system.
- **Status:** Set the status to `in_progress`.

## 2. Decompose into Granular Sub-Tasks

- **Action:** Break down the high-level analysis into smaller, manageable sub-tasks. Each sub-task should focus on a specific area or aspect of the analysis.
- **Example:**
    - `FRM-XXX-1.1: Analyze [Area A]`
    - `FRM-XXX-1.2: Analyze [Area B]`
    - `FRM-XXX-1.3: Analyze [Area C]`
    - `FRM-XXX-1.4: Create Consolidation/Action Plan`
- **Work Item:** Document these sub-tasks within the parent work item.

## 3. Execute Each Analysis Sub-Task

For each granular sub-task (e.g., `FRM-XXX-1.1`):

### 3.1. Identify Scope
- **Action:** Clearly define the scope of the sub-task (e.g., list the specific files, directories, or components to be analyzed).

### 3.2. Perform Analysis
- **Action:** Conduct the analysis, focusing on the objectives of the sub-task.

### 3.3. Document Detailed Findings
- **Action:** Create a dedicated markdown file for the detailed findings.
- **Location:** `core/docs/analysis/FRM-XXX-1.1_[sub-task-name]_analysis.md`
- **Content:** The file should contain the full, detailed results of the analysis.

### 3.4. Update Work Item
- **Action:** Update the sub-task in the project management system:
    - Set the status to `done`.
    - Add a concise summary of the findings to the `notes` section of the parent work item (`FRM-XXX-1`).

## 4. Synthesize Findings and Create a Plan

- **Action:** Once all analysis sub-tasks are complete, create a final "Strategy" or "Plan" document.
- **Location:** `core/docs/analysis/FRM-XXX-1.X_[plan-name].md`
- **Content:** This document should synthesize the findings from all the individual analysis files and propose a clear, actionable plan. The plan should include concrete steps, such as which files to merge, delete, or update.

## 5. Finalize Analysis Phase

- **Action:** Update the high-level analysis work item (`FRM-XXX-1`):
    - Set the status to `done`.
    - Add a summary of the created plan to the `notes` section.

## 6. Present for Approval

- **Action:** Present the final consolidation strategy or plan to the user or project lead for approval before proceeding with implementation.
- **Implementation:** The implementation of the plan will be handled in subsequent work items (e.g., `FRM-XXX-2`, `FRM-XXX-3`, etc.).
