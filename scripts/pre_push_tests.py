#!/usr/bin/env python3
"""
AI Lab Framework - Pre-Push Test Runner

Führt umfassende Tests vor jedem git push durch.
Blockt Push bei Test-Fehlern.

Usage:
    python scripts/pre_push_tests.py
    python scripts/pre_push_tests.py --fast
    python scripts/pre_push_tests.py --coverage
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class PrePushTestRunner:
    """Runs comprehensive tests before git push."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()
        self.results = {}
        self.start_time = time.time()

    def run_all_tests(self, fast_mode: bool = False, coverage: bool = True) -> bool:
        """Run all pre-push tests."""
        print("🚀 Running pre-push tests...")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        success = True

        # 1. Code Quality Checks
        if not self._run_code_quality_tests():
            success = False

        # 2. Unit Tests
        if not self._run_unit_tests(coverage):
            success = False

        # 3. Integration Tests (skip in fast mode)
        if not fast_mode and not self._run_integration_tests():
            success = False

        # 4. Security Tests
        if not self._run_security_tests():
            success = False

        # 5. Performance Tests (skip in fast mode)
        if not fast_mode and not self._run_performance_tests():
            success = False

        # 6. Database Tests
        if not self._run_database_tests():
            success = False

        # Generate report
        self._generate_test_report()

        duration = time.time() - self.start_time
        print("=" * 60)
        if success:
            print(f"✅ All tests passed! ({duration:.1f}s)")
            print("🚀 Ready to push!")
        else:
            print(f"❌ Some tests failed! ({duration:.1f}s)")
            print("🛑 Fix issues before pushing.")
            print("\n💡 Run with --fast for quicker checks")

        return success

    def _run_code_quality_tests(self) -> bool:
        """Run code quality checks."""
        print("\n📋 Running Code Quality Tests...")
        print("-" * 40)

        success = True

        # Black formatting
        print("🎨 Checking code formatting with Black...")
        try:
            result = subprocess.run(
                ["black", "--check", "--diff", "."],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                print("✅ Black formatting: PASSED")
                self.results["black"] = {"status": "PASSED", "duration": 0}
            else:
                print("❌ Black formatting: FAILED")
                print("Diff:")
                print(result.stdout)
                self.results["black"] = {
                    "status": "FAILED",
                    "duration": 0,
                    "output": result.stdout,
                }
                success = False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  Black not available or timed out")
            self.results["black"] = {"status": "SKIPPED", "duration": 0}

        # Ruff linting
        print("\n🔍 Running Ruff linter...")
        try:
            start_time = time.time()
            result = subprocess.run(
                ["ruff", "check", "."], capture_output=True, text=True, timeout=120
            )
            duration = time.time() - start_time

            if result.returncode == 0:
                print("✅ Ruff linting: PASSED")
                self.results["ruff"] = {"status": "PASSED", "duration": duration}
            else:
                print("❌ Ruff linting: FAILED")
                issues = result.stdout.strip().split("\n")
                print(f"Found {len([i for i in issues if i])} issues:")
                for issue in issues[:10]:  # Show first 10 issues
                    if issue:
                        print(f"  • {issue}")
                if len(issues) > 10:
                    print(f"  ... and {len(issues) - 10} more")
                self.results["ruff"] = {
                    "status": "FAILED",
                    "duration": duration,
                    "issues": len(issues),
                }
                success = False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  Ruff not available or timed out")
            self.results["ruff"] = {"status": "SKIPPED", "duration": 0}

        # MyPy type checking
        print("\n🔬 Running MyPy type checking...")
        try:
            start_time = time.time()
            result = subprocess.run(
                ["mypy", "src/", "--ignore-missing-imports"],
                capture_output=True,
                text=True,
                timeout=180,
            )
            duration = time.time() - start_time

            if result.returncode == 0:
                print("✅ MyPy type checking: PASSED")
                self.results["mypy"] = {"status": "PASSED", "duration": duration}
            else:
                print("❌ MyPy type checking: FAILED")
                print("Type errors:")
                print(result.stdout)
                self.results["mypy"] = {
                    "status": "FAILED",
                    "duration": duration,
                    "errors": result.stdout,
                }
                success = False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  MyPy not available or timed out")
            self.results["mypy"] = {"status": "SKIPPED", "duration": 0}

        return success

    def _run_unit_tests(self, coverage: bool = True) -> bool:
        """Run unit tests with coverage."""
        print("\n🧪 Running Unit Tests...")
        print("-" * 40)

        try:
            start_time = time.time()

            if coverage:
                print("📊 Running with coverage...")
                cmd = [
                    "pytest",
                    "tests/unit/",
                    "--cov=src",
                    "--cov-report=term-missing",
                    "--cov-report=html",
                    "--cov-fail-under=80",
                    "-v",
                ]
            else:
                print("⚡ Running without coverage...")
                cmd = ["pytest", "tests/unit/", "-v"]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            duration = time.time() - start_time

            if result.returncode == 0:
                print("✅ Unit tests: PASSED")
                self.results["unit_tests"] = {"status": "PASSED", "duration": duration}
                return True
            else:
                print("❌ Unit tests: FAILED")
                print("Test output:")
                print(result.stdout)
                if result.stderr:
                    print("Errors:")
                    print(result.stderr)

                self.results["unit_tests"] = {
                    "status": "FAILED",
                    "duration": duration,
                    "output": result.stdout,
                    "errors": result.stderr,
                }
                return False

        except subprocess.TimeoutExpired:
            print("❌ Unit tests: TIMEOUT")
            self.results["unit_tests"] = {"status": "TIMEOUT", "duration": 300}
            return False
        except FileNotFoundError:
            print("⚠️  pytest not available")
            self.results["unit_tests"] = {"status": "SKIPPED", "duration": 0}
            return True  # Don't block push if pytest not available

    def _run_integration_tests(self) -> bool:
        """Run integration tests."""
        print("\n🔗 Running Integration Tests...")
        print("-" * 40)

        try:
            start_time = time.time()
            result = subprocess.run(
                ["pytest", "tests/integration/", "-v"],
                capture_output=True,
                text=True,
                timeout=600,
            )
            duration = time.time() - start_time

            if result.returncode == 0:
                print("✅ Integration tests: PASSED")
                self.results["integration_tests"] = {
                    "status": "PASSED",
                    "duration": duration,
                }
                return True
            else:
                print("❌ Integration tests: FAILED")
                print("Test output:")
                print(result.stdout)

                self.results["integration_tests"] = {
                    "status": "FAILED",
                    "duration": duration,
                    "output": result.stdout,
                }
                return False

        except subprocess.TimeoutExpired:
            print("❌ Integration tests: TIMEOUT")
            self.results["integration_tests"] = {"status": "TIMEOUT", "duration": 600}
            return False
        except FileNotFoundError:
            print("⚠️  Integration tests not found")
            self.results["integration_tests"] = {"status": "SKIPPED", "duration": 0}
            return True

    def _run_security_tests(self) -> bool:
        """Run security tests."""
        print("\n🔒 Running Security Tests...")
        print("-" * 40)

        success = True

        # Bandit security scan
        print("🛡️  Running Bandit security scan...")
        try:
            start_time = time.time()
            result = subprocess.run(
                ["bandit", "-r", "src/", "-f", "json"],
                capture_output=True,
                text=True,
                timeout=120,
            )
            duration = time.time() - start_time

            if result.returncode == 0:
                print("✅ Bandit security scan: PASSED")
                self.results["bandit"] = {"status": "PASSED", "duration": duration}
            else:
                print("⚠️  Bandit found security issues")
                try:
                    bandit_output = json.loads(result.stdout)
                    issues = bandit_output.get("results", [])
                    high_issues = [
                        i for i in issues if i.get("issue_severity") == "HIGH"
                    ]
                    medium_issues = [
                        i for i in issues if i.get("issue_severity") == "MEDIUM"
                    ]

                    if high_issues:
                        print(f"❌ {len(high_issues)} HIGH severity issues found")
                        success = False
                    else:
                        print("✅ No HIGH severity issues")

                    if medium_issues:
                        print(f"⚠️  {len(medium_issues)} MEDIUM severity issues found")

                    self.results["bandit"] = {
                        "status": "FAILED" if high_issues else "PASSED",
                        "duration": duration,
                        "high_issues": len(high_issues),
                        "medium_issues": len(medium_issues),
                    }
                except json.JSONDecodeError:
                    print("⚠️  Could not parse Bandit output")
                    self.results["bandit"] = {"status": "ERROR", "duration": duration}

        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  Bandit not available or timed out")
            self.results["bandit"] = {"status": "SKIPPED", "duration": 0}

        # Safety dependency check
        print("\n📦 Checking dependencies with Safety...")
        try:
            start_time = time.time()
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            duration = time.time() - start_time

            if result.returncode == 0:
                print("✅ Safety check: PASSED")
                self.results["safety"] = {"status": "PASSED", "duration": duration}
            else:
                print("⚠️  Safety found vulnerable dependencies")
                try:
                    safety_output = json.loads(result.stdout)
                    vulnerabilities = safety_output.get("vulnerabilities", [])
                    print(f"Found {len(vulnerabilities)} vulnerabilities")

                    self.results["safety"] = {
                        "status": "FAILED",
                        "duration": duration,
                        "vulnerabilities": len(vulnerabilities),
                    }
                except json.JSONDecodeError:
                    print("⚠️  Could not parse Safety output")
                    self.results["safety"] = {"status": "ERROR", "duration": duration}

        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  Safety not available or timed out")
            self.results["safety"] = {"status": "SKIPPED", "duration": 0}

        return success

    def _run_performance_tests(self) -> bool:
        """Run performance tests."""
        print("\n⚡ Running Performance Tests...")
        print("-" * 40)

        try:
            start_time = time.time()
            result = subprocess.run(
                ["pytest", "tests/performance/", "-v", "--benchmark-only"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            duration = time.time() - start_time

            if result.returncode == 0:
                print("✅ Performance tests: PASSED")
                self.results["performance_tests"] = {
                    "status": "PASSED",
                    "duration": duration,
                }
                return True
            else:
                print("❌ Performance tests: FAILED")
                print("Test output:")
                print(result.stdout)

                self.results["performance_tests"] = {
                    "status": "FAILED",
                    "duration": duration,
                    "output": result.stdout,
                }
                return False

        except subprocess.TimeoutExpired:
            print("❌ Performance tests: TIMEOUT")
            self.results["performance_tests"] = {"status": "TIMEOUT", "duration": 300}
            return False
        except FileNotFoundError:
            print("⚠️  Performance tests not found")
            self.results["performance_tests"] = {"status": "SKIPPED", "duration": 0}
            return True

    def _run_database_tests(self) -> bool:
        """Run database tests."""
        print("\n🗄️  Running Database Tests...")
        print("-" * 40)

        try:
            start_time = time.time()
            result = subprocess.run(
                ["pytest", "tests/database/", "-v"],
                capture_output=True,
                text=True,
                timeout=180,
            )
            duration = time.time() - start_time

            if result.returncode == 0:
                print("✅ Database tests: PASSED")
                self.results["database_tests"] = {
                    "status": "PASSED",
                    "duration": duration,
                }
                return True
            else:
                print("❌ Database tests: FAILED")
                print("Test output:")
                print(result.stdout)

                self.results["database_tests"] = {
                    "status": "FAILED",
                    "duration": duration,
                    "output": result.stdout,
                }
                return False

        except subprocess.TimeoutExpired:
            print("❌ Database tests: TIMEOUT")
            self.results["database_tests"] = {"status": "TIMEOUT", "duration": 180}
            return False
        except FileNotFoundError:
            print("⚠️  Database tests not found")
            self.results["database_tests"] = {"status": "SKIPPED", "duration": 0}
            return True

    def _generate_test_report(self):
        """Generate test report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "duration": time.time() - self.start_time,
            "results": self.results,
            "summary": self._generate_summary(),
        }

        # Save report
        report_dir = self.base_dir / "ai-logs" / "test-reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        report_file = (
            report_dir / f"pre-push-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        )
        report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False))

        # Print summary
        print(f"\n📊 Test Report saved to: {report_file}")

        summary = report["summary"]
        print(f"\n📈 Summary:")
        print(f"  Total tests: {summary['total']}")
        print(f"  Passed: {summary['passed']}")
        print(f"  Failed: {summary['failed']}")
        print(f"  Skipped: {summary['skipped']}")
        print(f"  Duration: {summary['duration']:.1f}s")

    def _generate_summary(self) -> Dict:
        """Generate test summary."""
        total = len(self.results)
        passed = len([r for r in self.results.values() if r["status"] == "PASSED"])
        failed = len(
            [
                r
                for r in self.results.values()
                if r["status"] in ["FAILED", "TIMEOUT", "ERROR"]
            ]
        )
        skipped = len([r for r in self.results.values() if r["status"] == "SKIPPED"])

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration": time.time() - self.start_time,
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run pre-push tests")

    parser.add_argument(
        "--fast",
        action="store_true",
        help="Run fast tests only (skip integration and performance)",
    )
    parser.add_argument(
        "--no-coverage", action="store_true", help="Skip coverage reporting"
    )
    parser.add_argument(
        "--base-dir", type=Path, help="Base directory (default: current)"
    )

    args = parser.parse_args()

    runner = PrePushTestRunner(args.base_dir)
    success = runner.run_all_tests(args.fast, not args.no_coverage)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
