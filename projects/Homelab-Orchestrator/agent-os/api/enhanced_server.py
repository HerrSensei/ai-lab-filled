#!/usr/bin/env python3
"""
FastAPI Server for Enhanced Homelab Management
Based on Agent Control Plane architecture
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..core.enhanced_homelab_manager import get_homelab_manager

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# FastAPI App
app = FastAPI(
    title="Enhanced Homelab Manager API",
    description="RESTful API for homelab infrastructure management",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models
class HealthResponse(BaseModel):
    timestamp: str
    overall_status: str
    services: Dict[str, Any]
    summary: Dict[str, int]


class ServiceActionRequest(BaseModel):
    action: str  # start, stop, restart, etc.


class CommandRequest(BaseModel):
    command: str
    timeout: Optional[int] = 30


class CommandResponse(BaseModel):
    command: str
    returncode: int
    stdout: str
    stderr: str
    success: bool


# Global homelab manager
homelab_manager = None


@app.on_event("startup")
async def startup_event():
    """Initialize the homelab manager on startup"""
    global homelab_manager
    logger.info("Starting Enhanced Homelab Manager API...")
    homelab_manager = await get_homelab_manager()
    logger.info("Enhanced Homelab Manager API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global homelab_manager
    logger.info("Shutting down Enhanced Homelab Manager API...")
    if homelab_manager:
        await homelab_manager.cleanup()
    logger.info("Enhanced Homelab Manager API shutdown complete")


# Health and System Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Overall system health check"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        health_data = await homelab_manager.get_system_health()
        return HealthResponse(**health_data)
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/services")
async def list_services():
    """List all available services"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        services = await homelab_manager.list_services()
        return {"services": services}
    except Exception as e:
        logger.error(f"Error listing services: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/services/{service_name}/health")
async def service_health_check(service_name: str):
    """Health check for specific service"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        service = await homelab_manager.get_service(service_name)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service {service_name} not found",
            )

        health = await service.health_check()
        return health
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Service health check error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/services/{service_name}/restart")
async def restart_service(service_name: str):
    """Restart a specific service"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        success = await homelab_manager.restart_service(service_name)
        if success:
            return {"message": f"Service {service_name} restarted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to restart service {service_name}",
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Service restart error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# System Service Endpoints
@app.get("/system/info")
async def get_system_info():
    """Get system information"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        system_service = await homelab_manager.get_service("system")
        if not system_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="System service not available",
            )

        info = await system_service.get_system_info()
        return info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"System info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/system/cpu")
async def get_cpu_usage():
    """Get CPU usage information"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        system_service = await homelab_manager.get_service("system")
        if not system_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="System service not available",
            )

        cpu_data = await system_service.get_cpu_usage()
        return cpu_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CPU usage error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/system/memory")
async def get_memory_usage():
    """Get memory usage information"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        system_service = await homelab_manager.get_service("system")
        if not system_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="System service not available",
            )

        memory_data = await system_service.get_memory_usage()
        return memory_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Memory usage error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/system/command", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """Execute a system command"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        system_service = await homelab_manager.get_service("system")
        if not system_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="System service not available",
            )

        result = await system_service.execute_command(request.command, request.timeout)
        return CommandResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Command execution error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Docker Service Endpoints
@app.get("/docker/containers")
async def get_docker_containers():
    """Get Docker containers"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        docker_service = await homelab_manager.get_service("docker")
        if not docker_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Docker service not available",
            )

        containers = await docker_service.get_containers()
        return {"containers": containers}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Docker containers error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/docker/containers/{container_id}/action")
async def docker_container_action(container_id: str, request: ServiceActionRequest):
    """Perform action on Docker container"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        docker_service = await homelab_manager.get_service("docker")
        if not docker_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Docker service not available",
            )

        success = await docker_service.container_action(container_id, request.action)
        if success:
            return {"message": f"Container {container_id} {request.action} successful"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to {request.action} container {container_id}",
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Docker container action error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Proxmox Service Endpoints
@app.get("/proxmox/vms")
async def get_proxmox_vms():
    """Get Proxmox VMs"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        proxmox_service = await homelab_manager.get_service("proxmox")
        if not proxmox_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proxmox service not available",
            )

        vms = await proxmox_service.get_vms()
        return {"vms": vms}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Proxmox VMs error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/proxmox/vms/{vmid}/action")
async def proxmox_vm_action(vmid: int, request: ServiceActionRequest):
    """Perform action on Proxmox VM"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        proxmox_service = await homelab_manager.get_service("proxmox")
        if not proxmox_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proxmox service not available",
            )

        success = await proxmox_service.vm_action(vmid, request.action)
        if success:
            return {"message": f"VM {vmid} {request.action} successful"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to {request.action} VM {vmid}",
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Proxmox VM action error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Monitoring Endpoints
@app.get("/monitoring")
async def get_monitoring_data():
    """Get comprehensive monitoring data"""
    if not homelab_manager:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Homelab manager not initialized",
        )

    try:
        monitoring_data = await homelab_manager.get_monitoring_data()
        return monitoring_data
    except Exception as e:
        logger.error(f"Monitoring data error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
