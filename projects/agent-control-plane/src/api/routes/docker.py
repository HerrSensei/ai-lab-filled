#!/usr/bin/env python3
"""
Docker API Routes
"""

from typing import Any

from fastapi import APIRouter, HTTPException

from src.services.docker import DockerService

router = APIRouter()
docker_service = DockerService()


@router.get("/")
async def get_containers(all_containers: bool = False) -> list[dict[str, Any]]:
    """Get all containers"""
    try:
        await docker_service.initialize()
        return await docker_service.get_containers(all_containers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{container_id}")
async def get_container_info(container_id: str) -> dict[str, Any]:
    """Get container information"""
    try:
        await docker_service.initialize()
        return await docker_service.get_container_info(container_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{container_id}/stats")
async def get_container_stats(container_id: str) -> dict[str, Any]:
    """Get container statistics"""
    try:
        await docker_service.initialize()
        return await docker_service.get_container_stats(container_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{container_id}/start")
async def start_container(container_id: str):
    """Start container"""
    try:
        await docker_service.initialize()
        await docker_service.start_container(container_id)
        return {"message": f"Container {container_id} started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{container_id}/stop")
async def stop_container(container_id: str):
    """Stop container"""
    try:
        await docker_service.initialize()
        await docker_service.stop_container(container_id)
        return {"message": f"Container {container_id} stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{container_id}/restart")
async def restart_container(container_id: str):
    """Restart container"""
    try:
        await docker_service.initialize()
        await docker_service.restart_container(container_id)
        return {"message": f"Container {container_id} restarted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{container_id}")
async def remove_container(container_id: str):
    """Remove container"""
    try:
        await docker_service.initialize()
        await docker_service.remove_container(container_id)
        return {"message": f"Container {container_id} removed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/images/")
async def get_images() -> list[dict[str, Any]]:
    """Get all images"""
    try:
        await docker_service.initialize()
        return await docker_service.get_images()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/images/pull")
async def pull_image(image_name: str):
    """Pull image"""
    try:
        await docker_service.initialize()
        await docker_service.pull_image(image_name)
        return {"message": f"Image {image_name} pulled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/images/{image_id}")
async def remove_image(image_id: str):
    """Remove image"""
    try:
        await docker_service.initialize()
        await docker_service.remove_image(image_id)
        return {"message": f"Image {image_id} removed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/system/info")
async def get_system_info() -> dict[str, Any]:
    """Get Docker system information"""
    try:
        await docker_service.initialize()
        return await docker_service.get_system_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
