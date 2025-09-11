#!/usr/bin/env python3
"""
Phantombuster Automation Setup Script
This script helps set up the entire automation system
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🤖 PHANTOMBUSTER AUTOMATION SUITE SETUP")
    print("=" * 60)
    print()

def check_python():
    """Check Python version"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_dependencies():
    """Check system dependencies"""
    print("\n📦 Checking system dependencies...")
    
    dependencies = {
        'git': 'Git version control',
        'python3': 'Python 3 interpreter',
        'pip': 'Python package manager'
    }
    
    missing = []
    for cmd, desc in dependencies.items():
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            print(f"✅ {desc} found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {desc} not found")
            missing.append(cmd)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Please install them before continuing")
        return False
    
    return True

def install_python_packages():
    """Install Python packages"""
    print("\n📚 Installing Python packages...")
    
    packages = [
        'selenium==4.15.2',
        'flask==2.3.3',
        'requests==2.31.0',
        'chromedriver-autoinstaller==0.6.2'
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         check=True, capture_output=True)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            return False
    
    return True

def create_config():
    """Create configuration file"""
    print("\n⚙️  Creating configuration file...")
    
    config = {
        "selenium": {
            "email": "",
            "password": "",
            "headless": True,
            "screenshot_dir": "debug_screenshots",
            "download_dir": "result_files"
        },
        "webhook": {
            "host": "0.0.0.0",
            "port": 5000,
            "debug": False
        },
        "downloader": {
            "download_dir": "downloaded_files",
            "max_retries": 3,
            "timeout": 30,
            "skip_existing": True
        },
        "github": {
            "webhook_secret": "",
            "repository": ""
        }
    }
    
    config_file = "config.json"
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Created {config_file}")
    else:
        print(f"✅ {config_file} already exists")
    
    return True

def create_env_file():
    """Create environment file"""
    print("\n🌍 Creating environment file...")
    
    env_content = """# Phantombuster Automation Environment Variables
# Copy this file to .env and fill in your values

# Selenium Configuration
PHANTOMBUSTER_EMAIL=your-email@example.com
PHANTOMBUSTER_PASSWORD=your-password
CHROME_BIN=/usr/bin/google-chrome
CHROMEDRIVER=/usr/local/bin/chromedriver

# Webhook Configuration
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=5000
WEBHOOK_DEBUG=false

# Downloader Configuration
DOWNLOAD_DIR=downloaded_files
MAX_RETRIES=3
TIMEOUT=30

# GitHub Configuration (Optional)
GITHUB_WEBHOOK_SECRET=your-secret-here
GITHUB_REPOSITORY=your-username/your-repo
"""
    
    env_file = ".env.example"
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Created {env_file}")
    else:
        print(f"✅ {env_file} already exists")
    
    return True

def setup_github_actions():
    """Set up GitHub Actions workflows"""
    print("\n🔄 Setting up GitHub Actions...")
    
    workflows_dir = ".github/workflows"
    os.makedirs(workflows_dir, exist_ok=True)
    
    # Copy workflow files
    workflow_files = [
        "github-actions/selenium-download.yml",
        "github-actions/github-webhook-trigger.yml"
    ]
    
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            dest = os.path.join(workflows_dir, os.path.basename(workflow_file))
            shutil.copy2(workflow_file, dest)
            print(f"✅ Copied {workflow_file} to {dest}")
        else:
            print(f"⚠️  {workflow_file} not found")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "result_files",
        "debug_screenshots",
        "downloaded_files",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/")
    
    return True

def create_scripts():
    """Create helper scripts"""
    print("\n🔧 Creating helper scripts...")
    
    # Start all script
    start_script = """#!/bin/bash
# Start all Phantombuster automation services

echo "🚀 Starting Phantombuster Automation Suite..."

# Start webhook in background
echo "📡 Starting webhook server..."
cd webhook-api
python webhook_app.py &
WEBHOOK_PID=$!

# Wait for webhook to start
sleep 5

# Start selenium automation
echo "🤖 Starting selenium automation..."
cd ../selenium-automation
python selenium_download.py

# Stop webhook
echo "🛑 Stopping webhook server..."
kill $WEBHOOK_PID

echo "✅ All services stopped"
"""
    
    with open("start_all.sh", "w") as f:
        f.write(start_script)
    os.chmod("start_all.sh", 0o755)
    print("✅ Created start_all.sh")
    
    # Test script
    test_script = """#!/bin/bash
# Test Phantombuster automation components

echo "🧪 Testing Phantombuster Automation Suite..."

# Test Python packages
echo "Testing Python packages..."
python -c "import selenium, flask, requests; print('✅ All packages imported successfully')"

# Test webhook
echo "Testing webhook..."
cd webhook-api
python -c "from webhook_app import app; print('✅ Webhook app created successfully')"

# Test downloader
echo "Testing downloader..."
cd ../downloader-scripts
python -c "from webhook_downloader import WebhookDownloader; print('✅ Downloader created successfully')"

echo "✅ All tests passed!"
"""
    
    with open("test_setup.sh", "w") as f:
        f.write(test_script)
    os.chmod("test_setup.sh", 0o755)
    print("✅ Created test_setup.sh")
    
    return True

def print_next_steps():
    """Print next steps"""
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("1. Edit config.json with your Phantombuster credentials")
    print("2. Copy .env.example to .env and fill in your values")
    print("3. Test the setup: ./test_setup.sh")
    print("4. Run the automation: ./start_all.sh")
    print()
    print("📚 Documentation:")
    print("- README.md - Main documentation")
    print("- INSTALLATION.md - Detailed installation guide")
    print("- QUICK_START.md - Quick start guide")
    print()
    print("🔗 Quick Commands:")
    print("- Start all services: ./start_all.sh")
    print("- Test setup: ./test_setup.sh")
    print("- Run selenium: cd selenium-automation && python selenium_download.py")
    print("- Start webhook: cd webhook-api && python webhook_app.py")
    print("- Download files: cd downloader-scripts && python download_from_webhook.py")
    print()
    print("🚀 Happy automating!")

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    if not check_python():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Install packages
    if not install_python_packages():
        print("❌ Failed to install Python packages")
        sys.exit(1)
    
    # Create configuration
    create_config()
    create_env_file()
    
    # Set up GitHub Actions
    setup_github_actions()
    
    # Create directories
    create_directories()
    
    # Create helper scripts
    create_scripts()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
