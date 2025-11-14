#!/usr/bin/env python3
"""
API Routes Package
"""

from fastapi import APIRouter

# Import individual route modules
from . import adguard, auth, docker, hisense, proxmox, system

# Main router
router = APIRouter()

# Include all sub-routers
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(proxmox.router, prefix="/proxmox", tags=["Proxmox"])
router.include_router(adguard.router, prefix="/adguard", tags=["AdGuard"])
router.include_router(docker.router, prefix="/docker", tags=["Docker"])
router.include_router(system.router, prefix="/system", tags=["System"])
router.include_router(hisense.router, prefix="/hisense", tags=["Hisense TV"])

__all__ = ["router"]
