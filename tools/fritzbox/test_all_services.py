#!/usr/bin/env python3
"""
Comprehensive test of all available fritzconnection services
Tests all 41 available services to collect maximum data from Fritz!Box
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from fritzbox_api import FritzBoxAPI


async def test_all_services():
    """Test all available fritzconnection services"""

    print("🔍 Testing all available Fritz!Box services...")

    # Initialize API with environment variables
    api = FritzBoxAPI(
        host=os.getenv("FRITZBOX_HOST", "192.168.178.1"),
        user="",  # Fritz!Box doesn't use username
        password=os.getenv("FRITZBOX_PASSWORD", ""),
    )

    # Connect to router
    if not await api.connect():
        print("❌ Connection failed - cannot test services")
        return False

    # Get device info first
    device_info = await api.get_device_info()
    if not device_info:
        print("❌ Cannot get device info")
        return False

    # List of all available services to test
    services_to_test = [
        # Device Info
        "DeviceInfo1",
        "DeviceInfo2",
        "LANConfigSecurity1",
        "LANEthernetInterfaceConfig1",
        "LANHostConfigManagement1",
        "WANCommonInterfaceConfig1",
        "WANDSLInterfaceConfig1",
        "WANIPConnection1",
        "WANIPConnection2",
        "WANPPPConnection1",
        "WLANConfiguration1",
        "WLANConfiguration2",
        "WLANConfiguration3",
        "WLANConfiguration4",
        "WLANConfiguration5",
        "Layer3Forwarding1",
        "ManagementServer1",
        "Time1",
        "UserInterface1",
        "X_AVM-DE_Filelinks1",
        "X_AVM-DE_Homeauto1",
        "X_AVM-DE_MyFritz1",
        "X_AVM-DE_OnTel1",
        "X_AVM-DE_RemoteAccess1",
        "X_AVM-DE_Storage1",
        "X_AVM-DE_TAM1",
        "X_AVM-DE_UPnP1",
        "X_AVM-DE_VPN1",
        "X_AVM-DE_WANConfig1",
        "X_AVM-DE_WLANConfiguration1",
        "X_AVM-DE_WLANConfiguration2",
        "X_AVM-DE_WLANConfiguration3",
        "X_AVM-DE_WLANConfiguration4",
        "X_AVM-DE_WLANConfiguration5",
        "X_AVM-DE_Dect1",
        "X_AVM-DE_Mesh1",
        "X_AVM-DE_PushMail1",
        "X_AVM-DE_Speedtest1",
        "X_AVM-DE_Traceroute1",
    ]

    results = {
        "test_timestamp": datetime.now().isoformat(),
        "connection_info": conn_info,
        "working_services": {},
        "failed_services": {},
        "partial_services": {},
    }

    print(f"🧪 Testing {len(services_to_test)} services...")

    for service in services_to_test:
        print(f"  Testing {service}...")

        try:
            # Get service actions
            actions = api.get_service_actions(service)

            if not actions:
                results["failed_services"][service] = "No actions available"
                print("    ❌ No actions available")
                continue

            service_results = {}
            working_actions = 0
            failed_actions = 0

            # Test each action
            for action in actions:
                try:
                    action_result = api.call_service_action(service, action)
                    service_results[action] = {
                        "status": "success",
                        "data": action_result,
                    }
                    working_actions += 1

                except Exception as e:
                    service_results[action] = {"status": "failed", "error": str(e)}
                    failed_actions += 1

            # Categorize service results
            if working_actions > 0:
                if failed_actions == 0:
                    results["working_services"][service] = service_results
                    print(f"    ✅ All {working_actions} actions working")
                else:
                    results["partial_services"][service] = service_results
                    print(
                        f"    ⚠️  {working_actions}/{working_actions + failed_actions} actions working"
                    )
            else:
                results["failed_services"][service] = service_results
                print("    ❌ All actions failed")

        except Exception as e:
            results["failed_services"][service] = {"error": str(e)}
            print(f"    ❌ Service failed: {str(e)}")

    # Test specific high-value functions
    print("\n🎯 Testing high-value specific functions...")

    high_value_tests = {}

    # Test host enumeration
    try:
        hosts = api.get_host_entries()
        high_value_tests["host_entries"] = {
            "status": "success",
            "count": len(hosts) if hosts else 0,
            "data": hosts[:5] if hosts else [],  # First 5 for sample
        }
        print(f"  ✅ Host entries: {len(hosts) if hosts else 0} devices")
    except Exception as e:
        high_value_tests["host_entries"] = {"status": "failed", "error": str(e)}
        print(f"  ❌ Host entries failed: {str(e)}")

    # Test WAN info
    try:
        wan_info = api.get_wan_info()
        high_value_tests["wan_info"] = {"status": "success", "data": wan_info}
        print("  ✅ WAN info retrieved")
    except Exception as e:
        high_value_tests["wan_info"] = {"status": "failed", "error": str(e)}
        print(f"  ❌ WAN info failed: {str(e)}")

    # Test specific device info
    try:
        device_info = api.get_specific_device_info()
        high_value_tests["device_info"] = {"status": "success", "data": device_info}
        print("  ✅ Device info retrieved")
    except Exception as e:
        high_value_tests["device_info"] = {"status": "failed", "error": str(e)}
        print(f"  ❌ Device info failed: {str(e)}")

    results["high_value_tests"] = high_value_tests

    # Save comprehensive results
    output_file = Path("/data/fritzbox_comprehensive_test.json")
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n📊 Test Summary:")
    print(f"  ✅ Working services: {len(results['working_services'])}")
    print(f"  ⚠️  Partial services: {len(results['partial_services'])}")
    print(f"  ❌ Failed services: {len(results['failed_services'])}")
    print(f"  📁 Results saved to: {output_file}")

    return True


if __name__ == "__main__":
    success = test_all_services()
    sys.exit(0 if success else 1)
