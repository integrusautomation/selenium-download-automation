# Installation Guide

This guide will help you install and set up the Phantombuster Automation Suite.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 1GB free space minimum
- **Internet**: Stable internet connection

### Required Software
- Python 3.8+
- pip (Python package manager)
- Git
- Google Chrome browser
- ChromeDriver (automatically installed)

## 🚀 Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd phantombuster-automation

# Run the installation script
chmod +x scripts/install.sh
./scripts/install.sh
```

### Method 2: Manual Install

#### Step 1: Clone Repository
```bash
git clone <your-repo-url>
cd phantombuster-automation
```

#### Step 2: Install Python Dependencies

**Selenium Automation:**
```bash
cd selenium-automation
pip install -r requirements.txt
```

**Webhook API:**
```bash
cd webhook-api
pip install -r webhook_requirements.txt
```

**Downloader Scripts:**
```bash
cd downloader-scripts
pip install requests
```

#### Step 3: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip git wget unzip
sudo apt-get install -y google-chrome-stable
```

**macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python3 git wget
brew install --cask google-chrome
```

**Windows:**
```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install dependencies
choco install python3 git wget googlechrome
```

#### Step 4: Install ChromeDriver

**Automatic (Recommended):**
```bash
# The selenium script will auto-install ChromeDriver
cd selenium-automation
python selenium_download.py
```

**Manual:**
```bash
# Download ChromeDriver
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d "." -f1)

# Download and install
wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}/chromedriver_linux64.zip"
sudo unzip /tmp/chromedriver.zip -d /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

### Method 3: Docker Install

```bash
# Build Docker image
docker build -t phantombuster-automation .

# Run with Docker Compose
docker-compose up -d
```

## 🔧 Configuration

### Step 1: Create Configuration File
```bash
cp examples/config.example.json config.json
```

### Step 2: Edit Configuration
```json
{
  "selenium": {
    "email": "your-email@example.com",
    "password": "your-password",
    "headless": true,
    "screenshot_dir": "screenshots",
    "download_dir": "result_files"
  },
  "webhook": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false
  },
  "downloader": {
    "download_dir": "downloads",
    "max_retries": 3,
    "timeout": 30,
    "skip_existing": true
  }
}
```

### Step 3: Set Environment Variables
```bash
# Create .env file
cat > .env << EOF
PHANTOMBUSTER_EMAIL=your-email@example.com
PHANTOMBUSTER_PASSWORD=your-password
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=5000
DOWNLOAD_DIR=downloads
EOF
```

## ✅ Verification

### Test Selenium Installation
```bash
cd selenium-automation
python -c "from selenium import webdriver; print('Selenium installed successfully')"
```

### Test Webhook Installation
```bash
cd webhook-api
python -c "import flask; print('Flask installed successfully')"
```

### Test Downloader Installation
```bash
cd downloader-scripts
python -c "import requests; print('Requests installed successfully')"
```

### Test Chrome Installation
```bash
google-chrome --version
```

### Test ChromeDriver Installation
```bash
chromedriver --version
```

## 🐛 Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Check Python installation
python3 --version

# If not found, install Python
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# macOS
brew install python3

# Windows
# Download from python.org
```

#### Permission Denied
```bash
# Fix permissions
chmod +x scripts/*.sh
sudo chmod +x /usr/local/bin/chromedriver
```

#### Chrome Not Found
```bash
# Check Chrome installation
which google-chrome

# If not found, install Chrome
# Ubuntu/Debian
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install -y google-chrome-stable
```

#### ChromeDriver Version Mismatch
```bash
# Check Chrome version
google-chrome --version

# Check ChromeDriver version
chromedriver --version

# If versions don't match, reinstall ChromeDriver
```

#### Module Not Found
```bash
# Install missing modules
pip install selenium flask requests

# Or install from requirements
pip install -r selenium-automation/requirements.txt
pip install -r webhook-api/webhook_requirements.txt
```

### Getting Help

1. **Check Logs**: Look at error messages in the console
2. **Verify Dependencies**: Ensure all required software is installed
3. **Check Permissions**: Ensure proper file permissions
4. **Update Software**: Make sure you have the latest versions
5. **Check Documentation**: Review the troubleshooting guide

## 🔄 Updates

### Update the Project
```bash
git pull origin main
pip install -r selenium-automation/requirements.txt
pip install -r webhook-api/webhook_requirements.txt
```

### Update Dependencies
```bash
pip install --upgrade selenium flask requests
```

### Update ChromeDriver
```bash
# The selenium script will auto-update ChromeDriver
cd selenium-automation
python selenium_download.py
```

## 🧹 Uninstallation

### Remove Project Files
```bash
rm -rf phantombuster-automation
```

### Remove Dependencies (Optional)
```bash
pip uninstall selenium flask requests
```

### Remove ChromeDriver (Optional)
```bash
sudo rm /usr/local/bin/chromedriver
```

## 📞 Support

If you encounter issues during installation:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review the [FAQ](documentation/FAQ.md)
3. Create a [GitHub Issue](https://github.com/your-repo/issues)
4. Contact the maintainers

---

**Next Steps**: After installation, see the [Quick Start Guide](QUICK_START.md) to begin using the system.
