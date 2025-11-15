# Project Vocabulary Dictionary

This document defines key terms used within the AI Lab Framework project to ensure consistent understanding and communication.

## Core Concepts

*   **Agent:** An autonomous or semi-autonomous software entity designed to perform specific tasks or manage other components within the Homelab Orchestrator. Agents can be of various types (e.g., workflow, service, monitor, AI).
*   **Agent OS:** A framework for building AI-powered agents that can understand, plan, and execute tasks, often used for structured, spec-driven development.
*   **CLI Workflows:** Standardized command-line interface procedures and sequences of operations for various tasks, guiding users through common interactions with the framework.
*   **Context:** Environmental or operational information relevant to the execution of an agent or tool. This includes configuration, state, and other data necessary for proper functioning.
*   **Documentation:** Written materials that explain the project's design, functionality, usage, and maintenance.
*   **E2E Tests (End-to-End Tests):** A type of software testing that verifies an application's entire workflow from start to finish, simulating real user scenarios.
*   **Error Handling:** Mechanisms and strategies implemented to detect, respond to, and recover from errors or unexpected conditions during program execution.
*   **GitHub PAT (Personal Access Token):** A secure alternative to using a password for authentication to GitHub when using the GitHub API or command line.
*   **GitHub Projects:** A project management tool within GitHub that allows users to organize and track work using boards, tables, and timelines, often integrated with issues and pull requests.
*   **Homelab:** A personal laboratory environment set up at home for learning, experimentation, and self-hosting various services and applications.
*   **Idea:** An initial concept or proposal for a feature, improvement, or research area within the framework. Ideas are often refined and converted into work items.
*   **Logging:** The process of recording events, operations and status information for monitoring, debugging, and auditing purposes. The framework uses structured logging (`structlog`).
*   **MCP (Model Context Protocol):** A protocol or architecture for managing context and communication between different models or agents, especially in distributed AI systems.
*   **Playwright:** A Node.js library to automate Chromium, Firefox and WebKit with a single API. Used for End-to-End (E2E) testing.
*   **Profile:** A three-tier system (`Experimental`, `Standard`, `Production`) that defines requirements for logging, context management, error handling, testing, documentation, and validation, adapting to different development stages and criticality levels.
*   **Project:** A high-level organizational unit representing a significant development effort or a collection of related work items and ideas.
*   **Service:** A distinct functional unit that provides a specific capability (e.g., SystemService for OS interactions, DockerService for container management, ProxmoxService for virtualization, AdGuardService for DNS filtering). Services are typically managed by agents.
*   **Testing:** The process of evaluating software to verify that it meets specified requirements and to identify defects. Includes unit, integration, and end-to-end tests.
*   **Tool:** A specific utility or module designed to perform a specialized function, often integrated into agents or CLI workflows. Examples include `project-creator` or `fritzbox` integration.
*   **TR-064 API:** A technical specification used by AVM FRITZ!Box routers (and other devices) to allow remote control and configuration of various functions over the local network.
*   **Validation:** The process of ensuring that data, inputs, or system states conform to predefined rules, standards, or expectations.
*   **Work Item:** A discrete, actionable task or feature that contributes to a project. Work items are tracked and managed through their lifecycle (e.g., new, in progress, completed).

## Related Terms

*   **Agent Manager:** The central component responsible for registering, monitoring, and orchestrating agents.
*   **Agent Registry:** A component within the Agent Manager that maintains a record of all registered agents and their current status.
*   **FastAPI:** The web framework used for building the REST API endpoints in the Homelab Orchestrator.
*   **Homelab Orchestrator:** The overarching system that manages and automates various services and devices within a home lab environment, utilizing agents and services from this framework.
*   **n8n:** A workflow automation tool that helps to connect apps and services with a visual workflow editor.
*   **Poetry:** The dependency management and packaging tool used for this Python project.
*   **Pydantic:** A data validation and settings management library used for defining data models and ensuring data integrity.
*   **Structured Logging:** A logging approach where log messages are formatted as machine-readable data (e.g., JSON) to facilitate easier parsing, searching, and analysis.
