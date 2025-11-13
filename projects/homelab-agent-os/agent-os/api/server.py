"""
Homelab Agent OS Framework - API Server
REST API for managing agents and services
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import logging

from ..core.agent_manager import agent_manager, Agent, AgentType, AgentStatus


# Pydantic models for API
class AgentConfig(BaseModel):
    heartbeat_interval: int = Field(
        default=30, description="Heartbeat interval in seconds"
    )
    check_interval: int = Field(default=60, description="Check interval in seconds")
    service_config: Optional[Dict[str, Any]] = Field(
        default=None, description="Service-specific configuration"
    )


class AgentCreateRequest(BaseModel):
    name: str = Field(..., description="Agent name")
    type: str = Field(..., description="Agent type (workflow, service, monitor, ai)")
    config: AgentConfig = Field(..., description="Agent configuration")


class AgentResponse(BaseModel):
    id: str
    name: str
    type: str
    status: str
    config: Dict[str, Any]
    created_at: str
    updated_at: str
    last_heartbeat: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentUpdateRequest(BaseModel):
    status: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class SystemStatsResponse(BaseModel):
    total_agents: int
    by_type: Dict[str, int]
    by_status: Dict[str, int]


# Initialize FastAPI app
app = FastAPI(
    title="Homelab Agent OS API",
    description="REST API for managing homelab agents and services",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)


def agent_to_response(agent: Agent) -> AgentResponse:
    """Convert Agent to AgentResponse"""
    return AgentResponse(
        id=agent.id,
        name=agent.name,
        type=agent.type.value,
        status=agent.status.value,
        config=agent.config,
        created_at=agent.created_at.isoformat(),
        updated_at=agent.updated_at.isoformat(),
        last_heartbeat=agent.last_heartbeat.isoformat()
        if agent.last_heartbeat
        else None,
        metadata=agent.metadata,
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Homelab Agent OS API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": len(agent_manager.registry.agents),
    }


@app.post("/agents", response_model=AgentResponse)
async def create_agent(request: AgentCreateRequest, background_tasks: BackgroundTasks):
    """Create a new agent"""
    try:
        # Convert string type to enum
        agent_type = AgentType(request.type.lower())

        # Create agent
        agent = await agent_manager.create_agent(
            name=request.name, agent_type=agent_type, config=request.config.dict()
        )

        logger.info(f"Created agent: {agent.name} ({agent.id})")
        return agent_to_response(agent)

    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid agent type: {request.type}"
        )
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents", response_model=List[AgentResponse])
async def list_agents():
    """List all agents"""
    agents = agent_manager.registry.list_agents()
    return [agent_to_response(agent) for agent in agents]


@app.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get agent by ID"""
    agent = agent_manager.registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent_to_response(agent)


@app.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, request: AgentUpdateRequest):
    """Update agent"""
    agent = agent_manager.registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        # Update agent fields
        if request.status:
            agent.status = AgentStatus(request.status.lower())

        if request.config:
            agent.config.update(request.config)

        if request.metadata:
            agent.metadata = request.metadata

        agent.updated_at = datetime.now()

        logger.info(f"Updated agent: {agent.name} ({agent_id})")
        return agent_to_response(agent)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid status: {request.status}")
    except Exception as e:
        logger.error(f"Error updating agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete agent"""
    # Stop agent first
    await agent_manager.stop_agent(agent_id)

    # Unregister agent
    success = agent_manager.registry.unregister_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")

    logger.info(f"Deleted agent: {agent_id}")
    return {"message": "Agent deleted successfully"}


@app.post("/agents/{agent_id}/stop")
async def stop_agent(agent_id: str):
    """Stop an agent"""
    success = await agent_manager.stop_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")

    logger.info(f"Stopped agent: {agent_id}")
    return {"message": "Agent stopped successfully"}


@app.get("/agents/type/{agent_type}", response_model=List[AgentResponse])
async def get_agents_by_type(agent_type: str):
    """Get agents by type"""
    try:
        type_enum = AgentType(agent_type.lower())
        agents = agent_manager.registry.get_agents_by_type(type_enum)
        return [agent_to_response(agent) for agent in agents]
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid agent type: {agent_type}")


@app.get("/agents/status/{status}", response_model=List[AgentResponse])
async def get_agents_by_status(status: str):
    """Get agents by status"""
    try:
        status_enum = AgentStatus(status.lower())
        agents = agent_manager.registry.get_agents_by_status(status_enum)
        return [agent_to_response(agent) for agent in agents]
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")


@app.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats():
    """Get system statistics"""
    stats = agent_manager.registry.get_stats()
    return SystemStatsResponse(**stats)


@app.get("/services")
async def get_services():
    """Get available services"""
    return {
        "services": [
            {
                "name": "n8n",
                "status": "running",
                "url": "http://localhost:5678",
                "description": "Workflow automation platform",
            },
            {
                "name": "gemini-cli",
                "status": "available",
                "description": "Local AI assistant via opencode",
            },
            {
                "name": "agent-os",
                "status": "running",
                "url": "http://localhost:8080",
                "description": "Agent management system",
            },
        ]
    }


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8080)
