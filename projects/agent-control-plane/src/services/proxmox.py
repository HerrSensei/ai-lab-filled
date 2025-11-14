#!/usr/bin/env python3
"""
Proxmox Service - VM und Container Management
"""

import logging
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class ProxmoxService:
    """Proxmox VE Management Service"""

    def __init__(self):
        self.base_url = None
        self.session = None
        self.ticket = None
        self.csrf_token = None
        self.initialized = False

    async def initialize(self):
        """Initialisiere Proxmox Verbindung"""
        try:
            # TODO: Load from config
            self.base_url = "https://proxmox.local:8006"
            self.session = aiohttp.ClientSession()

            # Login
            login_data = {
                "username": "root@pam",
                "password": "your_password",  # TODO: Load from secure config
            }

            async with self.session.post(
                f"{self.base_url}/api2/json/access/ticket", json=login_data, ssl=False
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.ticket = data["data"]["ticket"]
                    self.csrf_token = data["data"]["CSRFPreventionToken"]
                    self.initialized = True
                    logger.info("Proxmox service initialized successfully")
                else:
                    logger.error(f"Proxmox login failed: {resp.status}")

        except Exception as e:
            logger.error(f"Proxmox initialization error: {e}")

    async def health_check(self) -> bool:
        """Health Check für Proxmox"""
        if not self.initialized:
            return False

        try:
            async with self.session.get(
                f"{self.base_url}/api2/json/version",
                cookies={"PVEAuthCookie": self.ticket},
                ssl=False,
            ) as resp:
                return resp.status == 200
        except:
            return False

    async def get_vms(self) -> list[dict[str, Any]]:
        """Liste alle VMs und Container"""
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
            logger.error(f"Error getting VMs: {e}")
            raise

    async def get_vm_status(self, vmid: int) -> dict[str, Any]:
        """Status einer spezifischen VM"""
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
            logger.error(f"Error getting VM status: {e}")
            raise

    async def vm_action(self, vmid: int, action: str) -> bool:
        """Führe Aktion auf VM durch (start, stop, restart, shutdown)"""
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
            logger.error(f"Error performing VM action {action}: {e}")
            raise

    async def get_containers(self) -> list[dict[str, Any]]:
        """Liste alle LXC Container"""
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
            logger.error(f"Error getting containers: {e}")
            raise

    async def container_action(self, vmid: int, action: str) -> bool:
        """Führe Aktion auf Container durch"""
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
            logger.error(f"Error performing container action {action}: {e}")
            raise

    async def get_cluster_status(self) -> dict[str, Any]:
        """Cluster Status"""
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
            logger.error(f"Error getting cluster status: {e}")
            raise

    async def cleanup(self):
        """Cleanup bei Shutdown"""
        if self.session:
            await self.session.close()
        logger.info("Proxmox service cleaned up")
