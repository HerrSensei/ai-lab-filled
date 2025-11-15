#!/usr/bin/env python3
"""
Enhanced Proxmox Service for Homelab Management
Based on Agent Control Plane architecture
"""

import logging
from typing import Any, Dict, List, Optional

import aiohttp

from .base_service import BaseService

logger = logging.getLogger(__name__)


class ProxmoxService(BaseService):
    """Enhanced Proxmox VE Management Service"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("proxmox")
        self.config = config or {}
        self.base_url = None
        self.session = None
        self.ticket = None
        self.csrf_token = None

    async def _initialize(self) -> bool:
        """Initialize Proxmox connection"""
        try:
            # Load configuration
            self.base_url = self.config.get("base_url", "https://proxmox.local:8006")
            username = self.config.get("username", "root@pam")
            password = self.config.get("password")

            if not password:
                self.logger.error("Proxmox password not configured")
                return False

            # Create session
            self.session = aiohttp.ClientSession()

            # Login
            login_data = {"username": username, "password": password}

            async with self.session.post(
                f"{self.base_url}/api2/json/access/ticket", json=login_data, ssl=False
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.ticket = data["data"]["ticket"]
                    self.csrf_token = data["data"]["CSRFPreventionToken"]
                    self.logger.info("Proxmox authentication successful")
                    return True
                else:
                    self.logger.error(f"Proxmox login failed: {resp.status}")
                    return False

        except Exception as e:
            self.logger.error(f"Proxmox initialization error: {e}")
            return False

    async def _health_check(self) -> Dict[str, Any]:
        """Health check for Proxmox"""
        try:
            if not self.session or not self.ticket:
                return {"status": "unhealthy", "reason": "Not authenticated"}

            async with self.session.get(
                f"{self.base_url}/api2/json/version",
                cookies={"PVEAuthCookie": self.ticket},
                ssl=False,
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "status": "healthy",
                        "version": data["data"],
                        "api_accessible": True,
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "reason": f"API returned {resp.status}",
                    }
        except Exception as e:
            return {"status": "unhealthy", "reason": str(e)}

    async def _cleanup(self):
        """Cleanup Proxmox resources"""
        if self.session:
            await self.session.close()
            self.session = None

    async def get_vms(self) -> List[Dict[str, Any]]:
        """List all VMs"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.get(
                f"{self.base_url}/api2/json/cluster/resources",
                params={"type": "vm"},
                cookies={"PVEAuthCookie": self.ticket},
                ssl=False,
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["data"]
                else:
                    raise Exception(f"Failed to get VMs: {resp.status}")
        except Exception as e:
            self.logger.error(f"Error getting VMs: {e}")
            raise

    async def get_vm_status(self, vmid: int) -> Dict[str, Any]:
        """Get VM status"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.get(
                f"{self.base_url}/api2/json/nodes/proxmox/qemu/{vmid}/status/current",
                cookies={"PVEAuthCookie": self.ticket},
                ssl=False,
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["data"]
                else:
                    raise Exception(f"Failed to get VM status: {resp.status}")
        except Exception as e:
            self.logger.error(f"Error getting VM status: {e}")
            raise

    async def vm_action(self, vmid: int, action: str) -> bool:
        """Perform VM action (start, stop, restart, shutdown)"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.post(
                f"{self.base_url}/api2/json/nodes/proxmox/qemu/{vmid}/status/{action}",
                cookies={"PVEAuthCookie": self.ticket},
                headers={"CSRFPreventionToken": self.csrf_token},
                ssl=False,
            ) as resp:
                return resp.status == 200
        except Exception as e:
            self.logger.error(f"Error performing VM action {action}: {e}")
            raise

    async def get_containers(self) -> List[Dict[str, Any]]:
        """List all LXC containers"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.get(
                f"{self.base_url}/api2/json/cluster/resources",
                params={"type": "lxc"},
                cookies={"PVEAuthCookie": self.ticket},
                ssl=False,
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["data"]
                else:
                    raise Exception(f"Failed to get containers: {resp.status}")
        except Exception as e:
            self.logger.error(f"Error getting containers: {e}")
            raise

    async def container_action(self, vmid: int, action: str) -> bool:
        """Perform container action"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.post(
                f"{self.base_url}/api2/json/nodes/proxmox/lxc/{vmid}/status/{action}",
                cookies={"PVEAuthCookie": self.ticket},
                headers={"CSRFPreventionToken": self.csrf_token},
                ssl=False,
            ) as resp:
                return resp.status == 200
        except Exception as e:
            self.logger.error(f"Error performing container action {action}: {e}")
            raise

    async def get_cluster_status(self) -> Dict[str, Any]:
        """Get cluster status"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.get(
                f"{self.base_url}/api2/json/cluster/status",
                cookies={"PVEAuthCookie": self.ticket},
                ssl=False,
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["data"]
                else:
                    raise Exception(f"Failed to get cluster status: {resp.status}")
        except Exception as e:
            self.logger.error(f"Error getting cluster status: {e}")
            raise
