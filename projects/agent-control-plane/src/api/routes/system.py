#!/usr/bin/env python3
"""
System API Routes
"""

from fastapi import APIRouter, HTTPException

from src.services.system import SystemService

router = APIRouter()
system_service = SystemService()


@router.get("/info")
async def get_system_info():
    """Get system information"""
    try:
        await system_service.initialize()
        return await system_service.get_system_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/cpu")
async def get_cpu_usage():
    """Get CPU usage"""
    try:
        await system_service.initialize()
        return await system_service.get_cpu_usage()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/memory")
async def get_memory_usage():
    """Get memory usage"""
    try:
        await system_service.initialize()
        return await system_service.get_memory_usage()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/processes")
async def get_process_list():
    """Get process list"""
    try:
        await system_service.initialize()
        return await system_service.get_process_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/command")
async def execute_command(command: str, timeout: int = 30):
    """Execute system command"""
    try:
        await system_service.initialize()
        return await system_service.execute_command(command, timeout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/services/{service_name}")
async def get_service_status(service_name: str):
    """Get service status"""
    try:
        await system_service.initialize()
        return await system_service.get_service_status(service_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/services/{service_name}/{action}")
async def control_service(service_name: str, action: str):
    """Control system service"""
    try:
        await system_service.initialize()
        return await system_service.control_service(service_name, action)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
