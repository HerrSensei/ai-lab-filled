#!/usr/bin/env python3
"""
Service Base Class for Homelab Management
Inspired by Agent Control Plane architecture
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """Base class for all homelab services"""

    def __init__(self, name: str):
        self.name = name
        self.initialized = False
        self.logger = logging.getLogger(f"service.{name}")

    async def initialize(self) -> bool:
        """Initialize the service"""
        try:
            self.logger.info(f"Initializing {self.name} service...")
            success = await self._initialize()
            self.initialized = success
            if success:
                self.logger.info(f"{self.name} service initialized successfully")
            else:
                self.logger.error(f"{self.name} service initialization failed")
            return success
        except Exception as e:
            self.logger.error(f"Error initializing {self.name} service: {e}")
            self.initialized = False
            return False

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check for the service"""
        if not self.initialized:
            return {
                "service": self.name,
                "status": "unhealthy",
                "reason": "Service not initialized",
            }

        try:
            health = await self._health_check()
            health["service"] = self.name
            return health
        except Exception as e:
            self.logger.error(f"Health check failed for {self.name}: {e}")
            return {"service": self.name, "status": "unhealthy", "reason": str(e)}

    async def cleanup(self):
        """Cleanup service resources"""
        try:
            self.logger.info(f"Cleaning up {self.name} service...")
            await self._cleanup()
            self.initialized = False
            self.logger.info(f"{self.name} service cleaned up successfully")
        except Exception as e:
            self.logger.error(f"Error cleaning up {self.name} service: {e}")

    @abstractmethod
    async def _initialize(self) -> bool:
        """Service-specific initialization logic"""
        pass

    @abstractmethod
    async def _health_check(self) -> Dict[str, Any]:
        """Service-specific health check logic"""
        pass

    @abstractmethod
    async def _cleanup(self):
        """Service-specific cleanup logic"""
        pass


class ServiceManager:
    """Manages multiple homelab services"""

    def __init__(self):
        self.services: Dict[str, BaseService] = {}
        self.logger = logging.getLogger("service_manager")

    def register_service(self, service: BaseService):
        """Register a service"""
        self.services[service.name] = service
        self.logger.info(f"Registered service: {service.name}")

    async def initialize_all(self) -> Dict[str, bool]:
        """Initialize all registered services"""
        results = {}
        tasks = []

        for name, service in self.services.items():
            task = asyncio.create_task(service.initialize())
            tasks.append((name, task))

        for name, task in tasks:
            try:
                results[name] = await task
            except Exception as e:
                self.logger.error(f"Failed to initialize {name}: {e}")
                results[name] = False

        return results

    async def health_check_all(self) -> Dict[str, Dict[str, Any]]:
        """Perform health check on all services"""
        results = {}
        tasks = []

        for name, service in self.services.items():
            task = asyncio.create_task(service.health_check())
            tasks.append((name, task))

        for name, task in tasks:
            try:
                results[name] = await task
            except Exception as e:
                self.logger.error(f"Health check failed for {name}: {e}")
                results[name] = {
                    "service": name,
                    "status": "unhealthy",
                    "reason": str(e),
                }

        return results

    async def cleanup_all(self):
        """Cleanup all services"""
        tasks = []

        for name, service in self.services.items():
            task = asyncio.create_task(service.cleanup())
            tasks.append((name, task))

        for name, task in tasks:
            try:
                await task
            except Exception as e:
                self.logger.error(f"Failed to cleanup {name}: {e}")

    def get_service(self, name: str) -> Optional[BaseService]:
        """Get a specific service by name"""
        return self.services.get(name)

    def list_services(self) -> list[str]:
        """List all registered service names"""
        return list(self.services.keys())
