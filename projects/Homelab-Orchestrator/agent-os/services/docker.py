#!/usr/bin/env python3
"""
Docker Service - Container Management
"""

import logging
from typing import Any
import asyncio

import aiohttp

from ...core.base_service import BaseAgentService

logger = logging.getLogger(__name__)


class DockerService(BaseAgentService):
    """Docker Container Management Service"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.base_url = self.config.get("docker_host", "unix:///var/run/docker.sock")
        self.session: Optional[aiohttp.ClientSession] = None

    async def initialize(self):
        """Initialisiere Docker Verbindung"""
        try:
            self.session = aiohttp.ClientSession()
            self.logger.info("Docker service initialized successfully")

        except Exception as e:
            self.logger.error(f"Docker initialization error: {e}")
            raise

    async def health_check(self) -> bool:
        """Health Check für Docker"""
        if not self.session:
            return False

        try:
            # Docker Ping
            async with self.session.get(f"{self.base_url}/_ping") as resp:
                return resp.status == 200
        except Exception:
            return False

    async def run(self) -> None:
        """Run the main logic of the service. For DockerService, this is a no-op as it's primarily reactive."""
        self.logger.info("Docker service is running in reactive mode.")
        while True:
            await asyncio.sleep(self.config.get("check_interval", 60)) # Keep alive and allow for checks
            # No active tasks for DockerService, it responds to requests
            pass

    async def get_containers(
        self, all_containers: bool = False
    ) -> list[dict[str, Any]]:
        """Liste alle Container"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            params = {"all": str(all_containers).lower()}
            async with self.session.get(
                f"{self.base_url}/containers/json", params=params
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    raise Exception(f"Failed to get containers: {resp.status}")
        except Exception as e:
            self.logger.error(f"Error getting containers: {e}")
            raise

    async def get_container_info(self, container_id: str) -> dict[str, Any]:
        """Container Informationen"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            async with self.session.get(
                f"{self.base_url}/containers/{container_id}/json"
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    raise Exception(f"Failed to get container info: {resp.status}")
        except Exception as e:
            self.logger.error(f"Error getting container info: {e}")
            raise

    async def get_container_logs(self, container_id: str, lines: int = 100) -> str:
        """Container Logs"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            params = {"stdout": "true", "stderr": "true", "tail": str(lines)}
            async with self.session.get(
                f"{self.base_url}/containers/{container_id}/logs", params=params
            ) as resp:
                if resp.status == 200:
                    data = await resp.text()
                    return data
                else:
                    raise Exception(f"Failed to get container logs: {resp.status}")
        except Exception as e:
            self.logger.error(f"Error getting container logs: {e}")
            raise

    async def get_container_stats(self, container_id: str) -> dict[str, Any]:
        """Container Statistiken"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            async with self.session.get(
                f"{self.base_url}/containers/{container_id}/stats",
                params={"stream": "false"},
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    raise Exception(f"Failed to get container stats: {resp.status}")
        except Exception as e:
            self.logger.error(f"Error getting container stats: {e}")
            raise

    async def start_container(self, container_id: str) -> bool:
        """Container starten"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            async with self.session.post(
                f"{self.base_url}/containers/{container_id}/start"
            ) as resp:
                return resp.status in [200, 204]
        except Exception as e:
            self.logger.error(f"Error starting container: {e}")
            raise

    async def stop_container(self, container_id: str, timeout: int = 10) -> bool:
        """Container stoppen"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            params = {"t": str(timeout)}
            async with self.session.post(
                f"{self.base_url}/containers/{container_id}/stop", params=params
            ) as resp:
                return resp.status in [200, 204]
        except Exception as e:
            self.logger.error(f"Error stopping container: {e}")
            raise

    async def restart_container(self, container_id: str, timeout: int = 10) -> bool:
        """Container neustarten"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            params = {"t": str(timeout)}
            async with self.session.post(
                f"{self.base_url}/containers/{container_id}/restart", params=params
            ) as resp:
                return resp.status in [200, 204]
        except Exception as e:
            self.logger.error(f"Error restarting container: {e}")
            raise

    async def remove_container(self, container_id: str, force: bool = False) -> bool:
        """Container entfernen"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            params = {"force": str(force).lower()}
            async with self.session.delete(
                f"{self.base_url}/containers/{container_id}", params=params
            ) as resp:
                return resp.status in [200, 204]
        except Exception as e:
            self.logger.error(f"Error removing container: {e}")
            raise

    async def get_images(self) -> list[dict[str, Any]]:
        """Liste alle Images"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            async with self.session.get(f"{self.base_url}/images/json") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    raise Exception(f"Failed to get images: {resp.status}")
        except Exception as e:
            self.logger.error(f"Error getting images: {e}")
            raise

    async def pull_image(self, image_name: str) -> bool:
        """Image pullen"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            params = {"fromImage": image_name}
            async with self.session.post(
                f"{self.base_url}/images/create", params=params
            ) as resp:
                return resp.status in [200, 204]
        except Exception as e:
            self.logger.error(f"Error pulling image: {e}")
            raise

    async def remove_image(self, image_id: str, force: bool = False) -> bool:
        """Image entfernen"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            params = {"force": str(force).lower()}
            async with self.session.delete(
                f"{self.base_url}/images/{image_id}", params=params
            ) as resp:
                return resp.status in [200, 204]
        except Exception as e:
            self.logger.error(f"Error removing image: {e}")
            raise

    async def get_system_info(self) -> dict[str, Any]:
        """Docker System Informationen"""
        if not self.session:
            raise Exception("Service not initialized")

        try:
            async with self.session.get(f"{self.base_url}/info") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    raise Exception(f"Failed to get system info: {resp.status}")
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            raise

    async def cleanup(self):
        """Cleanup bei Shutdown"""
        if self.session:
            await self.session.close()
        self.logger.info("Docker service cleaned up")
