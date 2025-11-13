"""
n8n Custom Node for Agent OS Integration
Provides n8n nodes to interact with the Homelab Agent OS framework
"""

from n8n_nodes_base.node import Node
from n8n_nodes_base.fields import (
    TextField,
    DropdownField,
    NumberField,
    BooleanField,
    TextAreaField,
    MultiSelectField,
)
import requests
import json
from typing import Dict, Any, List


class AgentOSNode(Node):
    """Base class for Agent OS nodes"""

    def __init__(self):
        super().__init__()
        self.base_url = "http://localhost:8080"

    def _make_request(
        self, method: str, endpoint: str, data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Agent OS API"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Agent OS API request failed: {str(e)}")


class CreateAgentNode(AgentOSNode):
    """Node to create new agents"""

    display_name = "Agent OS - Create Agent"
    description = "Create a new agent in the Homelab Agent OS framework"

    fields = [
        TextField("name", "Agent Name", required=True),
        DropdownField(
            "type",
            "Agent Type",
            required=True,
            options=[
                {"value": "workflow", "label": "Workflow Agent"},
                {"value": "service", "label": "Service Agent"},
                {"value": "monitor", "label": "Monitor Agent"},
                {"value": "ai", "label": "AI Agent"},
            ],
        ),
        NumberField("heartbeat_interval", "Heartbeat Interval (seconds)", default=30),
        NumberField("check_interval", "Check Interval (seconds)", default=60),
        TextAreaField("service_config", "Service Configuration (JSON)", optional=True),
    ]

    def execute(self) -> List[Dict[str, Any]]:
        agent_name = self.get_field_value("name")
        agent_type = self.get_field_value("type")
        heartbeat_interval = self.get_field_value("heartbeat_interval")
        check_interval = self.get_field_value("check_interval")
        service_config_str = self.get_field_value("service_config")

        # Parse service config if provided
        service_config = {}
        if service_config_str:
            try:
                service_config = json.loads(service_config_str)
            except json.JSONDecodeError:
                raise Exception("Invalid JSON in service configuration")

        # Prepare request data
        request_data = {
            "name": agent_name,
            "type": agent_type,
            "config": {
                "heartbeat_interval": heartbeat_interval,
                "check_interval": check_interval,
                "service_config": service_config,
            },
        }

        # Create agent
        response = self._make_request("POST", "/agents", request_data)

        return [
            {
                "agent_id": response["id"],
                "agent_name": response["name"],
                "agent_type": response["type"],
                "agent_status": response["status"],
                "created_at": response["created_at"],
            }
        ]


class ListAgentsNode(AgentOSNode):
    """Node to list all agents"""

    display_name = "Agent OS - List Agents"
    description = "List all agents in the Homelab Agent OS framework"

    fields = [
        DropdownField(
            "filter_type",
            "Filter by Type",
            optional=True,
            options=[
                {"value": "", "label": "All Types"},
                {"value": "workflow", "label": "Workflow Agents"},
                {"value": "service", "label": "Service Agents"},
                {"value": "monitor", "label": "Monitor Agents"},
                {"value": "ai", "label": "AI Agents"},
            ],
        ),
        DropdownField(
            "filter_status",
            "Filter by Status",
            optional=True,
            options=[
                {"value": "", "label": "All Statuses"},
                {"value": "starting", "label": "Starting"},
                {"value": "running", "label": "Running"},
                {"value": "stopping", "label": "Stopping"},
                {"value": "stopped", "label": "Stopped"},
                {"value": "error", "label": "Error"},
            ],
        ),
    ]

    def execute(self) -> List[Dict[str, Any]]:
        filter_type = self.get_field_value("filter_type")
        filter_status = self.get_field_value("filter_status")

        # Determine endpoint
        if filter_type:
            endpoint = f"/agents/type/{filter_type}"
        elif filter_status:
            endpoint = f"/agents/status/{filter_status}"
        else:
            endpoint = "/agents"

        # Get agents
        agents = self._make_request("GET", endpoint)

        return [
            {
                "agents": agents,
                "count": len(agents),
                "filter_type": filter_type,
                "filter_status": filter_status,
            }
        ]


class StopAgentNode(AgentOSNode):
    """Node to stop an agent"""

    display_name = "Agent OS - Stop Agent"
    description = "Stop a running agent"

    fields = [TextField("agent_id", "Agent ID", required=True)]

    def execute(self) -> List[Dict[str, Any]]:
        agent_id = self.get_field_value("agent_id")

        # Stop agent
        response = self._make_request("POST", f"/agents/{agent_id}/stop")

        return [
            {
                "agent_id": agent_id,
                "message": response["message"],
                "timestamp": response.get("timestamp"),
            }
        ]


class GetSystemStatsNode(AgentOSNode):
    """Node to get system statistics"""

    display_name = "Agent OS - System Stats"
    description = "Get system statistics from the Agent OS framework"

    fields = []

    def execute(self) -> List[Dict[str, Any]]:
        # Get system stats
        stats = self._make_request("GET", "/stats")

        return [
            {
                "total_agents": stats["total_agents"],
                "agents_by_type": stats["by_type"],
                "agents_by_status": stats["by_status"],
                "timestamp": stats.get("timestamp"),
            }
        ]


class AIAgentNode(AgentOSNode):
    """Node to interact with AI agents"""

    display_name = "Agent OS - AI Agent"
    description = "Send tasks to AI agents and get responses"

    fields = [
        TextField(
            "agent_id",
            "Agent ID",
            optional=True,
            description="Leave empty to use any available AI agent",
        ),
        TextAreaField("task", "Task Description", required=True),
        DropdownField(
            "priority",
            "Priority",
            default="medium",
            options=[
                {"value": "low", "label": "Low"},
                {"value": "medium", "label": "Medium"},
                {"value": "high", "label": "High"},
            ],
        ),
        BooleanField("wait_for_completion", "Wait for Completion", default=True),
        NumberField("timeout", "Timeout (seconds)", default=300),
    ]

    def execute(self) -> List[Dict[str, Any]]:
        agent_id = self.get_field_value("agent_id")
        task = self.get_field_value("task")
        priority = self.get_field_value("priority")
        wait_for_completion = self.get_field_value("wait_for_completion")
        timeout = self.get_field_value("timeout")

        # If no specific agent ID, find an available AI agent
        if not agent_id:
            ai_agents = self._make_request("GET", "/agents/type/ai")
            running_agents = [
                agent for agent in ai_agents if agent["status"] == "running"
            ]

            if not running_agents:
                raise Exception("No running AI agents available")

            agent_id = running_agents[0]["id"]

        # Send task to AI agent
        task_data = {
            "task": task,
            "priority": priority,
            "wait_for_completion": wait_for_completion,
            "timeout": timeout,
        }

        response = self._make_request("POST", f"/agents/{agent_id}/task", task_data)

        return [
            {
                "agent_id": agent_id,
                "task_id": response.get("task_id"),
                "result": response.get("result"),
                "status": response.get("status"),
                "execution_time": response.get("execution_time"),
            }
        ]


# Node registration
def register_nodes():
    """Register all Agent OS nodes with n8n"""
    return [
        CreateAgentNode,
        ListAgentsNode,
        StopAgentNode,
        GetSystemStatsNode,
        AIAgentNode,
    ]
