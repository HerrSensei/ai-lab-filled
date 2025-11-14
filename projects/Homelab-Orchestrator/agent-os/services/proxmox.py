#!/usr/bin/env python3
"""
Proxmox Service - VM und Container Management
"""

import logging
from typing import Any, Optional
import asyncio

import aiohttp

from ...core.base_service import BaseAgentService

logger = logging.getLogger(__name__)


class ProxmoxService(BaseAgentService):
    """Proxmox VE Management Service"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.base_url = self.config.get("proxmox_url", "https://proxmox.local:8006")
        self.username = self.config.get("proxmox_username", "root@pam")
        self.password = self.config.get("proxmox_password", "your_password")
        self.session: Optional[aiohttp.ClientSession] = None
        self.ticket: Optional[str] = None
        self.csrf_token: Optional[str] = None

    async def initialize(self):
        """Initialisiere Proxmox Verbindung"""
        try:
            self.session = aiohttp.ClientSession()

            # Login
            login_data = {
                "username": self.username,
                "password": self.password,
            }

            async with self.session.post(
                f"{self.base_url}/api2/json/access/ticket", json=login_data, ssl=False
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.ticket = data["data"]["ticket"]
                    self.csrf_token = data["data"]["CSRFPreventionToken"]
                    self.logger.info("Proxmox service initialized successfully")
                else:
                    self.logger.error(f"Proxmox login failed: {resp.status}")
                    raise Exception(f"Proxmox login failed with status: {resp.status}")

        except Exception as e:
            self.logger.error(f"Proxmox initialization error: {e}")
            raise

    async def health_check(self) -> bool:
        """Health Check für Proxmox"""
        if not self.session or not self.ticket:
            return False

        try:
            async with self.session.get(
                f"{self.base_url}/api2/json/version",
                cookies={"PVEAuthCookie": self.ticket},
                ssl=False,
            ) as resp:
                return resp.status == 200
        except Exception:
            return False

    async def run(self) -> None:
        """Run the main logic of the service. For ProxmoxService, this is a no-op as it's primarily reactive."""
        self.logger.info("Proxmox service is running in reactive mode.")
        while True:
            await asyncio.sleep(self.config.get("check_interval", 60)) # Keep alive and allow for checks
            # No active tasks for ProxmoxService, it responds to requests
            pass

    async def get_vms(self) -> list[dict[str, Any]]:
        """Liste alle VMs und Container"""
        if not self.session or not self.ticket:
            raise Exception("Service not initialized or not authenticated")

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

    async def get_vm_status(self, vmid: int) -> dict[str, Any]:
        """Status einer spezifischen VM"""
        if not self.session or not self.ticket:
            raise Exception("Service not initialized or not authenticated")

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
        """Führe Aktion auf VM durch (start, stop, restart, shutdown)"""
        if not self.session or not self.ticket:
            raise Exception("Service not initialized or not authenticated")

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

    async def get_containers(self) -> list[dict[str, Any]]:
        """Liste alle LXC Container"""
        if not self.session or not self.ticket:
            raise Exception("Service not initialized or not authenticated")

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
        """Führe Aktion auf Container durch"""
        if not self.session or not self.ticket:
            raise Exception("Service not initialized or not authenticated")

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

    async def get_cluster_status(self) -> dict[str, Any]:
        """Cluster Status"""
        if not self.session or not self.ticket:
            raise Exception("Service not initialized or not authenticated")

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

    async def cleanup(self):
        """Cleanup bei Shutdown"""
        if self.session:
            await self.session.close()
        self.logger.info("Proxmox service cleaned up")
