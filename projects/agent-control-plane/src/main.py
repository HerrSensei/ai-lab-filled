#!/usr/bin/env python3
"""
Agent Control Plane - MCP Server für Homeserver Steuerung

Produktionsreifer MCP Server zur Verwaltung von:
- Linux User Authentication
- Proxmox VM/Container Management
- Service Management (AdGuard, Docker, etc.)
- Real-time Monitoring & Logging
"""

import json
import logging
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from src.api.routes import adguard, auth, docker, hisense, proxmox, system
from src.auth.token_manager import TokenManager

# Konfiguration
from src.auth.user_manager import UserManager
from src.services.adguard import AdGuardService
from src.services.docker import DockerService
from src.services.proxmox import ProxmoxService
from src.services.system import SystemService

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("agent-control-plane.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# FastAPI App
app = FastAPI(
    title="Agent Control Plane",
    description="MCP Server für Homeserver Steuerung",
    version="1.0.0",
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

# Security
security = HTTPBearer()

# Services Initialisierung
user_manager = UserManager()
token_manager = TokenManager()
proxmox_service = ProxmoxService()
adguard_service = AdGuardService()
docker_service = DockerService()
system_service = SystemService()

# API Router
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(proxmox.router, prefix="/proxmox", tags=["Proxmox"])
app.include_router(adguard.router, prefix="/adguard", tags=["AdGuard"])
app.include_router(docker.router, prefix="/docker", tags=["Docker"])
app.include_router(system.router, prefix="/system", tags=["System"])
app.include_router(hisense.router, prefix="/hisense", tags=["Hisense TV"])


# Health Check
@app.get("/health")
async def health_check():
    """Health Check Endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "proxmox": await proxmox_service.health_check(),
            "adguard": await adguard_service.health_check(),
            "docker": await docker_service.health_check(),
            "system": await system_service.health_check(),
        },
    }


# Startup
@app.on_event("startup")
async def startup_event():
    """Startup Initialisierung"""
    logger.info("Agent Control Plane starting up...")

    # Lade Konfiguration
    config_path = Path("config/config.json")
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            logger.info(f"Configuration loaded: {len(config)} services")

    # Initialisiere Services
    await user_manager.initialize()
    await proxmox_service.initialize()
    await adguard_service.initialize()
    await docker_service.initialize()
    await system_service.initialize()

    logger.info("Agent Control Plane startup complete")


# Shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown Cleanup"""
    logger.info("Agent Control Plane shutting down...")

    # Cleanup Services
    await proxmox_service.cleanup()
    await adguard_service.cleanup()
    await docker_service.cleanup()
    await system_service.cleanup()

    logger.info("Agent Control Plane shutdown complete")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
