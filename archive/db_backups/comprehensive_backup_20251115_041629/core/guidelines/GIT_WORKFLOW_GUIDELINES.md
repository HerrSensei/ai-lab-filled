# Git Workflow Guidelines for AI Lab Framework

This document outlines the standardized Git workflow for contributing to the AI Lab Framework. Adhering to these guidelines ensures code quality, stability, and efficient collaboration.

## 1. Branching Strategy

All development, bug fixes, and new features **must** be done on dedicated branches.

*   **Feature Branches:** For new features or significant changes.
    *   Naming convention: `feature/<descriptive-name>` (e.g., `feature/add-new-agent-type`)
*   **Bugfix Branches:** For addressing bugs.
    *   Naming convention: `bugfix/<issue-number>-<descriptive-name>` (e.g., `bugfix/123-fix-login-error`)
*   **Hotfix Branches:** For urgent fixes to production.
    *   Naming convention: `hotfix/<descriptive-name>` (e.g., `hotfix/critical-security-patch`)

**Never commit directly to `main` or `develop` branches.**

## 2. Development Cycle

1.  **Pull Latest Changes:** Always start by pulling the latest changes from the `main` branch to ensure your local `main` is up-to-date.
    ```bash
    git checkout main
    git pull origin main
    ```
2.  **Create a New Branch:** Create a new branch from the `main` branch for your work.
    ```bash
    git checkout -b <your-branch-name>
    ```
3.  **Develop and Commit:** Make your changes, commit frequently with clear, concise commit messages.
    ```bash
    git add .
    git commit -m "feat: Add new feature"
    ```
    (Use `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `style:`, `test:` prefixes for commit messages.)
4.  **Push to Remote:** Regularly push your branch to the remote repository.
    ```bash
    git push origin <your-branch-name>
    ```

## 3. Testing and Quality Assurance

Before merging any changes, a rigorous testing process is mandatory to prevent regressions and ensure stability.

1.  **Run Local Tests:** Execute the entire test suite locally, including unit, integration, and E2E tests (if applicable).
    ```bash
    pytest
    # Or specific test commands as defined in the project's DEVELOPMENT.md or README.md
    ```
2.  **Verify Code Quality:** Ensure all code quality checks pass (linting, formatting, type checking).
    ```bash
    black .
    ruff check --fix .
    mypy .
    ```
3.  **Regression Testing:** The entire framework, tools, and workflows **must** be tested as regression tests to ensure no existing functionality has been broken. This includes:
    *   Running all automated tests (`pytest`).
    *   Manually verifying critical workflows if automated tests don't cover them comprehensively.

## 4. Merging Changes

Merging changes into `main` requires a Pull Request (PR) and approval.

1.  **Create a Pull Request (PR):** Once your work is complete and all local tests pass, push your branch and open a PR to merge into `main`.
2.  **Request Review:** Request reviews from at least one other team member.
3.  **Automated Checks:** Ensure all CI/CD pipeline checks (automated tests, linting, etc.) pass on the PR.
4.  **Address Feedback:** Incorporate feedback from reviewers and push new commits to your branch.
5.  **Merge:** Once approved and all checks pass, the branch can be merged into `main`. **Use 'Squash and Merge' or 'Rebase and Merge' to maintain a clean `main` branch history.**

### Handling Test Failures

*   **If tests fail during development:** Fix the issue on your branch and re-run tests.
*   **If tests fail on the PR (CI/CD):** Investigate the failure, fix the issue on your branch, and push new commits.
*   **If a critical issue is discovered after merging:** Immediately create a `hotfix` branch from `main`, fix the issue, and follow the PR process for hotfixes.

## 5. Review Process for Big Changes / New Features

For significant changes or new features, a personal review by the project owner is required.

1.  **Deployment Report:** Before requesting a personal review, prepare a "Deployment Report" (as defined in `core/guidelines/DEPLOYMENT_REPORT_GUIDELINES.md`). This report should detail:
    *   **What was changed/added:** High-level overview.
    *   **Why it was changed/added:** Problem solved, benefit.
    *   **Impact:** Potential effects on existing systems or users.
    *   **How to test/verify:** Simple steps for the reviewer.
    *   **Rollback plan:** How to revert if issues arise.
2.  **Personal Review:** Share the Deployment Report and the PR with the project owner for a personal review. Do not merge until explicit approval is given.

## 6. Post-Merge Actions

*   **Delete Branch:** After merging, delete the feature/bugfix branch from the remote repository.
    ```bash
    git push origin --delete <your-branch-name>
    ```
*   **Update Local Main:** Pull the latest `main` branch to keep your local repository synchronized.
    ```bash
    git checkout main
    git pull origin main
    ```
