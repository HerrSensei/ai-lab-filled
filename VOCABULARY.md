# Project Vocabulary Dictionary

This document defines key terms used within the AI Lab Framework project to ensure consistent understanding and communication.

## Core Concepts

*   **Agent:** An autonomous or semi-autonomous software entity designed to perform specific tasks or manage other components within the Homelab Orchestrator. Agents can be of various types (e.g., workflow, service, monitor, AI).
*   **Service:** A distinct functional unit that provides a specific capability (e.g., SystemService for OS interactions, DockerService for container management, ProxmoxService for virtualization, AdGuardService for DNS filtering). Services are typically managed by agents.
*   **Tool:** A specific utility or module designed to perform a specialized function, often integrated into agents or CLI workflows. Examples include `project-creator` or `fritzbox` integration.
*   **Project:** A high-level organizational unit representing a significant development effort or a collection of related work items and ideas.
*   **Idea:** An initial concept or proposal for a feature, improvement, or research area within the framework. Ideas are often refined and converted into work items.
*   **Work Item:** A discrete, actionable task or feature that contributes to a project. Work items are tracked and managed through their lifecycle (e.g., new, in progress, completed).
*   **Profile:** A three-tier system (`Experimental`, `Standard`, `Production`) that defines requirements for logging, context management, error handling, testing, documentation, and validation, adapting to different development stages and criticality levels.
*   **Context:** Environmental or operational information relevant to the execution of an agent or tool. This includes configuration, state, and other data necessary for proper functioning.
*   **Logging:** The process of recording events, operations, and status information for monitoring, debugging, and auditing purposes. The framework uses structured logging (`structlog`).
*   **Error Handling:** Mechanisms and strategies implemented to detect, respond to, and recover from errors or unexpected conditions during program execution.
*   **Testing:** The process of evaluating software to verify that it meets specified requirements and to identify defects. Includes unit, integration, and end-to-end tests.
*   **Documentation:** Written materials that explain the project's design, functionality, usage, and maintenance.
*   **Validation:** The process of ensuring that data, inputs, or system states conform to predefined rules, standards, or expectations.
*   **CLI Workflows:** Standardized command-line interface procedures and sequences of operations for various tasks, guiding users through common interactions with the framework.

## Related Terms

*   **Agent Manager:** The central component responsible for registering, monitoring, and orchestrating agents.
*   **Agent Registry:** A component within the Agent Manager that maintains a record of all registered agents and their current status.
*   **Homelab Orchestrator:** The overarching system that manages and automates various services and devices within a home lab environment, utilizing agents and services from this framework.
*   **Structured Logging:** A logging approach where log messages are formatted as machine-readable data (e.g., JSON) to facilitate easier parsing, searching, and analysis.
*   **Poetry:** The dependency management and packaging tool used for this Python project.
*   **FastAPI:** The web framework used for building the REST API endpoints in the Homelab Orchestrator.
*   **Pydantic:** A data validation and settings management library used for defining data models and ensuring data integrity.
