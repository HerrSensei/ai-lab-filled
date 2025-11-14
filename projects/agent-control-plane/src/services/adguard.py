#!/usr/bin/env python3
"""
AdGuard Service - DNS und Werbeblocker Management
"""

import logging
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class AdGuardService:
    """AdGuard Home Management Service"""

    def __init__(self):
        self.base_url = None
        self.session = None
        self.username = None
        self.password = None
        self.initialized = False

    async def initialize(self):
        """Initialisiere AdGuard Verbindung"""
        try:
            # TODO: Load from config
            self.base_url = "http://adguard.local:3000"
            self.username = "admin"
            self.password = "your_password"  # TODO: Load from secure config
            self.session = aiohttp.ClientSession()

            # Login und Session prüfen
            await self._login()
            self.initialized = True
            logger.info("AdGuard service initialized successfully")

        except Exception as e:
            logger.error(f"AdGuard initialization error: {e}")

    async def _login(self):
        """Login bei AdGuard"""
        try:
            login_data = {"name": self.username, "password": self.password}

            async with self.session.post(
                f"{self.base_url}/control/login", json=login_data
            ) as resp:
                if resp.status == 200:
                    # Session cookie wird automatisch gesetzt
                    return True
                else:
                    raise Exception(f"AdGuard login failed: {resp.status}")
        except Exception as e:
            logger.error(f"AdGuard login error: {e}")
            raise

    async def health_check(self) -> bool:
        """Health Check für AdGuard"""
        if not self.initialized:
            return False

        try:
            async with self.session.get(f"{self.base_url}/control/status") as resp:
                return resp.status == 200
        except:
            return False

    async def get_status(self) -> dict[str, Any]:
        """AdGuard Status"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.get(f"{self.base_url}/control/status") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    raise Exception(f"Failed to get status: {resp.status}")
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            raise

    async def get_stats(self) -> dict[str, Any]:
        """DNS Statistiken"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.get(f"{self.base_url}/control/stats") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    raise Exception(f"Failed to get stats: {resp.status}")
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            raise

    async def get_querylog(self, limit: int = 100) -> list[dict[str, Any]]:
        """DNS Query Log"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            params = {"limit": limit}
            async with self.session.get(
                f"{self.base_url}/control/querylog", params=params
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("data", [])
                else:
                    raise Exception(f"Failed to get querylog: {resp.status}")
        except Exception as e:
            logger.error(f"Error getting querylog: {e}")
            raise

    async def add_filter(self, url: str, name: str = None) -> bool:
        """Filter hinzufügen"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            filter_data = {"url": url, "name": name or url}

            async with self.session.post(
                f"{self.base_url}/control/filter/add", json=filter_data
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Error adding filter: {e}")
            raise

    async def remove_filter(self, filter_id: int) -> bool:
        """Filter entfernen"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.post(
                f"{self.base_url}/control/filter/remove", json={"id": filter_id}
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Error removing filter: {e}")
            raise

    async def enable_filter(self, filter_id: int) -> bool:
        """Filter aktivieren"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.post(
                f"{self.base_url}/control/filter/enable",
                json={"id": filter_id, "enabled": True},
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Error enabling filter: {e}")
            raise

    async def disable_filter(self, filter_id: int) -> bool:
        """Filter deaktivieren"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.post(
                f"{self.base_url}/control/filter/disable",
                json={"id": filter_id, "enabled": False},
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Error disabling filter: {e}")
            raise

    async def add_whitelist_rule(self, rule: str) -> bool:
        """Whitelist Regel hinzufügen"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.post(
                f"{self.base_url}/control/whitelist/add", json={"rule": rule}
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Error adding whitelist rule: {e}")
            raise

    async def remove_whitelist_rule(self, rule: str) -> bool:
        """Whitelist Regel entfernen"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            async with self.session.post(
                f"{self.base_url}/control/whitelist/remove", json={"rule": rule}
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Error removing whitelist rule: {e}")
            raise

    async def rewrite_dns(self, domain: str, answer: str) -> bool:
        """DNS Rewrite Regel"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            rewrite_data = {"domain": domain, "answer": answer}

            async with self.session.post(
                f"{self.base_url}/control/rewrite/add", json=rewrite_data
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Error adding DNS rewrite: {e}")
            raise

    async def set_protection(self, enabled: bool) -> bool:
        """DNS Protection aktivieren/deaktivieren"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            protection_data = {"protection_enabled": enabled}

            async with self.session.post(
                f"{self.base_url}/control/protection", json=protection_data
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Error setting protection: {e}")
            raise

    async def cleanup(self):
        """Cleanup bei Shutdown"""
        if self.session:
            await self.session.close()
        logger.info("AdGuard service cleaned up")
