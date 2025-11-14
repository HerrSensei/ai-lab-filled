#!/usr/bin/env python3
"""
Proxmox API Routes
"""

from typing import Any

from fastapi import APIRouter, HTTPException

from src.services.proxmox import ProxmoxService

router = APIRouter()
proxmox_service = ProxmoxService()


@router.get("/vms")
async def get_vms() -> list[dict[str, Any]]:
    """Get all VMs and containers"""
    try:
        await proxmox_service.initialize()
        return await proxmox_service.get_vms()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/vms/{vmid}")
async def get_vm_status(vmid: int) -> dict[str, Any]:
    """Get VM status"""
    try:
        await proxmox_service.initialize()
        return await proxmox_service.get_vm_status(vmid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/vms/{vmid}/{action}")
async def vm_action(vmid: int, action: str):
    """Control VM (start, stop, restart)"""
    try:
        await proxmox_service.initialize()
        await proxmox_service.vm_action(vmid, action)
        return {"message": f"VM {vmid} {action} action completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/containers")
async def get_containers() -> list[dict[str, Any]]:
    """Get all LXC containers"""
    try:
        await proxmox_service.initialize()
        return await proxmox_service.get_containers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/containers/{vmid}/{action}")
async def container_action(vmid: int, action: str):
    """Control container (start, stop, restart)"""
    try:
        await proxmox_service.initialize()
        await proxmox_service.container_action(vmid, action)
        return {"message": f"Container {vmid} {action} action completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/cluster/status")
async def get_cluster_status() -> dict[str, Any]:
    """Get cluster status"""
    try:
        await proxmox_service.initialize()
        return await proxmox_service.get_cluster_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
