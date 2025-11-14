from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from ...services.docker import DockerService

docker_router = APIRouter(prefix="/docker", tags=["Docker"])

# Initialize service instance (will be managed by agent_manager later)
docker_service = DockerService(config={})

class ContainerResponse(BaseModel):
    Id: str
    Names: List[str]
    Image: str
    Status: str
    State: str

class ContainerInfoResponse(BaseModel):
    Id: str
    Name: str
    State: Dict[str, Any]
    Config: Dict[str, Any]

class ContainerLogsResponse(BaseModel):
    logs: str

class ContainerStatsResponse(BaseModel):
    read: str
    preread: str
    pids_stats: Dict[str, Any]
    blkio_stats: Dict[str, Any]
    num_procs: int
    storage_stats: Dict[str, Any]
    cpu_stats: Dict[str, Any]
    memory_stats: Dict[str, Any]
    name: str
    id: str
    networks: Dict[str, Any]

class ImageResponse(BaseModel):
    Id: str
    RepoTags: List[str]
    Created: int
    Size: int

class DockerSystemInfoResponse(BaseModel):
    ID: str
    Containers: int
    Images: int
    OperatingSystem: str
    Architecture: str
    ServerVersion: str

class ContainerActionRequest(BaseModel):
    container_id: str
    timeout: Optional[int] = None

class ImageActionRequest(BaseModel):
    image_name: Optional[str] = None
    image_id: Optional[str] = None
    force: bool = False

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
