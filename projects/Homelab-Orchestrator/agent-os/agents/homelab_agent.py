"""
Homelab Management Agent
Provides comprehensive homelab infrastructure management via SSH and CLI tools
"""

import asyncio
import logging
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from pathlib import Path
import yaml


# Mock imports for now - these would need to be installed
try:
    import paramiko
except ImportError:
    paramiko = None

try:
    import aiohttp
except ImportError:
    aiohttp = None

try:
    import docker
except ImportError:
    docker = None


@dataclass
class SSHConfig:
    """SSH connection configuration"""

    host: str
    username: str
    port: int = 22
    password: Optional[str] = None
    key_file: Optional[str] = None
    timeout: int = 30


@dataclass
class ServiceConfig:
    """Service configuration"""

    name: str
    type: str  # docker, systemd, custom
    check_command: str
    start_command: str
    stop_command: str
    restart_command: str
    status_command: str
    health_check_url: Optional[str] = None


@dataclass
class BackupConfig:
    """Backup configuration"""

    name: str
    source_path: str
    destination_path: str
    schedule: str  # cron format
    retention_days: int = 30
    compression: bool = True
    exclude_patterns: List[str] = field(default_factory=list)


class HomelabManager:
    """Core homelab management functionality"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.ssh_clients: Dict[str, Any] = {}  # paramiko.SSHClient
        self.docker_client = None

        # Initialize configurations
        self.ssh_configs = {
            name: SSHConfig(**cfg) for name, cfg in config.get("ssh_hosts", {}).items()
        }
        self.services = {
            name: ServiceConfig(**cfg)
            for name, cfg in config.get("services", {}).items()
        }
        self.backups = {
            name: BackupConfig(**cfg) for name, cfg in config.get("backups", {}).items()
        }

        # Initialize Docker client if configured
        if config.get("docker_enabled", False) and docker:
            try:
                self.docker_client = docker.from_env()
                self.logger.info("Docker client initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize Docker client: {e}")

    async def get_system_stats(self, host: str) -> Dict[str, Any]:
        """Get system statistics from a host"""
        try:
            if not paramiko:
                return {
                    "host": host,
                    "status": "error",
                    "error": "paramiko not available",
                }

            ssh_client = await self._get_ssh_client(host)

            # Get CPU usage
            cpu_cmd = "top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1"
            cpu_result = await self._execute_ssh_command(ssh_client, cpu_cmd)
            cpu_usage = float(cpu_result.strip()) if cpu_result.strip() else 0.0

            # Get memory usage
            mem_cmd = "free | grep Mem | awk '{printf \"%.2f\", $3/$2 * 100.0}'"
            mem_result = await self._execute_ssh_command(ssh_client, mem_cmd)
            memory_usage = float(mem_result.strip()) if mem_result.strip() else 0.0

            # Get disk usage
            disk_cmd = "df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1"
            disk_result = await self._execute_ssh_command(ssh_client, disk_cmd)
            disk_usage = float(disk_result.strip()) if disk_result.strip() else 0.0

            # Get uptime
            uptime_cmd = "uptime -p"
            uptime_result = await self._execute_ssh_command(ssh_client, uptime_cmd)

            # Get load average
            load_cmd = "uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | cut -d',' -f1"
            load_result = await self._execute_ssh_command(ssh_client, load_cmd)
            load_avg = float(load_result.strip()) if load_result.strip() else 0.0

            return {
                "host": host,
                "timestamp": datetime.now().isoformat(),
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "disk_usage": disk_usage,
                "uptime": uptime_result.strip(),
                "load_average": load_avg,
                "status": "healthy"
                if cpu_usage < 80 and memory_usage < 80 and disk_usage < 80
                else "warning",
            }

        except Exception as e:
            self.logger.error(f"Failed to get system stats from {host}: {e}")
            return {
                "host": host,
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e),
            }

    async def check_service_status(self, service_name: str) -> Dict[str, Any]:
        """Check status of a specific service"""
        try:
            if service_name not in self.services:
                return {
                    "service": service_name,
                    "status": "not_found",
                    "error": "Service not configured",
                }

            service = self.services[service_name]

            if service.type == "docker":
                return await self._check_docker_service(service)
            elif service.type == "systemd":
                return await self._check_systemd_service(service)
            else:
                return await self._check_custom_service(service)

        except Exception as e:
            self.logger.error(f"Failed to check service {service_name}: {e}")
            return {"service": service_name, "status": "error", "error": str(e)}

    async def control_service(self, service_name: str, action: str) -> Dict[str, Any]:
        """Control a service (start, stop, restart)"""
        try:
            if service_name not in self.services:
                return {
                    "service": service_name,
                    "status": "not_found",
                    "error": "Service not configured",
                }

            service = self.services[service_name]

            if action == "start":
                command = service.start_command
            elif action == "stop":
                command = service.stop_command
            elif action == "restart":
                command = service.restart_command
            else:
                return {
                    "service": service_name,
                    "status": "error",
                    "error": f"Invalid action: {action}",
                }

            if service.type == "docker":
                return await self._control_docker_service(service, action)
            elif service.type == "systemd":
                return await self._control_systemd_service(service, action)
            else:
                return await self._execute_custom_command(service, command)

        except Exception as e:
            self.logger.error(f"Failed to control service {service_name}: {e}")
            return {"service": service_name, "status": "error", "error": str(e)}

    async def create_backup(self, backup_name: str) -> Dict[str, Any]:
        """Create a backup"""
        try:
            if backup_name not in self.backups:
                return {
                    "backup": backup_name,
                    "status": "not_found",
                    "error": "Backup not configured",
                }

            backup = self.backups[backup_name]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{backup.name}_{timestamp}.tar.gz"

            # Create backup command
            cmd_parts = ["tar", "-czf", f"{backup.destination_path}/{backup_file}"]

            # Add exclude patterns
            if backup.exclude_patterns:
                for pattern in backup.exclude_patterns:
                    cmd_parts.extend(["--exclude", pattern])

            # Add source path
            cmd_parts.append(backup.source_path)

            # Execute backup
            result = subprocess.run(cmd_parts, capture_output=True, text=True)

            if result.returncode == 0:
                # Clean old backups
                await self._cleanup_old_backups(backup)

                return {
                    "backup": backup_name,
                    "status": "success",
                    "file": backup_file,
                    "size": Path(f"{backup.destination_path}/{backup_file}")
                    .stat()
                    .st_size,
                    "timestamp": datetime.now().isoformat(),
                }
            else:
                return {
                    "backup": backup_name,
                    "status": "error",
                    "error": result.stderr,
                }

        except Exception as e:
            self.logger.error(f"Failed to create backup {backup_name}: {e}")
            return {"backup": backup_name, "status": "error", "error": str(e)}

    async def check_updates(self, host: str) -> Dict[str, Any]:
        """Check for system updates"""
        try:
            if not paramiko:
                return {
                    "host": host,
                    "status": "error",
                    "error": "paramiko not available",
                }

            ssh_client = await self._get_ssh_client(host)

            # Check for package updates (Ubuntu/Debian)
            update_cmd = "apt list --upgradable 2>/dev/null | grep -v 'WARNING' | wc -l"
            result = await self._execute_ssh_command(ssh_client, update_cmd)
            updates_count = int(result.strip()) if result.strip() else 0

            # Check for Docker updates
            docker_updates = []
            if self.docker_client:
                try:
                    for image in self.docker_client.images.list():
                        if image.attrs and image.attrs.get("RepoTags"):
                            repo_tag = image.attrs["RepoTags"][0]
                            if ":latest" in repo_tag:
                                docker_updates.append(repo_tag)
                except Exception as e:
                    self.logger.warning(f"Failed to check Docker updates: {e}")

            return {
                "host": host,
                "timestamp": datetime.now().isoformat(),
                "system_updates": updates_count,
                "docker_updates": docker_updates,
                "status": "up_to_date"
                if updates_count == 0 and not docker_updates
                else "updates_available",
            }

        except Exception as e:
            self.logger.error(f"Failed to check updates on {host}: {e}")
            return {"host": host, "status": "error", "error": str(e)}

    async def _get_ssh_client(self, host: str) -> Any:  # paramiko.SSHClient
        """Get or create SSH client for host"""
        if host not in self.ssh_clients:
            ssh_config = self.ssh_configs.get(host)
            if not ssh_config:
                raise ValueError(f"No SSH configuration found for host: {host}")

            if not paramiko:
                raise ImportError("paramiko is not available")

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if ssh_config.key_file:
                client.connect(
                    hostname=ssh_config.host,
                    port=ssh_config.port,
                    username=ssh_config.username,
                    key_filename=ssh_config.key_file,
                    timeout=ssh_config.timeout,
                )
            else:
                client.connect(
                    hostname=ssh_config.host,
                    port=ssh_config.port,
                    username=ssh_config.username,
                    password=ssh_config.password,
                    timeout=ssh_config.timeout,
                )

            self.ssh_clients[host] = client

        return self.ssh_clients[host]

    async def _execute_ssh_command(
        self, ssh_client: Any, command: str
    ) -> str:  # paramiko.SSHClient
        """Execute SSH command and return output"""
        stdin, stdout, stderr = ssh_client.exec_command(command)
        return stdout.read().decode().strip()

    async def _check_docker_service(self, service: ServiceConfig) -> Dict[str, Any]:
        """Check Docker service status"""
        try:
            if not self.docker_client:
                return {
                    "service": service.name,
                    "status": "error",
                    "error": "Docker client not available",
                }

            container = self.docker_client.containers.get(service.name)
            status = container.status.lower() if container.status else "unknown"

            # Additional health check if URL configured
            health_status = None
            if service.health_check_url and aiohttp:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            service.health_check_url, timeout=5
                        ) as response:
                            health_status = (
                                "healthy" if response.status == 200 else "unhealthy"
                            )
                except:
                    health_status = "unhealthy"

            return {
                "service": service.name,
                "type": "docker",
                "status": status,
                "health": health_status,
                "container_id": container.id[:12] if container.id else "unknown",
                "image": container.image.tags[0]
                if container.image and container.image.tags
                else "unknown",
            }

        except Exception as e:
            if hasattr(e, "response") and e.response.status_code == 404:
                return {
                    "service": service.name,
                    "type": "docker",
                    "status": "not_found",
                }
            return {
                "service": service.name,
                "type": "docker",
                "status": "error",
                "error": str(e),
            }

    async def _check_systemd_service(self, service: ServiceConfig) -> Dict[str, Any]:
        """Check systemd service status"""
        try:
            # This would need SSH implementation for remote hosts
            # For now, return placeholder
            return {
                "service": service.name,
                "type": "systemd",
                "status": "unknown",
                "note": "SSH implementation needed",
            }
        except Exception as e:
            return {
                "service": service.name,
                "type": "systemd",
                "status": "error",
                "error": str(e),
            }

    async def _check_custom_service(self, service: ServiceConfig) -> Dict[str, Any]:
        """Check custom service status"""
        try:
            result = subprocess.run(
                service.check_command, shell=True, capture_output=True, text=True
            )
            return {
                "service": service.name,
                "type": "custom",
                "status": "running" if result.returncode == 0 else "stopped",
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if result.stderr else None,
            }
        except Exception as e:
            return {
                "service": service.name,
                "type": "custom",
                "status": "error",
                "error": str(e),
            }

    async def _control_docker_service(
        self, service: ServiceConfig, action: str
    ) -> Dict[str, Any]:
        """Control Docker service"""
        try:
            if not self.docker_client:
                return {
                    "service": service.name,
                    "status": "error",
                    "error": "Docker client not available",
                }

            container = self.docker_client.containers.get(service.name)

            if action == "start":
                container.start()
            elif action == "stop":
                container.stop()
            elif action == "restart":
                container.restart()

            return {"service": service.name, "action": action, "status": "success"}

        except Exception as e:
            return {
                "service": service.name,
                "action": action,
                "status": "error",
                "error": str(e),
            }

    async def _control_systemd_service(
        self, service: ServiceConfig, action: str
    ) -> Dict[str, Any]:
        """Control systemd service"""
        # Placeholder for systemd control
        return {
            "service": service.name,
            "action": action,
            "status": "not_implemented",
            "note": "SSH implementation needed",
        }

    async def _execute_custom_command(
        self, service: ServiceConfig, command: str
    ) -> Dict[str, Any]:
        """Execute custom service command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                "service": service.name,
                "command": command,
                "status": "success" if result.returncode == 0 else "error",
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if result.stderr else None,
            }
        except Exception as e:
            return {
                "service": service.name,
                "command": command,
                "status": "error",
                "error": str(e),
            }

    async def _cleanup_old_backups(self, backup: BackupConfig):
        """Clean up old backup files"""
        try:
            cutoff_date = datetime.now() - timedelta(days=backup.retention_days)
            backup_path = Path(backup.destination_path)

            for backup_file in backup_path.glob(f"{backup.name}_*.tar.gz"):
                if backup_file.stat().st_mtime < cutoff_date.timestamp():
                    backup_file.unlink()
                    self.logger.info(f"Deleted old backup: {backup_file}")

        except Exception as e:
            self.logger.error(f"Failed to cleanup old backups: {e}")

    def cleanup(self):
        """Cleanup resources"""
        for client in self.ssh_clients.values():
            if hasattr(client, "close"):
                client.close()
        self.ssh_clients.clear()


class HomelabAgent:
    """Homelab Management Agent implementation"""

    def __init__(self, agent_config: Dict[str, Any]):
        self.config = agent_config
        self.manager = HomelabManager(agent_config)
        self.logger = logging.getLogger(f"{__name__}.homelab_agent")
        self.running = False

    async def start(self):
        """Start the homelab agent"""
        self.logger.info(f"Starting Homelab Agent")
        self.running = True

        try:
            while self.running:
                # Perform monitoring checks
                await self._perform_monitoring_checks()

                # Sleep until next check
                await asyncio.sleep(
                    self.config.get("check_interval", 300)
                )  # 5 minutes default

        except asyncio.CancelledError:
            self.logger.info(f"Homelab Agent cancelled")
        except Exception as e:
            self.logger.error(f"Homelab Agent error: {e}")
        finally:
            self.manager.cleanup()

    async def stop(self):
        """Stop the homelab agent"""
        self.logger.info(f"Stopping Homelab Agent")
        self.running = False

    async def _perform_monitoring_checks(self):
        """Perform regular monitoring checks"""
        try:
            # Check all configured hosts
            for host in self.manager.ssh_configs.keys():
                stats = await self.manager.get_system_stats(host)
                self.logger.debug(f"System stats for {host}: {stats}")

                # Check for alerts
                if stats.get("status") == "warning":
                    await self._send_alert(f"System warning on {host}", stats)
                elif stats.get("status") == "error":
                    await self._send_alert(f"System error on {host}", stats)

            # Check all configured services
            for service_name in self.manager.services.keys():
                service_status = await self.manager.check_service_status(service_name)
                self.logger.debug(
                    f"Service status for {service_name}: {service_status}"
                )

                # Check for service alerts
                if service_status.get("status") in ["stopped", "error"]:
                    await self._send_alert(
                        f"Service issue: {service_name}", service_status
                    )

            # Check for updates (less frequently)
            if datetime.now().hour % 6 == 0:  # Every 6 hours
                for host in self.manager.ssh_configs.keys():
                    updates = await self.manager.check_updates(host)
                    if updates.get("status") == "updates_available":
                        self.logger.info(f"Updates available on {host}: {updates}")

        except Exception as e:
            self.logger.error(f"Error in monitoring checks: {e}")

    async def _send_alert(self, message: str, data: Dict[str, Any]):
        """Send alert notification"""
        # Placeholder for alert implementation
        self.logger.warning(f"ALERT: {message} - {data}")

        # Could integrate with:
        # - Email notifications
        # - Slack/Telegram bots
        # - Push notifications
        # - SMS alerts

    async def handle_command(
        self, command: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle agent commands"""
        try:
            if command == "get_stats":
                host = params.get("host")
                if not host:
                    return {"error": "Host parameter required"}
                return await self.manager.get_system_stats(host)

            elif command == "check_service":
                service_name = params.get("service")
                if not service_name:
                    return {"error": "Service parameter required"}
                return await self.manager.check_service_status(service_name)

            elif command == "control_service":
                service_name = params.get("service")
                action = params.get("action")
                if not service_name or not action:
                    return {"error": "Service and action parameters required"}
                return await self.manager.control_service(service_name, action)

            elif command == "create_backup":
                backup_name = params.get("backup")
                if not backup_name:
                    return {"error": "Backup parameter required"}
                return await self.manager.create_backup(backup_name)

            elif command == "check_updates":
                host = params.get("host")
                if not host:
                    return {"error": "Host parameter required"}
                return await self.manager.check_updates(host)

            else:
                return {"error": f"Unknown command: {command}"}

        except Exception as e:
            self.logger.error(f"Error handling command {command}: {e}")
            return {"error": str(e)}
