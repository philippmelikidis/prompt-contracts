#!/usr/bin/env python3
"""
Robust development installation script for prompt-contracts.

This script ensures a reliable editable installation that works consistently
across different environments and Python versions.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def ensure_clean_installation():
    """Ensure a clean installation by removing any existing installations."""
    print("🧹 Cleaning existing installations...")

    # Uninstall existing package
    run_command([sys.executable, "-m", "pip", "uninstall", "prompt-contracts", "-y"], check=False)

    # Clean build artifacts
    for dir_name in ["build", "dist", "src/promptcontracts.egg-info"]:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}")
            shutil.rmtree(dir_name)


def install_package():
    """Install the package in editable mode."""
    print("📦 Installing package in editable mode...")

    # Method 1: Try pip install -e .
    try:
        run_command([sys.executable, "-m", "pip", "install", "-e", ".", "--force-reinstall"])
        print("✅ Editable installation successful")
        return True
    except SystemExit:
        print("❌ Method 1 failed, trying alternative...")

    # Method 2: Try with --no-build-isolation
    try:
        run_command(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-e",
                ".",
                "--no-build-isolation",
                "--force-reinstall",
            ]
        )
        print("✅ Editable installation successful (method 2)")
        return True
    except SystemExit:
        print("❌ Method 2 failed, trying alternative...")

    # Method 3: Manual PYTHONPATH setup
    try:
        src_path = os.path.abspath("src")
        if src_path not in sys.path:
            sys.path.insert(0, src_path)

        # Install dependencies first
        run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

        # Create a simple installation
        run_command([sys.executable, "-m", "pip", "install", ".", "--force-reinstall"])
        print("✅ Standard installation successful (method 3)")
        return True
    except SystemExit:
        print("❌ All methods failed")
        return False


def verify_installation():
    """Verify that the installation works correctly."""
    print("🔍 Verifying installation...")

    try:
        # Test import
        import promptcontracts

        print(f"✅ Module import successful: {promptcontracts.__version__}")

        # Test CLI
        result = run_command(
            [sys.executable, "-m", "promptcontracts.cli", "--version"], check=False
        )
        if result.returncode == 0:
            print("✅ CLI import successful")
        else:
            print("❌ CLI import failed")
            return False

        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def main():
    """Main installation process."""
    print("🚀 Starting robust development installation...")

    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    print(f"Working directory: {os.getcwd()}")

    # Ensure clean installation
    ensure_clean_installation()

    # Install package
    if not install_package():
        print("❌ Installation failed")
        sys.exit(1)

    # Verify installation
    if not verify_installation():
        print("❌ Verification failed")
        sys.exit(1)

    print("🎉 Installation completed successfully!")
    print("\nYou can now use:")
    print("  prompt-contracts --version")
    print("  prompt-contracts run --help")


if __name__ == "__main__":
    main()
