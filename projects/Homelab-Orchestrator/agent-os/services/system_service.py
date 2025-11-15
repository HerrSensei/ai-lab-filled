#!/usr/bin/env python3
"""
Enhanced System Service for Homelab Management
Based on Agent Control Plane architecture
"""

import logging
import psutil
import platform
from datetime import datetime
from typing import Any, Dict, List, Optional
import subprocess
import asyncio

from .base_service import BaseService

logger = logging.getLogger(__name__)


class SystemService(BaseService):
    """Enhanced System Management Service"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("system")
        self.config = config or {}

    async def _initialize(self) -> bool:
        """Initialize system service"""
        try:
            # Test system access
            platform.uname()
            psutil.cpu_percent()
            self.logger.info("System service initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"System initialization error: {e}")
            return False

    async def _health_check(self) -> Dict[str, Any]:
        """Health check for system service"""
        try:
            return {
                "status": "healthy",
                "platform": platform.system(),
                "python_version": platform.python_version(),
                "uptime": self._get_uptime(),
                "load_average": psutil.getloadavg()
                if hasattr(psutil, "getloadavg")
                else None,
            }
        except Exception as e:
            return {"status": "unhealthy", "reason": str(e)}

    async def _cleanup(self):
        """Cleanup system resources"""
        pass

    def _get_uptime(self) -> str:
        """Get system uptime"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{days}d {hours}h {minutes}m"
        except Exception:
            return "Unknown"

    async def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            uname = platform.uname()
            boot_time = datetime.fromtimestamp(psutil.boot_time())

            return {
                "system": {
                    "hostname": uname.node,
                    "platform": uname.system,
                    "release": uname.release,
                    "version": uname.version,
                    "machine": uname.machine,
                    "processor": uname.processor,
                    "python_version": platform.python_version(),
                },
                "boot_time": boot_time.isoformat(),
                "uptime": self._get_uptime(),
            }
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            raise

    async def get_cpu_usage(self) -> Dict[str, Any]:
        """Get CPU usage information"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_count_physical = psutil.cpu_count(logical=False)
            cpu_freq = psutil.cpu_freq()

            return {
                "usage_percent": psutil.cpu_percent(interval=1),
                "usage_per_cpu": cpu_percent,
                "cpu_count_logical": cpu_count_logical,
                "cpu_count_physical": cpu_count_physical,
                "frequency": {
                    "current": cpu_freq.current if cpu_freq else None,
                    "min": cpu_freq.min if cpu_freq else None,
                    "max": cpu_freq.max if cpu_freq else None,
                }
                if cpu_freq
                else None,
                "load_average": psutil.getloadavg()
                if hasattr(psutil, "getloadavg")
                else None,
            }
        except Exception as e:
            self.logger.error(f"Error getting CPU usage: {e}")
            raise

    async def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            virtual_memory = psutil.virtual_memory()
            swap_memory = psutil.swap_memory()

            return {
                "virtual": {
                    "total": virtual_memory.total,
                    "available": virtual_memory.available,
                    "used": virtual_memory.used,
                    "free": virtual_memory.free,
                    "percent": virtual_memory.percent,
                    "buffers": getattr(virtual_memory, "buffers", 0),
                    "cached": getattr(virtual_memory, "cached", 0),
                },
                "swap": {
                    "total": swap_memory.total,
                    "used": swap_memory.used,
                    "free": swap_memory.free,
                    "percent": swap_memory.percent,
                },
            }
        except Exception as e:
            self.logger.error(f"Error getting memory usage: {e}")
            raise

    async def get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            net_io = psutil.net_io_counters()
            net_if_addrs = psutil.net_if_addrs()
            net_if_stats = psutil.net_if_stats()

            interfaces = {}
            for interface_name, addresses in net_if_addrs.items():
                interface_info = {
                    "addresses": [
                        {
                            "family": str(addr.family),
                            "address": addr.address,
                            "netmask": addr.netmask,
                            "broadcast": addr.broadcast,
                            "ptp": addr.ptp,
                        }
                        for addr in addresses
                    ],
                    "stats": None,
                }

                if interface_name in net_if_stats:
                    stats = net_if_stats[interface_name]
                    interface_info["stats"] = {
                        "isup": stats.isup,
                        "duplex": stats.duplex,
                        "speed": stats.speed,
                        "mtu": stats.mtu,
                    }

                interfaces[interface_name] = interface_info

            return {
                "io_counters": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv,
                    "errin": net_io.errin,
                    "errout": net_io.errout,
                    "dropin": net_io.dropin,
                    "dropout": net_io.dropout,
                },
                "interfaces": interfaces,
            }
        except Exception as e:
            self.logger.error(f"Error getting network stats: {e}")
            raise

    async def get_process_list(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get list of running processes"""
        if not self.initialized:
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
                    pass

            # Sort by CPU usage and limit
            processes.sort(key=lambda x: x.get("cpu_percent", 0), reverse=True)
            return processes[:limit]
        except Exception as e:
            self.logger.error(f"Error getting process list: {e}")
            raise

    async def execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute a system command"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True,
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )

            return {
                "command": command,
                "returncode": process.returncode,
                "stdout": stdout.decode("utf-8").strip(),
                "stderr": stderr.decode("utf-8").strip(),
                "success": process.returncode == 0,
            }
        except asyncio.TimeoutError:
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

    async def get_service_status(
        self, service_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get systemd service status"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            if service_name:
                # Get specific service status
                result = await self.execute_command(f"systemctl status {service_name}")
                return {"service": service_name, "status": result}
            else:
                # List all services
                result = await self.execute_command(
                    "systemctl list-units --type=service --all"
                )
                return {"services": result}
        except Exception as e:
            self.logger.error(f"Error getting service status: {e}")
            raise

    async def control_service(self, service_name: str, action: str) -> Dict[str, Any]:
        """Control systemd service (start, stop, restart, enable, disable)"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            if action not in ["start", "stop", "restart", "enable", "disable"]:
                raise ValueError(f"Invalid action: {action}")

            result = await self.execute_command(f"systemctl {action} {service_name}")
            return {"service": service_name, "action": action, "result": result}
        except Exception as e:
            self.logger.error(f"Error controlling service: {e}")
            raise

    async def get_disk_usage(self) -> Dict[str, Any]:
        """Get disk usage information"""
        if not self.initialized:
            raise Exception("Service not initialized")

        try:
            disk_partitions = psutil.disk_partitions()
            disk_usage = {}

            for partition in disk_partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.mountpoint] = {
                        "device": partition.device,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": (usage.used / usage.total) * 100,
                    }
                except PermissionError:
                    continue

            disk_io = psutil.disk_io_counters()

            return {
                "partitions": disk_usage,
                "io_counters": {
                    "read_count": disk_io.read_count,
                    "write_count": disk_io.write_count,
                    "read_bytes": disk_io.read_bytes,
                    "write_bytes": disk_io.write_bytes,
                    "read_time": disk_io.read_time,
                    "write_time": disk_io.write_time,
                }
                if disk_io
                else None,
            }
        except Exception as e:
            self.logger.error(f"Error getting disk usage: {e}")
            raise
