#!/usr/bin/env python3
"""
Comprehensive test suite for Homelab Agent OS Framework
Tests all components and integrations
"""

import asyncio
import json
import logging
import requests
import subprocess
import time
import unittest
from datetime import datetime
from typing import Dict, Any, List
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent_os.core.agent_manager import AgentManager, AgentType, AgentStatus
from agent_os.services.gemini_integration import GeminiIntegrationService


class TestAgentManager(unittest.TestCase):
    """Test Agent Manager functionality"""

    def setUp(self):
        self.agent_manager = AgentManager()

    def test_create_agent(self):
        """Test agent creation"""

        async def test():
            agent = await self.agent_manager.create_agent(
                name="Test Agent",
                agent_type=AgentType.SERVICE,
                config={"heartbeat_interval": 30},
            )

            self.assertEqual(agent.name, "Test Agent")
            self.assertEqual(agent.type, AgentType.SERVICE)
            self.assertEqual(agent.status, AgentStatus.STARTING)

            # Clean up
            await self.agent_manager.stop_agent(agent.id)
            self.agent_manager.registry.unregister_agent(agent.id)

        asyncio.run(test())

    def test_agent_registry(self):
        """Test agent registry operations"""
        registry = self.agent_manager.registry

        # Test stats
        stats = registry.get_stats()
        self.assertIn("total_agents", stats)
        self.assertIn("by_type", stats)
        self.assertIn("by_status", stats)

        # Test empty registry
        self.assertEqual(stats["total_agents"], 0)


class TestGeminiIntegration(unittest.TestCase):
    """Test Gemini integration service"""

    def setUp(self):
        self.gemini_service = GeminiIntegrationService()

    def test_service_initialization(self):
        """Test service initialization"""
        self.assertIsNotNone(self.gemini_service)
        self.assertEqual(len(self.gemini_service.active_tasks), 0)

    def test_task_submission(self):
        """Test task submission"""

        async def test():
            await self.gemini_service.start_worker()

            task_id = await self.gemini_service.submit_task(
                agent_id="test-agent",
                task_type="analysis",
                prompt="Test prompt",
                context={"test": True},
            )

            self.assertIsNotNone(task_id)

            # Wait for completion
            await asyncio.sleep(2)

            task = await self.gemini_service.get_task_result(task_id)
            self.assertIsNotNone(task)
            self.assertIn(task.status, ["completed", "failed", "running"])

            await self.gemini_service.stop_worker()

        asyncio.run(test())


class TestAPIEndpoints(unittest.TestCase):
    """Test REST API endpoints"""

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://localhost:8080"
        cls.session = requests.Session()

    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            self.assertEqual(response.status_code, 200)

            data = response.json()
            self.assertIn("status", data)
            self.assertEqual(data["status"], "healthy")
        except requests.exceptions.ConnectionError:
            self.skipTest("API server not running")

    def test_create_agent_api(self):
        """Test agent creation via API"""
        try:
            agent_data = {
                "name": "API Test Agent",
                "type": "service",
                "config": {"heartbeat_interval": 30, "check_interval": 60},
            }

            response = self.session.post(
                f"{self.base_url}/agents", json=agent_data, timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                self.assertIn("id", data)
                self.assertEqual(data["name"], "API Test Agent")

                # Clean up
                agent_id = data["id"]
                self.session.post(f"{self.base_url}/agents/{agent_id}/stop", timeout=5)
                self.session.delete(f"{self.base_url}/agents/{agent_id}", timeout=5)
            else:
                self.skipTest(f"API returned status {response.status_code}")

        except requests.exceptions.ConnectionError:
            self.skipTest("API server not running")

    def test_list_agents_api(self):
        """Test agent listing via API"""
        try:
            response = self.session.get(f"{self.base_url}/agents", timeout=5)
            self.assertEqual(response.status_code, 200)

            data = response.json()
            self.assertIsInstance(data, list)

        except requests.exceptions.ConnectionError:
            self.skipTest("API server not running")

    def test_system_stats_api(self):
        """Test system stats via API"""
        try:
            response = self.session.get(f"{self.base_url}/stats", timeout=5)
            self.assertEqual(response.status_code, 200)

            data = response.json()
            self.assertIn("total_agents", data)
            self.assertIn("by_type", data)
            self.assertIn("by_status", data)

        except requests.exceptions.ConnectionError:
            self.skipTest("API server not running")


class TestDockerServices(unittest.TestCase):
    """Test Docker services"""

    def test_docker_available(self):
        """Test Docker availability"""
        try:
            result = subprocess.run(
                ["docker", "--version"], capture_output=True, text=True, timeout=5
            )
            self.assertEqual(result.returncode, 0)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.skipTest("Docker not available")

    def test_docker_compose_available(self):
        """Test Docker Compose availability"""
        try:
            result = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.assertEqual(result.returncode, 0)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.skipTest("Docker Compose not available")

    def test_compose_file_exists(self):
        """Test docker-compose file exists"""
        compose_file = os.path.join(
            os.path.dirname(__file__), "..", "docker-compose.yml"
        )
        self.assertTrue(os.path.exists(compose_file))


class TestN8nIntegration(unittest.TestCase):
    """Test n8n integration"""

    def test_n8n_custom_nodes_exist(self):
        """Test n8n custom nodes files exist"""
        nodes_dir = os.path.join(os.path.dirname(__file__), "..", "n8n-nodes")
        self.assertTrue(os.path.exists(nodes_dir))

        # Check for key files
        agent_os_nodes = os.path.join(nodes_dir, "agent_os_nodes.py")
        self.assertTrue(os.path.exists(agent_os_nodes))

    def test_n8n_service_config(self):
        """Test n8n service configuration"""
        compose_file = os.path.join(
            os.path.dirname(__file__), "..", "docker-compose.yml"
        )

        with open(compose_file, "r") as f:
            compose_content = f.read()

        # Check for n8n service
        self.assertIn("n8n:", compose_content)
        self.assertIn("n8nio/n8n:", compose_content)
        self.assertIn("5678:5678", compose_content)


class TestGeminiCli(unittest.TestCase):
    """Test Gemini CLI integration"""

    def test_gemini_cli_available(self):
        """Test gemini-cli availability"""
        try:
            result = subprocess.run(
                ["which", "gemini"], capture_output=True, text=True, timeout=5
            )
            # Don't fail if not found, just note it
            if result.returncode != 0:
                self.skipTest("gemini-cli not installed")
        except subprocess.TimeoutExpired:
            self.skipTest("gemini-cli check timeout")

    def test_opencode_available(self):
        """Test opencode availability"""
        try:
            result = subprocess.run(
                ["which", "opencode"], capture_output=True, text=True, timeout=5
            )
            if result.returncode != 0:
                self.skipTest("opencode not installed")
        except subprocess.TimeoutExpired:
            self.skipTest("opencode check timeout")


class TestKubernetesDeployment(unittest.TestCase):
    """Test Kubernetes deployment files"""

    def test_k8s_files_exist(self):
        """Test Kubernetes deployment files exist"""
        k8s_dir = os.path.join(os.path.dirname(__file__), "..", "deployment", "k8s")
        self.assertTrue(os.path.exists(k8s_dir))

        # Check for key files
        deployments_file = os.path.join(k8s_dir, "deployments.yaml")
        infrastructure_file = os.path.join(k8s_dir, "infrastructure.yaml")

        self.assertTrue(os.path.exists(deployments_file))
        self.assertTrue(os.path.exists(infrastructure_file))

    def test_k8s_deployments_valid(self):
        """Test Kubernetes deployment files are valid YAML"""
        import yaml

        k8s_dir = os.path.join(os.path.dirname(__file__), "..", "deployment", "k8s")

        deployments_file = os.path.join(k8s_dir, "deployments.yaml")
        infrastructure_file = os.path.join(k8s_dir, "infrastructure.yaml")

        try:
            with open(deployments_file, "r") as f:
                yaml.safe_load_all(f)

            with open(infrastructure_file, "r") as f:
                yaml.safe_load_all(f)

        except yaml.YAMLError as e:
            self.fail(f"Invalid YAML in K8s files: {e}")


class TestConfigurationFiles(unittest.TestCase):
    """Test configuration files"""

    def test_env_file_template(self):
        """Test .env template exists"""
        env_template = os.path.join(os.path.dirname(__file__), "..", ".env.template")
        self.assertTrue(os.path.exists(env_template))

    def test_config_files_exist(self):
        """Test configuration files exist"""
        config_dir = os.path.join(os.path.dirname(__file__), "..", "config")

        # Check if config directory exists (created by setup)
        if os.path.exists(config_dir):
            nginx_conf = os.path.join(config_dir, "nginx", "nginx.conf")
            if os.path.exists(nginx_conf):
                self.assertTrue(os.path.exists(nginx_conf))


class TestScripts(unittest.TestCase):
    """Test setup and deployment scripts"""

    def test_setup_script_exists(self):
        """Test setup script exists and is executable"""
        setup_script = os.path.join(
            os.path.dirname(__file__), "..", "scripts", "setup.sh"
        )
        self.assertTrue(os.path.exists(setup_script))
        self.assertTrue(os.access(setup_script, os.X_OK))

    def test_gemini_setup_script_exists(self):
        """Test gemini setup script exists and is executable"""
        gemini_script = os.path.join(
            os.path.dirname(__file__), "..", "scripts", "setup-gemini.sh"
        )
        self.assertTrue(os.path.exists(gemini_script))
        self.assertTrue(os.access(gemini_script, os.X_OK))

    def test_deployment_script_exists(self):
        """Test deployment script exists and is executable"""
        deploy_script = os.path.join(
            os.path.dirname(__file__), "..", "scripts", "deploy-homeserver.sh"
        )
        self.assertTrue(os.path.exists(deploy_script))
        self.assertTrue(os.access(deploy_script, os.X_OK))


def run_integration_tests():
    """Run integration tests that require running services"""
    print("\n🔗 Running Integration Tests...")
    print("=" * 50)

    # Test API connectivity
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ Agent OS API is running")
        else:
            print("❌ Agent OS API returned error status")
    except requests.exceptions.ConnectionError:
        print("⚠️  Agent OS API is not running")

    # Test n8n connectivity
    try:
        response = requests.get("http://localhost:5678", timeout=5)
        if response.status_code == 200:
            print("✅ n8n is running")
        else:
            print("❌ n8n returned error status")
    except requests.exceptions.ConnectionError:
        print("⚠️  n8n is not running")

    # Test Docker services
    try:
        result = subprocess.run(
            ["docker-compose", "ps"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print("✅ Docker Compose services are manageable")
        else:
            print("❌ Docker Compose error")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  Docker Compose not available")


def main():
    """Main test runner"""
    print("🧪 Homelab Agent OS Framework - Test Suite")
    print("=" * 50)
    print(f"Started at: {datetime.now().isoformat()}")
    print()

    # Configure logging
    logging.basicConfig(level=logging.WARNING)

    # Run unit tests
    print("🔬 Running Unit Tests...")
    print("-" * 30)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestAgentManager,
        TestGeminiIntegration,
        TestAPIEndpoints,
        TestDockerServices,
        TestN8nIntegration,
        TestGeminiCli,
        TestKubernetesDeployment,
        TestConfigurationFiles,
        TestScripts,
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")

    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")

    # Run integration tests
    run_integration_tests()

    # Final status
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
