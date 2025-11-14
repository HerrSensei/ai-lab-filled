# 🧪 AI Lab Framework E2E Tests

<div align="center">

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

*Comprehensive End-to-End (E2E) tests for critical user flows within the AI Lab Framework, powered by Playwright.*

</div>

---

## 📖 Table of Contents

*   [✨ Overview](#-overview)
*   [🚀 Features](#-features)
*   [⬇️ Installation](#️-installation)
*   [▶️ Running Tests](#️-running-tests)
*   [🤝 Contributing](#-contributing)
*   [📄 License](#-license)
*   [❓ Support](#-support)

---

## ✨ Overview

This directory houses the End-to-End (E2E) test suite for the AI Lab Framework. These tests are designed to simulate real user interactions and validate critical workflows across the entire application stack. By leveraging Playwright, we ensure that key functionalities, from UI interactions to backend integrations, are working seamlessly.

---

## 🚀 Features

*   **🌐 Browser Automation**: Utilizes Playwright for robust and reliable browser automation across Chromium, Firefox, and WebKit.
*   **✅ Critical Flow Validation**: Focuses on testing essential user journeys and application functionalities.
*   **📊 Comprehensive Reporting**: Integrates with Pytest for detailed test results and reporting.
*   **⚙️ Flexible Execution**: Supports various test execution modes, including headless, headed, and trace recording.
*   **🔄 CI/CD Integration**: Designed to be easily integrated into continuous integration and continuous deployment pipelines.

---

## ⬇️ Installation

To set up and run the E2E tests, follow these steps:

1.  **Install `pytest-playwright`**: This Pytest plugin provides the necessary Playwright integration.
    ```bash
    pip install pytest-playwright
    ```
2.  **Install Playwright browsers**: Download the browser binaries required by Playwright.
    ```bash
    playwright install
    ```
    *(Note: This command installs Chromium, Firefox, and WebKit browsers.)*

---

## ▶️ Running Tests

Execute the E2E test suite using `pytest` with various options:

*   **Run all E2E tests**:
    ```bash
    pytest tests/e2e/
    ```
*   **Run a specific test file**:
    ```bash
    pytest tests/e2e/test_dashboard.py
    ```
*   **Run tests with a visible browser (headed mode)**:
    ```bash
    pytest tests/e2e/ --headed
    ```
    *(Useful for debugging and visualizing test execution.)*
*   **Record a trace of test execution**:
    ```bash
    pytest tests/e2e/ --tracing retain-on-failure
    ```
    *(Generates a detailed trace file that can be opened with `playwright show-trace` for post-mortem debugging.)*

---

## 🤝 Contributing

We welcome contributions to the E2E test suite! Please refer to the main [Contributing Guidelines](core/guidelines/AGENTS.md) for the AI Lab Framework.

---

## 📄 License

This project is part of the AI Lab Framework and is licensed under the MIT License. See the main [LICENSE](README.md) file for details.

---

## ❓ Support

For issues, feature requests, or general support, please refer to the main [AI Lab Framework Documentation](README.md).