# Phantombuster Automation Suite

A comprehensive automation system for downloading CSV files from Phantombuster agents using Selenium WebDriver, with a webhook API and downloader scripts.

## 🚀 Overview

This project provides a complete solution for automating Phantombuster data collection:

1. **Selenium Automation** - Automated web scraping to collect agent results
2. **Webhook API** - RESTful API to serve collected data
3. **Downloader Scripts** - Tools to download CSV files from the API
4. **GitHub Actions** - Automated scheduling and deployment

## 📁 Project Structure

```
phantombuster-automation/
├── README.md                           # This file
├── INSTALLATION.md                     # Installation guide
├── QUICK_START.md                      # Quick start guide
├── CONFIGURATION.md                    # Configuration options
├── TROUBLESHOOTING.md                  # Troubleshooting guide
├── selenium-automation/                # Selenium automation scripts
│   ├── selenium_download.py            # Main automation script
│   ├── requirements.txt                # Python dependencies
│   └── README.md                       # Selenium documentation
├── webhook-api/                        # Webhook API service
│   ├── webhook_app.py                  # Flask webhook application
│   ├── update_webhook_results.py       # Results update script
│   ├── deploy_webhook.py               # Deployment helper
│   ├── webhook_requirements.txt        # API dependencies
│   └── README.md                       # Webhook documentation
├── downloader-scripts/                 # Downloader utilities
│   ├── webhook_downloader.py           # Full-featured downloader
│   ├── download_from_webhook.py        # Simple command-line downloader
│   ├── download_files.sh               # Unix/Linux shell script
│   ├── download_files.bat              # Windows batch script
│   └── README.md                       # Downloader documentation
├── github-actions/                     # GitHub Actions workflows
│   ├── selenium-download.yml           # Main automation workflow
│   └── README.md                       # CI/CD documentation
├── documentation/                      # Additional documentation
│   ├── API_REFERENCE.md                # Complete API reference
│   ├── DEPLOYMENT_GUIDE.md             # Deployment instructions
│   ├── SECURITY.md                     # Security considerations
│   └── CONTRIBUTING.md                 # Contribution guidelines
├── examples/                           # Usage examples
│   ├── basic_usage.py                  # Basic usage examples
│   ├── advanced_integration.py         # Advanced integration
│   ├── docker/                         # Docker examples
│   └── cloud-deployment/               # Cloud deployment examples
└── tests/                              # Test suite
    ├── test_selenium.py                # Selenium tests
    ├── test_webhook.py                 # Webhook tests
    └── test_downloader.py              # Downloader tests
```

## 🎯 Features

### Selenium Automation
- ✅ Automated login and navigation
- ✅ CAPTCHA handling and solving
- ✅ Multi-agent processing
- ✅ Screenshot capture for debugging
- ✅ Error handling and retry logic
- ✅ Headless browser support

### Webhook API
- ✅ RESTful API endpoints
- ✅ JSON and HTML data formats
- ✅ Summary statistics
- ✅ Health monitoring
- ✅ Auto-updating results
- ✅ CORS support

### Downloader Scripts
- ✅ Multiple download options
- ✅ Progress tracking
- ✅ Skip existing files
- ✅ Error handling
- ✅ Cross-platform support
- ✅ Detailed statistics

### GitHub Actions
- ✅ Automated scheduling
- ✅ Manual triggering
- ✅ Chrome and ChromeDriver setup
- ✅ Result file management
- ✅ Webhook updates

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd phantombuster-automation
```

### 2. Install Dependencies
```bash
# Install selenium automation dependencies
pip install -r selenium-automation/requirements.txt

# Install webhook API dependencies
pip install -r webhook-api/webhook_requirements.txt
```

### 3. Configure
```bash
# Copy and edit configuration
cp examples/config.example.json config.json
# Edit config.json with your settings
```

### 4. Run Selenium Automation
```bash
cd selenium-automation
python selenium_download.py
```

### 5. Start Webhook API
```bash
cd webhook-api
python webhook_app.py
```

### 6. Download Files
```bash
cd downloader-scripts
python download_from_webhook.py
```

## 📖 Documentation

- [Installation Guide](INSTALLATION.md) - Detailed installation instructions
- [Quick Start Guide](QUICK_START.md) - Get up and running quickly
- [Configuration Guide](CONFIGURATION.md) - Configuration options
- [API Reference](documentation/API_REFERENCE.md) - Complete API documentation
- [Deployment Guide](documentation/DEPLOYMENT_GUIDE.md) - Deployment instructions
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions

## 🔧 Configuration

### Environment Variables
```bash
# Selenium Configuration
export PHANTOMBUSTER_EMAIL="your-email@example.com"
export PHANTOMBUSTER_PASSWORD="your-password"
export CHROME_BIN="/usr/bin/google-chrome"
export CHROMEDRIVER="/usr/local/bin/chromedriver"

# Webhook Configuration
export WEBHOOK_HOST="0.0.0.0"
export WEBHOOK_PORT="5000"
export WEBHOOK_DEBUG="false"

# Downloader Configuration
export DOWNLOAD_DIR="downloads"
export MAX_RETRIES="3"
export TIMEOUT="30"
```

### Configuration File
```json
{
  "selenium": {
    "email": "your-email@example.com",
    "password": "your-password",
    "headless": true,
    "screenshot_dir": "screenshots"
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

## 🚀 Deployment

### Local Development
```bash
# Start all services
./scripts/start_all.sh

# Or start individually
./scripts/start_selenium.sh
./scripts/start_webhook.sh
./scripts/start_downloader.sh
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Cloud Deployment
- **Heroku**: See [Heroku Deployment](documentation/DEPLOYMENT_GUIDE.md#heroku)
- **Railway**: See [Railway Deployment](documentation/DEPLOYMENT_GUIDE.md#railway)
- **AWS**: See [AWS Deployment](documentation/DEPLOYMENT_GUIDE.md#aws)
- **Google Cloud**: See [GCP Deployment](documentation/DEPLOYMENT_GUIDE.md#gcp)

## 🔒 Security

- Credentials are stored securely
- HTTPS support for webhook API
- Input validation and sanitization
- Rate limiting and error handling
- Secure file handling

See [Security Guide](documentation/SECURITY.md) for detailed security considerations.

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test suites
python -m pytest tests/test_selenium.py
python -m pytest tests/test_webhook.py
python -m pytest tests/test_downloader.py
```

## 📊 Monitoring

### Health Checks
- Selenium automation status
- Webhook API health
- Download success rates
- Error logging and alerts

### Metrics
- Total files processed
- Download success rates
- Processing times
- Error frequencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [Contributing Guide](documentation/CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the documentation folder
- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub discussions
- **Email**: Contact the maintainers

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Selenium automation
- Webhook API
- Downloader scripts
- GitHub Actions integration
- Comprehensive documentation

## 🙏 Acknowledgments

- Phantombuster for the automation platform
- Selenium WebDriver for browser automation
- Flask for the webhook API
- GitHub Actions for CI/CD
- All contributors and users

---

**Made with ❤️ for automation enthusiasts**
