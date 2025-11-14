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
from ..services.system import SystemService
from ..services.docker import DockerService
from ..services.proxmox import ProxmoxService
from ..services.adguard import AdGuardService

from .routes.system import system_router
from .routes.docker import docker_router
from .routes.proxmox import proxmox_router
from .routes.adguard import adguard_router

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

app.include_router(system_router)
app.include_router(docker_router)
app.include_router(proxmox_router)
app.include_router(adguard_router)

@system_router.get("/info", response_model=SystemInfoResponse)
async def get_system_information():
    """Get system information"""
    try:
        return await system_service.get_system_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@system_router.get("/cpu", response_model=CpuUsageResponse)
async def get_cpu_usage_info():
    """Get CPU usage information"""
    try:
        return await system_service.get_cpu_usage()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@system_router.get("/memory", response_model=MemoryUsageResponse)
async def get_memory_usage_info():
    """Get memory usage information"""
    try:
        return await system_service.get_memory_usage()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@system_router.get("/network", response_model=NetworkStatsResponse)
async def get_network_statistics():
    """Get network statistics"""
    try:
        return await system_service.get_network_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@system_router.get("/processes", response_model=List[ProcessInfo])
async def get_process_list_info():
    """Get list of running processes"""
    try:
        return await system_service.get_process_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@system_router.post("/command", response_model=CommandExecuteResponse)
async def execute_system_command(request: CommandExecuteRequest):
    """Execute a system command"""
    try:
        return await system_service.execute_command(request.command, request.timeout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@system_router.get("/service/{service_name}", response_model=ServiceStatusResponse)
async def get_service_status_info(service_name: str):
    """Get status of a system service"""
    try:
        return await system_service.get_service_status(service_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@system_router.post("/service/control", response_model=bool)
async def control_system_service(request: ControlServiceRequest):
    """Control a system service (start, stop, restart, reload)"""
    try:
        return await system_service.control_service(request.service_name, request.action)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@system_router.get("/disk/{path:path}", response_model=DiskUsageResponse)
async def get_disk_usage_info(path: str = "/"):
    """Get disk usage for a specific path"""
    try:
        return await system_service.get_disk_usage(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







@docker_router.get("/containers", response_model=List[ContainerResponse])
async def get_all_containers(all_containers: bool = False):
    """List all Docker containers"""
    try:
        return await docker_service.get_containers(all_containers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.get("/containers/{container_id}", response_model=ContainerInfoResponse)
async def get_single_container_info(container_id: str):
    """Get information about a specific Docker container"""
    try:
        return await docker_service.get_container_info(container_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.get("/containers/{container_id}/logs", response_model=ContainerLogsResponse)
async def get_single_container_logs(container_id: str, lines: int = 100):
    """Get logs for a specific Docker container"""
    try:
        logs = await docker_service.get_container_logs(container_id, lines)
        return ContainerLogsResponse(logs=logs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.get("/containers/{container_id}/stats", response_model=ContainerStatsResponse)
async def get_single_container_stats(container_id: str):
    """Get statistics for a specific Docker container"""
    try:
        return await docker_service.get_container_stats(container_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.post("/containers/{container_id}/start", response_model=bool)
async def start_single_container(container_id: str):
    """Start a Docker container"""
    try:
        return await docker_service.start_container(container_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.post("/containers/{container_id}/stop", response_model=bool)
async def stop_single_container(container_id: str, timeout: int = 10):
    """Stop a Docker container"""
    try:
        return await docker_service.stop_container(container_id, timeout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.post("/containers/{container_id}/restart", response_model=bool)
async def restart_single_container(container_id: str, timeout: int = 10):
    """Restart a Docker container"""
    try:
        return await docker_service.restart_container(container_id, timeout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.delete("/containers/{container_id}", response_model=bool)
async def remove_single_container(container_id: str, force: bool = False):
    """Remove a Docker container"""
    try:
        return await docker_service.remove_container(container_id, force)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.get("/images", response_model=List[ImageResponse])
async def get_all_images():
    """List all Docker images"""
    try:
        return await docker_service.get_images()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.post("/images/pull", response_model=bool)
async def pull_docker_image(request: ImageActionRequest):
    """Pull a Docker image"""
    if not request.image_name:
        raise HTTPException(status_code=400, detail="Image name is required")
    try:
        return await docker_service.pull_image(request.image_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.delete("/images/{image_id}", response_model=bool)
async def remove_docker_image(image_id: str, force: bool = False):
    """Remove a Docker image"""
    try:
        return await docker_service.remove_image(image_id, force)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@docker_router.get("/info", response_model=DockerSystemInfoResponse)
async def get_docker_system_info():
    """Get Docker system information"""
    try:
        return await docker_service.get_system_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(docker_router)

@proxmox_router.get("/vms", response_model=List[ProxmoxVMResponse])
async def get_all_proxmox_vms():
    """List all Proxmox VMs and Containers"""
    try:
        return await proxmox_service.get_vms()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proxmox_router.get("/vms/{vmid}/status", response_model=ProxmoxVMStatusResponse)
async def get_proxmox_vm_status(vmid: int):
    """Get status of a specific Proxmox VM"""
    try:
        return await proxmox_service.get_vm_status(vmid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proxmox_router.post("/vms/{vmid}/action", response_model=bool)
async def perform_proxmox_vm_action(vmid: int, request: ProxmoxVMActionRequest):
    """Perform an action on a Proxmox VM (start, stop, restart, shutdown)"""
    try:
        return await proxmox_service.vm_action(vmid, request.action)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proxmox_router.get("/containers", response_model=List[ProxmoxContainerResponse])
async def get_all_proxmox_containers():
    """List all Proxmox LXC Containers"""
    try:
        return await proxmox_service.get_containers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proxmox_router.post("/containers/{vmid}/action", response_model=bool)
async def perform_proxmox_container_action(vmid: int, request: ProxmoxContainerActionRequest):
    """Perform an action on a Proxmox Container"""
    try:
        return await proxmox_service.container_action(vmid, request.action)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proxmox_router.get("/cluster/status", response_model=ProxmoxClusterStatusResponse)
async def get_proxmox_cluster_status():
    """Get Proxmox Cluster Status"""
    try:
        return await proxmox_service.get_cluster_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@proxmox_router.get("/vms", response_model=List[ProxmoxVMResponse])
async def get_all_proxmox_vms():
    """List all Proxmox VMs and Containers"""
    try:
        return await proxmox_service.get_vms()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proxmox_router.get("/vms/{vmid}/status", response_model=ProxmoxVMStatusResponse)
async def get_proxmox_vm_status(vmid: int):
    """Get status of a specific Proxmox VM"""
    try:
        return await proxmox_service.get_vm_status(vmid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proxmox_router.post("/vms/{vmid}/action", response_model=bool)
async def perform_proxmox_vm_action(vmid: int, request: ProxmoxVMActionRequest):
    """Perform an action on a Proxmox VM (start, stop, restart, shutdown)"""
    try:
        return await proxmox_service.vm_action(vmid, request.action)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proxmox_router.get("/containers", response_model=List[ProxmoxContainerResponse])
async def get_all_proxmox_containers():
    """List all Proxmox LXC Containers"""
    try:
        return await proxmox_service.get_containers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proxmox_router.post("/containers/{vmid}/action", response_model=bool)
async def perform_proxmox_container_action(vmid: int, request: ProxmoxContainerActionRequest):
    """Perform an action on a Proxmox Container"""
    try:
        return await proxmox_service.container_action(vmid, request.action)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@proxmox_router.get("/cluster/status", response_model=ProxmoxClusterStatusResponse)
async def get_proxmox_cluster_status():
    """Get Proxmox Cluster Status"""
    try:
        return await proxmox_service.get_cluster_status()
    except Exception as e:
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
