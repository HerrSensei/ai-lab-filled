"""
Gemini-CLI Integration Service
Integrates local gemini-cli/opencode with the Agent OS framework
"""

import asyncio
import json
import logging
import subprocess
import tempfile
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import uuid

from ..core.agent_manager import Agent, AgentType, AgentStatus


@dataclass
class GeminiTask:
    id: str
    agent_id: str
    task_type: str
    prompt: str
    context: Dict[str, Any]
    created_at: datetime
    status: str
    result: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None


class GeminiIntegrationService:
    """Service for integrating with gemini-cli/opencode"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.gemini_cli_path = self._find_gemini_cli()
        self.active_tasks: Dict[str, GeminiTask] = {}
        self.task_queue = asyncio.Queue()
        self.worker_task = None

    def _find_gemini_cli(self) -> Optional[str]:
        """Find gemini-cli executable"""
        # Check common locations
        possible_paths = [
            "gemini",
            "gemini-cli",
            "/usr/local/bin/gemini",
            "/opt/homebrew/bin/gemini",
            os.path.expanduser("~/.local/bin/gemini"),
        ]

        for path in possible_paths:
            try:
                result = subprocess.run(
                    [path, "--version"], capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    self.logger.info(f"Found gemini-cli at: {path}")
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

        self.logger.warning("gemini-cli not found. Using mock implementation.")
        return None

    async def start_worker(self):
        """Start the background task worker"""
        if self.worker_task is None:
            self.worker_task = asyncio.create_task(self._task_worker())
            self.logger.info("Gemini task worker started")

    async def stop_worker(self):
        """Stop the background task worker"""
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass
            self.worker_task = None
            self.logger.info("Gemini task worker stopped")

    async def submit_task(
        self, agent_id: str, task_type: str, prompt: str, context: Dict[str, Any] = None
    ) -> str:
        """Submit a task to gemini-cli"""
        task_id = str(uuid.uuid4())

        task = GeminiTask(
            id=task_id,
            agent_id=agent_id,
            task_type=task_type,
            prompt=prompt,
            context=context or {},
            created_at=datetime.now(),
            status="queued",
        )

        self.active_tasks[task_id] = task
        await self.task_queue.put(task)

        self.logger.info(f"Submitted task {task_id} for agent {agent_id}")
        return task_id

    async def get_task_result(self, task_id: str) -> Optional[GeminiTask]:
        """Get task result"""
        return self.active_tasks.get(task_id)

    async def _task_worker(self):
        """Background worker to process tasks"""
        while True:
            try:
                task = await self.task_queue.get()
                await self._execute_task(task)
                self.task_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Task worker error: {e}")

    async def _execute_task(self, task: GeminiTask):
        """Execute a single task"""
        start_time = datetime.now()
        task.status = "running"

        try:
            if self.gemini_cli_path:
                result = await self._execute_gemini_cli(task)
            else:
                result = await self._execute_mock(task)

            task.result = result
            task.status = "completed"

        except Exception as e:
            task.error = str(e)
            task.status = "failed"
            self.logger.error(f"Task {task.id} failed: {e}")

        # Calculate execution time
        end_time = datetime.now()
        task.execution_time = (end_time - start_time).total_seconds()

    async def _execute_gemini_cli(self, task: GeminiTask) -> str:
        """Execute task using real gemini-cli"""
        # Prepare prompt with context
        full_prompt = self._prepare_prompt(task)

        # Write prompt to temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(full_prompt)
            prompt_file = f.name

        try:
            # Execute gemini-cli
            cmd = [self.gemini_cli_path, "prompt", "--file", prompt_file]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                text=True,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise Exception(f"gemini-cli error: {stderr}")

            return stdout.strip()

        finally:
            # Clean up temporary file
            os.unlink(prompt_file)

    async def _execute_mock(self, task: GeminiTask) -> str:
        """Execute task with mock implementation"""
        # Simulate processing time
        await asyncio.sleep(1)

        # Generate mock response based on task type
        if task.task_type == "code_generation":
            return f"""# Generated Code for {task.prompt[:50]}...

```python
def generated_function():
    # Mock implementation
    return "Hello from Gemini!"
```

This code was generated based on your request."""

        elif task.task_type == "analysis":
            return f"""# Analysis Result

Based on the input: "{task.prompt[:100]}..."

## Key Points:
- Point 1: Analysis complete
- Point 2: Consider these factors
- Point 3: Recommended next steps

## Conclusion:
Mock analysis completed successfully."""

        elif task.task_type == "troubleshooting":
            return f"""# Troubleshooting Guide

## Issue: {task.prompt[:50]}...

## Possible Solutions:
1. Check configuration files
2. Verify service status
3. Review logs for errors

## Steps to Resolve:
1. Step one description
2. Step two description
3. Step three description

Mock troubleshooting advice provided."""

        else:
            return f"Mock response for task type '{task.task_type}' with prompt: {task.prompt[:100]}..."

    def _prepare_prompt(self, task: GeminiTask) -> str:
        """Prepare full prompt with context"""
        prompt_parts = [
            f"Task Type: {task.task_type}",
            f"Agent ID: {task.agent_id}",
            "",
            "Context:",
        ]

        # Add context information
        if task.context:
            for key, value in task.context.items():
                prompt_parts.append(f"- {key}: {value}")

        prompt_parts.extend(
            [
                "",
                "Task:",
                task.prompt,
                "",
                "Please provide a helpful response based on the task and context above.",
            ]
        )

        return "\n".join(prompt_parts)

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        queued_tasks = sum(
            1 for t in self.active_tasks.values() if t.status == "queued"
        )
        running_tasks = sum(
            1 for t in self.active_tasks.values() if t.status == "running"
        )
        completed_tasks = sum(
            1 for t in self.active_tasks.values() if t.status == "completed"
        )
        failed_tasks = sum(
            1 for t in self.active_tasks.values() if t.status == "failed"
        )

        return {
            "queue_size": self.task_queue.qsize(),
            "active_tasks": len(self.active_tasks),
            "by_status": {
                "queued": queued_tasks,
                "running": running_tasks,
                "completed": completed_tasks,
                "failed": failed_tasks,
            },
        }


class GeminiAgent(Agent):
    """Specialized agent for Gemini AI integration"""

    def __init__(self, gemini_service: GeminiIntegrationService, **kwargs):
        super().__init__(**kwargs)
        self.gemini_service = gemini_service
        self.supported_task_types = [
            "code_generation",
            "analysis",
            "troubleshooting",
            "planning",
            "review",
        ]

    async def process_task(
        self, task_type: str, prompt: str, context: Dict[str, Any] = None
    ) -> str:
        """Process a task using Gemini"""
        if task_type not in self.supported_task_types:
            raise ValueError(f"Unsupported task type: {task_type}")

        task_id = await self.gemini_service.submit_task(
            self.id, task_type, prompt, context
        )

        # Wait for completion (with timeout)
        timeout = 300  # 5 minutes
        start_time = datetime.now()

        while True:
            task = await self.gemini_service.get_task_result(task_id)

            if task.status in ["completed", "failed"]:
                break

            # Check timeout
            if (datetime.now() - start_time).total_seconds() > timeout:
                raise TimeoutError(f"Task {task_id} timed out")

            await asyncio.sleep(1)

        if task.status == "failed":
            raise Exception(f"Task failed: {task.error}")

        return task.result


# Global service instance
gemini_service = GeminiIntegrationService()
