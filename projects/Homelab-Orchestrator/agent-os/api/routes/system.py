from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from ...services.system import SystemService

system_router = APIRouter(prefix="/system", tags=["System"])

# Initialize service instance (will be managed by agent_manager later)
system_service = SystemService(config={})

class SystemInfoResponse(BaseModel):
    hostname: str
    platform: str
    release: str
    version: str
    machine: str
    uptime: str
    cpu_count: int
    cpu_count_logical: int
    memory_total: int
    memory_available: int
    disk_usage: Dict[str, Any]

class CpuUsageResponse(BaseModel):
    cpu_percent_per_core: List[float]
    cpu_percent_total: float
    cpu_freq_current: Optional[float]
    cpu_freq_min: Optional[float]
    cpu_freq_max: Optional[float]
    load_avg: Optional[List[float]]

class MemoryUsageResponse(BaseModel):
    virtual: Dict[str, Any]
    swap: Dict[str, Any]

class NetworkStatsResponse(BaseModel):
    __root__: Dict[str, Any]

class ProcessInfo(BaseModel):
    pid: int
    name: str
    username: str
    cpu_percent: float
    memory_percent: float
    status: str

class CommandExecuteRequest(BaseModel):
    command: str
    timeout: int = 30

class CommandExecuteResponse(BaseModel):
    command: str
    returncode: int
    stdout: str
    stderr: str
    success: bool

class ServiceStatusResponse(BaseModel):
    service: str
    active: bool
    enabled: bool
    loaded: bool
    raw_output: str

class ControlServiceRequest(BaseModel):
    service_name: str
    action: str

class DiskUsageResponse(BaseModel):
    path: str
    total: int
    used: int
    free: int
    percent: float

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
