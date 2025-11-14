#!/usr/bin/env python3
"""
System Service - System Commands und Monitoring
"""

import logging
import subprocess
from datetime import datetime
from typing import Any
import asyncio

import psutil

from ...core.base_service import BaseAgentService

logger = logging.getLogger(__name__)


class SystemService(BaseAgentService):
    """System Management Service"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self._is_initialized = False

    async def initialize(self):
        """Initialisiere System Service"""
        try:
            self._is_initialized = True
            self.logger.info("System service initialized successfully")

        except Exception as e:
            self.logger.error(f"System initialization error: {e}")
            raise

    async def health_check(self) -> bool:
        """Health Check für System Service"""
        return self._is_initialized

    async def run(self) -> None:
        """Run the main logic of the service. For SystemService, this is a no-op as it's primarily reactive."""
        self.logger.info("System service is running in reactive mode.")
        while True:
            await asyncio.sleep(self.config.get("check_interval", 60)) # Keep alive and allow for checks
            # No active tasks for SystemService, it responds to requests
            pass

    async def get_system_info(self) -> dict[str, Any]:
        """System Informationen"""
        if not self._is_initialized:
            raise Exception("Service not initialized")

        try:
            info = {
                "hostname": psutil.os.uname().nodename,
                "platform": psutil.os.uname().sysname,
                "release": psutil.os.uname().release,
                "version": psutil.os.uname().version,
                "machine": psutil.os.uname().machine,
                "uptime": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                "cpu_count": psutil.cpu_count(),
                "cpu_count_logical": psutil.cpu_count(logical=True),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "disk_usage": {},
            }

            # Disk usage für alle Mountpoints
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    info["disk_usage"][partition.mountpoint] = {
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": (usage.used / usage.total) * 100,
                    }
                except:
                    continue

            return info
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            raise

    async def get_cpu_usage(self) -> dict[str, Any]:
        """CPU Auslastung"""
        if not self._is_initialized:
            raise Exception("Service not initialized")

        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_freq = psutil.cpu_freq()

            return {
                "cpu_percent_per_core": cpu_percent,
                "cpu_percent_total": sum(cpu_percent) / len(cpu_percent),
                "cpu_freq_current": cpu_freq.current if cpu_freq else None,
                "cpu_freq_min": cpu_freq.min if cpu_freq else None,
                "cpu_freq_max": cpu_freq.max if cpu_freq else None,
                "load_avg": (
                    list(psutil.getloadavg()) if hasattr(psutil, "getloadavg") else None
                ),
            }
        except Exception as e:
            self.logger.error(f"Error getting CPU usage: {e}")
            raise

    async def get_memory_usage(self) -> dict[str, Any]:
        """Memory Auslastung"""
        if not self._is_initialized:
            raise Exception("Service not initialized")

        try:
            virtual = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                "virtual": {
                    "total": virtual.total,
                    "available": virtual.available,
                    "used": virtual.used,
                    "free": virtual.free,
                    "percent": virtual.percent,
                },
                "swap": {
                    "total": swap.total,
                    "used": swap.used,
                    "free": swap.free,
                    "percent": swap.percent,
                },
            }
        except Exception as e:
            self.logger.error(f"Error getting memory usage: {e}")
            raise

    async def get_network_stats(self) -> dict[str, Any]:
        """Network Statistiken"""
        if not self._is_initialized:
            raise Exception("Service not initialized")

        try:
            net_io = psutil.net_io_counters(pernic=True)
            net_if_addrs = psutil.net_if_addrs()
            net_if_stats = psutil.net_if_stats()

            result = {}
            for interface, stats in net_io.items():
                result[interface] = {
                    "bytes_sent": stats.bytes_sent,
                    "bytes_recv": stats.bytes_recv,
                    "packets_sent": stats.packets_sent,
                    "packets_recv": stats.packets_recv,
                    "errin": stats.errin,
                    "errout": stats.errout,
                    "dropin": stats.dropin,
                    "dropout": stats.dropout,
                    "addresses": net_if_addrs.get(interface, []),
                    "isup": (
                        net_if_stats.get(interface).isup
                        if net_if_stats.get(interface)
                        else None
                    ),
                    "speed": (
                        net_if_stats.get(interface).speed
                        if net_if_stats.get(interface)
                        else None
                    ),
                    "mtu": (
                        net_if_stats.get(interface).mtu
                        if net_if_stats.get(interface)
                        else None
                    ),
                }

            return result
        except Exception as e:
            self.logger.error(f"Error getting network stats: {e}")
            raise

    async def get_process_list(self) -> list[dict[str, Any]]:
        """Prozessliste"""
        if not self._is_initialized:
            raise Exception("Service not initialized")

        try:
            processes = []
            for proc in psutil.process_iter(
                ["pid", "name", "username", "cpu_percent", "memory_percent", "status"]
            ):
                try:
                    processes.append(proc.info)
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    continue

            return processes
        except Exception as e:
            self.logger.error(f"Error getting process list: {e}")
            raise

    async def execute_command(self, command: str, timeout: int = 30) -> dict[str, Any]:
        """System Kommando ausführen"""
        if not self._is_initialized:
            raise Exception("Service not initialized")

        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=timeout
            )

            return {
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {
                "command": command,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "success": False,
            }
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            raise

    async def get_service_status(self, service_name: str) -> dict[str, Any]:
        """Service Status (systemd)"""
        if not self._is_initialized:
            raise Exception("Service not initialized")

        try:
            result = await self.execute_command(f"systemctl status {service_name}")

            # Parse systemctl output
            status_info = {
                "service": service_name,
                "active": "active" in result["stdout"],
                "enabled": "enabled" in result["stdout"],
                "loaded": "loaded" in result["stdout"],
                "raw_output": result["stdout"],
            }

            return status_info
        except Exception as e:
            self.logger.error(f"Error getting service status: {e}")
            raise

    async def control_service(self, service_name: str, action: str) -> bool:
        """Service steuern (start, stop, restart, reload)"""
        if not self._is_initialized:
            raise Exception("Service not initialized")

        if action not in ["start", "stop", "restart", "reload", "enable", "disable"]:
            raise ValueError(f"Invalid action: {action}")

        try:
            result = await self.execute_command(f"systemctl {action} {service_name}")
            return result["success"]
        except Exception as e:
            self.logger.error(f"Error controlling service: {e}")
            raise

    async def get_disk_usage(self, path: str = "/") -> dict[str, Any]:
        """Disk Usage für spezifischen Pfad"""
        if not self._is_initialized:
            raise Exception("Service not initialized")

        try:
            usage = psutil.disk_usage(path)
            return {
                "path": path,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": (usage.used / usage.total) * 100,
            }
        except Exception as e:
            self.logger.error(f"Error getting disk usage: {e}")
            raise

    async def cleanup(self):
        """Cleanup bei Shutdown"""
        self.logger.info("System service cleaned up")
