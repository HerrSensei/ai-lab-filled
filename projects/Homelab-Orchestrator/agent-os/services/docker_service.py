#!/usr/bin/env python3
"""
Enhanced Docker Service for Homelab Management
Based on Agent Control Plane architecture
"""

import logging
from typing import Any, Dict, List, Optional

try:
    import docker
    from docker.models.containers import Container
    from docker.models.images import Image
except ImportError:
    docker = None
    Container = None
    Image = None

from .base_service import BaseService

logger = logging.getLogger(__name__)


class DockerService(BaseService):
    """Enhanced Docker Management Service"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("docker")
        self.config = config or {}
        self.client = None

    async def _initialize(self) -> bool:
        """Initialize Docker connection"""
        try:
            if docker is None:
                self.logger.error("Docker SDK not installed")
                return False

            # Initialize Docker client
            base_url = self.config.get("base_url", "unix://var/run/docker.sock")
            self.client = docker.DockerClient(base_url=base_url)

            # Test connection
            self.client.ping()
            self.logger.info("Docker connection established")
            return True

        except Exception as e:
            self.logger.error(f"Docker initialization error: {e}")
            return False

    async def _health_check(self) -> Dict[str, Any]:
        """Health check for Docker"""
        try:
            if not self.client:
                return {"status": "unhealthy", "reason": "Client not initialized"}

            # Test Docker connection
            self.client.ping()

            # Get system info
            info = self.client.info()

            return {
                "status": "healthy",
                "version": info.get("ServerVersion"),
                "containers_running": info.get("ContainersRunning", 0),
                "containers_total": info.get("Containers", 0),
                "images_total": info.get("Images", 0),
            }
        except Exception as e:
            return {"status": "unhealthy", "reason": str(e)}

    async def _cleanup(self):
        """Cleanup Docker resources"""
        if self.client:
            self.client.close()
            self.client = None

    async def get_containers(self, all_containers: bool = True) -> List[Dict[str, Any]]:
        """List all containers"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            containers = self.client.containers.list(all=all_containers)
            return [
                {
                    "id": container.id,
                    "name": container.name,
                    "status": container.status,
                    "image": container.image.tags[0]
                    if container.image.tags
                    else "unknown",
                    "labels": container.labels,
                    "ports": container.ports,
                    "created": container.attrs.get("Created"),
                }
                for container in containers
            ]
        except Exception as e:
            self.logger.error(f"Error getting containers: {e}")
            raise

    async def get_container_info(self, container_id: str) -> Dict[str, Any]:
        """Get detailed container information"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            container = self.client.containers.get(container_id)
            return {
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "labels": container.labels,
                "ports": container.ports,
                "mounts": [
                    {
                        "source": mount.get("Source"),
                        "destination": mount.get("Destination"),
                        "type": mount.get("Type"),
                    }
                    for mount in container.attrs.get("Mounts", [])
                ],
                "networks": list(
                    container.attrs.get("NetworkSettings", {})
                    .get("Networks", {})
                    .keys()
                ),
                "created": container.attrs.get("Created"),
                "started_at": container.attrs.get("State", {}).get("StartedAt"),
            }
        except Exception as e:
            self.logger.error(f"Error getting container info: {e}")
            raise

    async def container_action(self, container_id: str, action: str) -> bool:
        """Perform container action (start, stop, restart, pause, unpause)"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            container = self.client.containers.get(container_id)

            if action == "start":
                container.start()
            elif action == "stop":
                container.stop()
            elif action == "restart":
                container.restart()
            elif action == "pause":
                container.pause()
            elif action == "unpause":
                container.unpause()
            elif action == "remove":
                container.remove(force=True)
            else:
                raise ValueError(f"Unknown action: {action}")

            return True
        except Exception as e:
            self.logger.error(f"Error performing container action {action}: {e}")
            raise

    async def get_container_logs(self, container_id: str, tail: int = 100) -> str:
        """Get container logs"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(tail=tail, timestamps=True)
            return logs.decode("utf-8")
        except Exception as e:
            self.logger.error(f"Error getting container logs: {e}")
            raise

    async def get_container_stats(self, container_id: str) -> Dict[str, Any]:
        """Get container resource usage statistics"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            container = self.client.containers.get(container_id)
            stats = container.stats(stream=False)

            return {
                "cpu_usage": stats.get("cpu_stats", {}),
                "memory_usage": stats.get("memory_stats", {}),
                "network_io": stats.get("networks", {}),
                "block_io": stats.get("blkio_stats", {}),
                "read": stats.get("read"),
            }
        except Exception as e:
            self.logger.error(f"Error getting container stats: {e}")
            raise

    async def get_images(self) -> List[Dict[str, Any]]:
        """List all Docker images"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            images = self.client.images.list()
            return [
                {
                    "id": image.id,
                    "tags": image.tags,
                    "size": image.attrs.get("Size"),
                    "created": image.attrs.get("Created"),
                }
                for image in images
            ]
        except Exception as e:
            self.logger.error(f"Error getting images: {e}")
            raise

    async def image_action(self, image_id: str, action: str) -> bool:
        """Perform image action (remove)"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            if action == "remove":
                self.client.images.remove(image_id, force=True)
                return True
            else:
                raise ValueError(f"Unknown action: {action}")
        except Exception as e:
            self.logger.error(f"Error performing image action {action}: {e}")
            raise

    async def get_system_info(self) -> Dict[str, Any]:
        """Get Docker system information"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            info = self.client.info()
            version = self.client.version()

            return {
                "info": info,
                "version": version,
            }
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            raise
