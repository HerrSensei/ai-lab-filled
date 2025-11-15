#!/usr/bin/env python3
"""
Enhanced Homelab Manager with Service Architecture
Based on Agent Control Plane patterns
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from ..services.base_service import ServiceManager
from ..services.proxmox_service import ProxmoxService
from ..services.docker_service import DockerService
from ..services.system_service import SystemService

logger = logging.getLogger(__name__)


class EnhancedHomelabManager:
    """Enhanced homelab manager with modular service architecture"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/homelab_config.json"
        self.config = {}
        self.service_manager = ServiceManager()
        self.logger = logging.getLogger("homelab_manager")
        self.initialized = False

    async def initialize(self) -> bool:
        """Initialize the homelab manager"""
        try:
            self.logger.info("Initializing Enhanced Homelab Manager...")

            # Load configuration
            await self._load_config()

            # Initialize services
            await self._initialize_services()

            self.initialized = True
            self.logger.info("Enhanced Homelab Manager initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize homelab manager: {e}")
            return False

    async def _load_config(self):
        """Load configuration from file"""
        try:
            config_file = Path(self.config_path)
            if config_file.exists():
                import json

                with open(config_file) as f:
                    self.config = json.load(f)
                self.logger.info(f"Configuration loaded from {self.config_path}")
            else:
                self.logger.warning(
                    f"Config file {self.config_path} not found, using defaults"
                )
                self.config = self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            self.config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "services": {
                "proxmox": {
                    "enabled": True,
                    "base_url": "https://proxmox.local:8006",
                    "username": "root@pam",
                },
                "docker": {
                    "enabled": True,
                    "base_url": "unix://var/run/docker.sock",
                },
                "system": {
                    "enabled": True,
                },
            },
            "monitoring": {
                "health_check_interval": 60,
                "log_level": "INFO",
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8080,
                "enable_cors": True,
            },
        }

    async def _initialize_services(self):
        """Initialize all configured services"""
        services_config = self.config.get("services", {})

        # Initialize Proxmox service
        if services_config.get("proxmox", {}).get("enabled", False):
            proxmox_config = services_config["proxmox"]
            proxmox_service = ProxmoxService(proxmox_config)
            self.service_manager.register_service(proxmox_service)

        # Initialize Docker service
        if services_config.get("docker", {}).get("enabled", False):
            docker_config = services_config["docker"]
            docker_service = DockerService(docker_config)
            self.service_manager.register_service(docker_service)

        # Initialize System service
        if services_config.get("system", {}).get("enabled", False):
            system_config = services_config.get("system", {})
            system_service = SystemService(system_config)
            self.service_manager.register_service(system_service)

        # Initialize all services
        init_results = await self.service_manager.initialize_all()

        for service_name, success in init_results.items():
            if success:
                self.logger.info(f"Service {service_name} initialized successfully")
            else:
                self.logger.error(f"Failed to initialize service {service_name}")

    async def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health"""
        if not self.initialized:
            raise Exception("Manager not initialized")

        try:
            health_results = await self.service_manager.health_check_all()

            # Calculate overall health
            healthy_services = sum(
                1 for h in health_results.values() if h.get("status") == "healthy"
            )
            total_services = len(health_results)
            overall_status = (
                "healthy"
                if healthy_services == total_services
                else "degraded"
                if healthy_services > 0
                else "unhealthy"
            )

            return {
                "timestamp": datetime.now().isoformat(),
                "overall_status": overall_status,
                "services": health_results,
                "summary": {
                    "total_services": total_services,
                    "healthy_services": healthy_services,
                    "unhealthy_services": total_services - healthy_services,
                },
            }
        except Exception as e:
            self.logger.error(f"Error getting system health: {e}")
            raise

    async def get_service(self, service_name: str):
        """Get a specific service"""
        if not self.initialized:
            raise Exception("Manager not initialized")

        return self.service_manager.get_service(service_name)

    async def list_services(self) -> list[str]:
        """List all available services"""
        if not self.initialized:
            raise Exception("Manager not initialized")

        return self.service_manager.list_services()

    async def restart_service(self, service_name: str) -> bool:
        """Restart a specific service"""
        if not self.initialized:
            raise Exception("Manager not initialized")

        try:
            service = self.service_manager.get_service(service_name)
            if not service:
                self.logger.error(f"Service {service_name} not found")
                return False

            await service.cleanup()
            await asyncio.sleep(1)  # Brief pause
            success = await service.initialize()

            if success:
                self.logger.info(f"Service {service_name} restarted successfully")
            else:
                self.logger.error(f"Failed to restart service {service_name}")

            return success
        except Exception as e:
            self.logger.error(f"Error restarting service {service_name}: {e}")
            return False

    async def get_monitoring_data(self) -> Dict[str, Any]:
        """Get comprehensive monitoring data"""
        if not self.initialized:
            raise Exception("Manager not initialized")

        try:
            monitoring_data = {
                "timestamp": datetime.now().isoformat(),
                "services": {},
            }

            # Get data from each service
            for service_name in self.service_manager.list_services():
                service = self.service_manager.get_service(service_name)
                if service and service.initialized:
                    try:
                        if service_name == "system":
                            # Get system metrics
                            system_service = service
                            monitoring_data["services"][service_name] = {
                                "cpu_usage": await system_service.get_cpu_usage(),
                                "memory_usage": await system_service.get_memory_usage(),
                                "disk_usage": await system_service.get_disk_usage(),
                                "network_stats": await system_service.get_network_stats(),
                            }
                        elif service_name == "docker":
                            # Get Docker metrics
                            docker_service = service
                            containers = await docker_service.get_containers()
                            monitoring_data["services"][service_name] = {
                                "containers": {
                                    "total": len(containers),
                                    "running": len(
                                        [
                                            c
                                            for c in containers
                                            if c["status"] == "running"
                                        ]
                                    ),
                                    "stopped": len(
                                        [
                                            c
                                            for c in containers
                                            if c["status"] == "exited"
                                        ]
                                    ),
                                },
                                "images": await docker_service.get_images(),
                            }
                        elif service_name == "proxmox":
                            # Get Proxmox metrics
                            proxmox_service = service
                            vms = await proxmox_service.get_vms()
                            containers = await proxmox_service.get_containers()
                            monitoring_data["services"][service_name] = {
                                "vms": {
                                    "total": len(vms),
                                    "running": len(
                                        [
                                            vm
                                            for vm in vms
                                            if vm.get("status") == "running"
                                        ]
                                    ),
                                },
                                "containers": {
                                    "total": len(containers),
                                    "running": len(
                                        [
                                            c
                                            for c in containers
                                            if c.get("status") == "running"
                                        ]
                                    ),
                                },
                            }
                    except Exception as e:
                        self.logger.error(
                            f"Error getting monitoring data for {service_name}: {e}"
                        )
                        monitoring_data["services"][service_name] = {"error": str(e)}

            return monitoring_data
        except Exception as e:
            self.logger.error(f"Error getting monitoring data: {e}")
            raise

    async def cleanup(self):
        """Cleanup all resources"""
        try:
            self.logger.info("Cleaning up Enhanced Homelab Manager...")
            await self.service_manager.cleanup_all()
            self.initialized = False
            self.logger.info("Enhanced Homelab Manager cleaned up successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


# Global instance
_homelab_manager = None


async def get_homelab_manager() -> EnhancedHomelabManager:
    """Get or create the global homelab manager instance"""
    global _homelab_manager
    if _homelab_manager is None:
        _homelab_manager = EnhancedHomelabManager()
        await _homelab_manager.initialize()
    return _homelab_manager
