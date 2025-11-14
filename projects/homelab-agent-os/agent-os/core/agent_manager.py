"""
Homelab Agent OS Framework - Core Module
Provides the foundational agent management system
"""

import asyncio
import logging
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class AgentStatus(Enum):
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


class AgentType(Enum):
    WORKFLOW = "workflow"
    SERVICE = "service"
    MONITOR = "monitor"
    AI = "ai"


@dataclass
class Agent:
    id: str
    name: str
    type: AgentType
    status: AgentStatus
    config: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    last_heartbeat: datetime | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["type"] = self.type.value
        data["status"] = self.status.value
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        if self.last_heartbeat:
            data["last_heartbeat"] = self.last_heartbeat.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Agent":
        data["type"] = AgentType(data["type"])
        data["status"] = AgentStatus(data["status"])
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if data.get("last_heartbeat"):
            data["last_heartbeat"] = datetime.fromisoformat(data["last_heartbeat"])
        return cls(**data)


class AgentRegistry:
    """Central registry for managing agents"""

    def __init__(self):
        self.agents: dict[str, Agent] = {}
        self.logger = logging.getLogger(__name__)

    def register_agent(self, agent: Agent) -> bool:
        """Register a new agent"""
        if agent.id in self.agents:
            self.logger.warning(f"Agent {agent.id} already exists, updating...")

        self.agents[agent.id] = agent
        self.logger.info(f"Registered agent: {agent.name} ({agent.id})")
        return True

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent"""
        if agent_id not in self.agents:
            self.logger.warning(f"Agent {agent_id} not found")
            return False

        agent_name = self.agents[agent_id].name
        del self.agents[agent_id]
        self.logger.info(f"Unregistered agent: {agent_name} ({agent_id})")
        return True

    def get_agent(self, agent_id: str) -> Agent | None:
        """Get agent by ID"""
        return self.agents.get(agent_id)

    def get_agents_by_type(self, agent_type: AgentType) -> list[Agent]:
        """Get all agents of a specific type"""
        return [agent for agent in self.agents.values() if agent.type == agent_type]

    def get_agents_by_status(self, status: AgentStatus) -> list[Agent]:
        """Get all agents with a specific status"""
        return [agent for agent in self.agents.values() if agent.status == status]

    def update_agent_status(
        self, agent_id: str, status: AgentStatus, heartbeat: datetime | None = None
    ) -> bool:
        """Update agent status and optionally heartbeat"""
        if agent_id not in self.agents:
            self.logger.warning(f"Agent {agent_id} not found")
            return False

        agent = self.agents[agent_id]
        agent.status = status
        agent.updated_at = datetime.now()

        if heartbeat:
            agent.last_heartbeat = heartbeat

        self.logger.info(f"Updated agent {agent.name} status to {status.value}")
        return True

    def list_agents(self) -> list[Agent]:
        """List all registered agents"""
        return list(self.agents.values())

    def get_stats(self) -> dict[str, Any]:
        """Get registry statistics"""
        stats = {"total_agents": len(self.agents), "by_type": {}, "by_status": {}}

        for agent in self.agents.values():
            # Count by type
            type_name = agent.type.value
            stats["by_type"][type_name] = stats["by_type"].get(type_name, 0) + 1

            # Count by status
            status_name = agent.status.value
            stats["by_status"][status_name] = stats["by_status"].get(status_name, 0) + 1

        return stats


class AgentManager:
    """High-level agent management interface"""

    def __init__(self):
        self.registry = AgentRegistry()
        self.running_tasks: dict[str, asyncio.Task] = {}
        self.logger = logging.getLogger(__name__)

    async def create_agent(
        self, name: str, agent_type: AgentType, config: dict[str, Any]
    ) -> Agent:
        """Create and register a new agent"""
        agent_id = str(uuid.uuid4())
        now = datetime.now()

        agent = Agent(
            id=agent_id,
            name=name,
            type=agent_type,
            status=AgentStatus.STARTING,
            config=config,
            created_at=now,
            updated_at=now,
            metadata={},
        )

        self.registry.register_agent(agent)

        # Start agent based on type
        if agent_type == AgentType.SERVICE:
            task = asyncio.create_task(self._run_service_agent(agent))
            self.running_tasks[agent_id] = task
        elif agent_type == AgentType.MONITOR:
            task = asyncio.create_task(self._run_monitor_agent(agent))
            self.running_tasks[agent_id] = task

        return agent

    async def stop_agent(self, agent_id: str) -> bool:
        """Stop an agent"""
        if agent_id not in self.registry.agents:
            return False

        # Update status
        self.registry.update_agent_status(agent_id, AgentStatus.STOPPING)

        # Cancel running task
        if agent_id in self.running_tasks:
            self.running_tasks[agent_id].cancel()
            del self.running_tasks[agent_id]

        # Update status
        self.registry.update_agent_status(agent_id, AgentStatus.STOPPED)
        return True

    async def _run_service_agent(self, agent: Agent):
        """Run a service agent"""
        self.logger.info(f"Starting service agent: {agent.name}")

        try:
            self.registry.update_agent_status(agent.id, AgentStatus.RUNNING)

            # Service agent main loop
            while True:
                # Update heartbeat
                self.registry.update_agent_status(
                    agent.id, AgentStatus.RUNNING, datetime.now()
                )

                # Service-specific logic here
                await asyncio.sleep(agent.config.get("heartbeat_interval", 30))

        except asyncio.CancelledError:
            self.logger.info(f"Service agent {agent.name} cancelled")
        except Exception as e:
            self.logger.error(f"Service agent {agent.name} error: {e}")
            self.registry.update_agent_status(agent.id, AgentStatus.ERROR)

    async def _run_monitor_agent(self, agent: Agent):
        """Run a monitor agent"""
        self.logger.info(f"Starting monitor agent: {agent.name}")

        try:
            self.registry.update_agent_status(agent.id, AgentStatus.RUNNING)

            # Monitor agent main loop
            while True:
                # Update heartbeat
                self.registry.update_agent_status(
                    agent.id, AgentStatus.RUNNING, datetime.now()
                )

                # Monitoring logic here
                await self._perform_monitoring_checks(agent)

                await asyncio.sleep(agent.config.get("check_interval", 60))

        except asyncio.CancelledError:
            self.logger.info(f"Monitor agent {agent.name} cancelled")
        except Exception as e:
            self.logger.error(f"Monitor agent {agent.name} error: {e}")
            self.registry.update_agent_status(agent.id, AgentStatus.ERROR)

    async def _perform_monitoring_checks(self, agent: Agent):
        """Perform monitoring checks"""
        # Implementation depends on what we're monitoring
        # For now, just log
        self.logger.debug(f"Monitor agent {agent.name} performing checks")


# Global instance
agent_manager = AgentManager()
