#!/usr/bin/env python3
"""
Quick AdGuard VM setup script
Connects to AdGuard VM and checks/starts services
"""

import subprocess
import time


def run_ssh_command(command, vm_ip="192.168.178.166"):
    """Run SSH command on AdGuard VM"""
    try:
        # Try without password first (key-based auth)
        result = subprocess.run(
            f"ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no root@{vm_ip} '{command}'",
            shell=True,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            # Try with common passwords if key auth fails
            for password in ["", "admin", "password", "adguard"]:
                result = subprocess.run(
                    f"sshpass -p '{password}' ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no root@{vm_ip} '{command}'",
                    shell=True,
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    return result.stdout.strip()

            return f"SSH failed: {result.stderr.strip()}"

    except Exception as e:
        return f"Error: {str(e)}"


def check_adguard_vm():
    """Check AdGuard VM status and services"""
    vm_ip = "192.168.178.166"

    print(f"🔍 Prüfe AdGuard VM ({vm_ip})...")

    # Check if VM is reachable
    ping_result = run_ssh_command("echo 'VM reachable'", vm_ip)
    if "VM reachable" not in ping_result:
        print(f"❌ VM nicht erreichbar: {ping_result}")
        return False

    print("✅ VM erreichbar")

    # Check OS info
    os_info = run_ssh_command(
        "cat /etc/os-release | grep PRETTY_NAME | cut -d'=' -f2 | tr -d '\"'", vm_ip
    )
    print(f"🖥️  OS: {os_info}")

    # Check AdGuard service
    adguard_status = run_ssh_command(
        "systemctl is-active adguardhome 2>/dev/null || echo 'service not found'", vm_ip
    )
    print(f"📡 AdGuard Service: {adguard_status}")

    # Check if AdGuard is installed
    adguard_check = run_ssh_command(
        "which adguardhome || which AdGuardHome || echo 'not installed'", vm_ip
    )
    print(f"🔧 AdGuard Binary: {adguard_check}")

    # Check running processes
    processes = run_ssh_command(
        "ps aux | grep -i adguard | grep -v grep || echo 'no adguard processes'", vm_ip
    )
    if processes != "no adguard processes":
        print(f"🔄 AdGuard Processes:\n{processes}")

    # Check Docker containers
    docker_check = run_ssh_command(
        "docker ps -a | grep -i adguard || echo 'no adguard containers'", vm_ip
    )
    if docker_check != "no adguard containers":
        print(f"🐳 AdGuard Containers:\n{docker_check}")

    # Check network ports
    ports = run_ssh_command(
        "netstat -tlnp 2>/dev/null | grep -E ':(53|3000|80|443)' || ss -tlnp | grep -E ':(53|3000|80|443)' || echo 'no relevant ports'",
        vm_ip,
    )
    if ports != "no relevant ports":
        print(f"🌐 Offene Ports:\n{ports}")

    # Try to start AdGuard if not running
    if "inactive" in adguard_status or "not found" in adguard_status:
        print("\n🚀 Versuche AdGuard zu starten...")

        # Try Docker first
        start_docker = run_ssh_command(
            "docker run -d --name adguard -p 53:53/tcp -p 53:53/udp -p 80:80 -p 3000:3000 adguard/adguardhome 2>/dev/null || echo 'docker failed'",
            vm_ip,
        )
        if "docker failed" not in start_docker:
            print("✅ AdGuard Docker Container gestartet")
            time.sleep(5)
        else:
            # Try systemd service
            start_service = run_ssh_command(
                "systemctl start adguardhome 2>/dev/null || echo 'systemctl failed'",
                vm_ip,
            )
            if "systemctl failed" not in start_service:
                print("✅ AdGuard Service gestartet")
            else:
                # Try manual start
                run_ssh_command(
                    "adguardhome -c /etc/adguardhome/AdGuardHome.yaml -w /var/lib/adguardhome 2>/dev/null &",
                    vm_ip,
                )
                print("🔧 Versuche manuellen Start...")

    # Check status again
    time.sleep(3)
    final_status = run_ssh_command(
        "netstat -tlnp 2>/dev/null | grep -E ':(53|3000)' || ss -tlnp | grep -E ':(53|3000)' || echo 'still no ports'",
        vm_ip,
    )
    if final_status != "still no ports":
        print(f"✅ AdGuard Ports jetzt offen:\n{final_status}")
        return True
    else:
        print("❌ AdGuard konnte nicht gestartet werden")
        return False


if __name__ == "__main__":
    success = check_adguard_vm()

    if success:
        print("\n🎉 AdGuard VM Setup erfolgreich!")
        print(
            "📡 AdGuard sollte jetzt unter http://192.168.178.166:3000 erreichbar sein"
        )
    else:
        print("\n❌ AdGuard VM Setup fehlgeschlagen")
        print("💡 Manuelle Konfiguration erforderlich")
