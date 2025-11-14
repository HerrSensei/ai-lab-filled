#!/usr/bin/env python3
"""
Simple validation test for Homelab Agent OS Framework
Tests file structure and basic functionality without imports
"""

import os
import sys
from datetime import datetime

import yaml


def test_file_structure():
    """Test project file structure"""
    print("📁 Testing File Structure...")

    required_dirs = [
        "agent-os",
        "agent-os/core",
        "agent-os/services",
        "agent-os/api",
        "n8n-nodes",
        "deployment",
        "deployment/docker",
        "deployment/k8s",
        "config",
        "scripts",
        "docs",
        "tests",
    ]

    passed = 0
    failed = 0

    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✅ Directory exists: {dir_path}")
            passed += 1
        else:
            print(f"❌ Directory missing: {dir_path}")
            failed += 1

    required_files = [
        "README.md",
        "docker-compose.yml",
        "agent-os/core/agent_manager.py",
        "agent-os/services/gemini_integration.py",
        "agent-os/api/server.py",
        "n8n-nodes/agent_os_nodes.py",
        "deployment/docker/Dockerfile.agent-os",
        "deployment/docker/requirements.agent-os.txt",
        "deployment/k8s/deployments.yaml",
        "deployment/k8s/infrastructure.yaml",
        "scripts/setup.sh",
        "scripts/setup-gemini.sh",
        "scripts/deploy-homeserver.sh",
        "scripts/validate.sh",
        "tests/test_framework.py",
    ]

    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"✅ File exists: {file_path}")
            passed += 1
        else:
            print(f"❌ File missing: {file_path}")
            failed += 1

    return passed, failed


def test_python_syntax():
    """Test Python file syntax"""
    print("\n🐍 Testing Python Syntax...")

    python_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    passed = 0
    failed = 0

    for py_file in python_files:
        try:
            with open(py_file) as f:
                compile(f.read(), py_file, "exec")
            print(f"✅ Python syntax OK: {py_file}")
            passed += 1
        except SyntaxError as e:
            print(f"❌ Python syntax error in {py_file}: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  Could not check {py_file}: {e}")

    return passed, failed


def test_docker_compose():
    """Test Docker Compose configuration"""
    print("\n🐳 Testing Docker Compose...")

    if not os.path.isfile("docker-compose.yml"):
        print("❌ docker-compose.yml not found")
        return 0, 1

    try:
        # Try to parse YAML
        with open("docker-compose.yml") as f:
            compose_config = yaml.safe_load(f)

        # Check required services
        required_services = ["agent-os", "n8n", "redis"]
        passed = 0
        failed = 0

        if "services" in compose_config:
            for service in required_services:
                if service in compose_config["services"]:
                    print(f"✅ Service found: {service}")
                    passed += 1
                else:
                    print(f"❌ Service missing: {service}")
                    failed += 1
        else:
            print("❌ No services section in docker-compose.yml")
            failed += 1

        print("✅ docker-compose.yml syntax is valid")
        passed += 1

        return passed, failed

    except yaml.YAMLError as e:
        print(f"❌ docker-compose.yml YAML error: {e}")
        return 0, 1
    except Exception as e:
        print(f"❌ Error checking docker-compose.yml: {e}")
        return 0, 1


def test_kubernetes_yaml():
    """Test Kubernetes YAML files"""
    print("\n☸️  Testing Kubernetes YAML...")

    k8s_dir = "deployment/k8s"
    if not os.path.isdir(k8s_dir):
        print("⚠️  Kubernetes directory not found")
        return 0, 0

    yaml_files = []
    for file in os.listdir(k8s_dir):
        if file.endswith(".yaml"):
            yaml_files.append(os.path.join(k8s_dir, file))

    passed = 0
    failed = 0

    for yaml_file in yaml_files:
        try:
            with open(yaml_file) as f:
                yaml.safe_load_all(f)
            print(f"✅ Kubernetes YAML valid: {yaml_file}")
            passed += 1
        except yaml.YAMLError as e:
            print(f"❌ Kubernetes YAML error in {yaml_file}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Error checking {yaml_file}: {e}")
            failed += 1

    return passed, failed


def test_scripts_executable():
    """Test if scripts are executable"""
    print("\n🛠️  Testing Script Permissions...")

    scripts_dir = "scripts"
    if not os.path.isdir(scripts_dir):
        print("❌ Scripts directory not found")
        return 0, 1

    script_files = [
        "setup.sh",
        "setup-gemini.sh",
        "deploy-homeserver.sh",
        "validate.sh",
    ]

    passed = 0
    failed = 0

    for script in script_files:
        script_path = os.path.join(scripts_dir, script)
        if os.path.isfile(script_path):
            if os.access(script_path, os.X_OK):
                print(f"✅ Script executable: {script}")
                passed += 1
            else:
                print(f"❌ Script not executable: {script}")
                failed += 1
        else:
            print(f"❌ Script missing: {script}")
            failed += 1

    return passed, failed


def test_documentation():
    """Test documentation files"""
    print("\n📚 Testing Documentation...")

    doc_files = [
        "README.md",
        "agent-os/core/agent_manager.py",
        "agent-os/services/gemini_integration.py",
        "agent-os/api/server.py",
    ]

    passed = 0
    failed = 0

    # Check README
    if os.path.isfile("README.md"):
        with open("README.md") as f:
            readme_content = f.read()

        required_sections = ["Quick Start", "Architecture", "Features"]
        for section in required_sections:
            if section in readme_content:
                print(f"✅ README contains section: {section}")
                passed += 1
            else:
                print(f"⚠️  README missing section: {section}")

        print("✅ README.md exists")
        passed += 1
    else:
        print("❌ README.md missing")
        failed += 1

    # Check Python docstrings
    for py_file in doc_files:
        if py_file.endswith(".py") and os.path.isfile(py_file):
            with open(py_file) as f:
                content = f.read()

            if '"""' in content:
                print(f"✅ Documentation found: {py_file}")
                passed += 1
            else:
                print(f"⚠️  No documentation: {py_file}")

    return passed, failed


def main():
    """Main test runner"""
    print("🧪 Homelab Agent OS Framework - Simple Validation")
    print("=" * 60)
    print(f"Started at: {datetime.now().isoformat()}")
    print()

    total_passed = 0
    total_failed = 0

    # Run tests
    passed, failed = test_file_structure()
    total_passed += passed
    total_failed += failed

    passed, failed = test_python_syntax()
    total_passed += passed
    total_failed += failed

    passed, failed = test_docker_compose()
    total_passed += passed
    total_failed += failed

    passed, failed = test_kubernetes_yaml()
    total_passed += passed
    total_failed += failed

    passed, failed = test_scripts_executable()
    total_passed += passed
    total_failed += failed

    passed, failed = test_documentation()
    total_passed += passed
    total_failed += failed

    # Print summary
    print("\n" + "=" * 60)
    print("📊 Validation Summary:")
    print(f"✅ Passed:  {total_passed}")
    print(f"❌ Failed:  {total_failed}")

    if total_failed == 0:
        print("\n🎉 All validations passed!")
        print("✨ The Homelab Agent OS Framework is ready for deployment!")
        return 0
    else:
        print(f"\n⚠️  {total_failed} validation(s) failed - please review")
        return 1


if __name__ == "__main__":
    sys.exit(main())
