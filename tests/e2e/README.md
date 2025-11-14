# AI Lab Framework E2E Tests

End-to-end tests for critical user flows using Playwright.

## Installation

```bash
pip install pytest-playwright
playwright install
```

## Running Tests

```bash
# Run all E2E tests
pytest tests/e2e/

# Run specific test
pytest tests/e2e/test_dashboard.py

# Run with headed browser
pytest tests/e2e/ --headed

# Run with trace
pytest tests/e2e/ --tracing retain-on-failure
```