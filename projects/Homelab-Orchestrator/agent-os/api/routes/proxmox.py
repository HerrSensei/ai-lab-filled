from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from ...services.proxmox import ProxmoxService

proxmox_router = APIRouter(prefix="/proxmox", tags=["Proxmox"])

# Initialize service instance (will be managed by agent_manager later)
proxmox_service = ProxmoxService(config={})

class ProxmoxVMResponse(BaseModel):
    vmid: int
    name: str
    status: str
    node: str
    type: str

class ProxmoxVMStatusResponse(BaseModel):
    qemu: int
    status: str
    name: str
    uptime: int
    mem: int
    maxmem: int
    cpu: float
    maxcpu: int
    disk: int
    maxdisk: int

class ProxmoxVMActionRequest(BaseModel):
    vmid: int
    action: str

class ProxmoxContainerResponse(BaseModel):
    vmid: int
    name: str
    status: str
    node: str
    type: str

class ProxmoxContainerActionRequest(BaseModel):
    vmid: int
    action: str

class ProxmoxClusterStatusResponse(BaseModel):
    __root__: Dict[str, Any]

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
