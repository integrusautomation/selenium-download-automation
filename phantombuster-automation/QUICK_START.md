# Quick Start Guide

Get up and running with the Phantombuster Automation Suite in minutes!

## 🚀 5-Minute Setup

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd phantombuster-automation

# Run the setup script
python setup.py
```

### 2. Configure Credentials
```bash
# Edit the configuration file
nano config.json

# Fill in your Phantombuster credentials:
{
  "selenium": {
    "email": "your-email@example.com",
    "password": "your-password"
  }
}
```

### 3. Test the Setup
```bash
# Run the test script
./test_setup.sh
```

### 4. Run Automation
```bash
# Start everything
./start_all.sh

# Or run components individually:
cd selenium-automation && python selenium_download.py
cd webhook-api && python webhook_app.py
cd downloader-scripts && python download_from_webhook.py
```

## 🎯 What You Get

### Selenium Automation
- **Automated login** to Phantombuster
- **Processes 47 agents** automatically
- **Downloads CSV files** to `result_files/`
- **Handles CAPTCHAs** and errors
- **Screenshots** for debugging

### Webhook API
- **RESTful API** at `http://localhost:5000`
- **Beautiful web interface** with results table
- **JSON endpoints** for programmatic access
- **Real-time status** updates

### Downloader Scripts
- **Multiple download options** (CLI, interactive, scripts)
- **Progress tracking** and statistics
- **Skip existing files** automatically
- **Cross-platform** support

### GitHub Actions
- **Automated scheduling** (daily at 2 AM UTC)
- **Manual triggering** from GitHub UI
- **Result management** and webhook updates
- **Error handling** and logging

## 📊 Results

After running, you'll have:

```
result_files/
├── zb3ZwQnVuZcM0cfCNbQoIQ_000000108_result.csv
├── zb3ZwQnVuZcM0cfCNbQoIQ_000000107_result.csv
├── EQl5K9ngclSt6QfdgqaWOQ_000000078_result.csv
└── ... (200+ CSV files)

debug_screenshots/
├── debug_login_page_20250911_140914.png
├── debug_agent_8626543543351129_20250911_140925.png
└── ... (debug screenshots)
```

## 🌐 Web Interface

Visit `http://localhost:5000` to see:

- **Real-time status** of automation
- **Beautiful results table** with all folders and files
- **Progress tracking** during execution
- **Error reporting** if something goes wrong
- **Manual controls** to trigger automation

## 🔧 Configuration Options

### Environment Variables
```bash
# Selenium
export PHANTOMBUSTER_EMAIL="your-email@example.com"
export PHANTOMBUSTER_PASSWORD="your-password"

# Webhook
export WEBHOOK_PORT="5000"
export WEBHOOK_DEBUG="false"

# Downloader
export DOWNLOAD_DIR="downloads"
export MAX_RETRIES="3"
```

### Configuration File
Edit `config.json`:
```json
{
  "selenium": {
    "email": "your-email@example.com",
    "password": "your-password",
    "headless": true
  },
  "webhook": {
    "port": 5000,
    "debug": false
  }
}
```

## 🚀 Deployment Options

### Local Development
```bash
# Start all services
./start_all.sh
```

### Cloud Deployment
```bash
# Deploy webhook to Heroku
cd webhook-api
python deploy_webhook.py

# Deploy to Railway
python deploy_github_webhook.py
```

### Docker
```bash
# Build and run
docker-compose up -d
```

## 📱 API Usage

### Get Results
```bash
# JSON format
curl http://localhost:5000/api/results

# HTML table
curl http://localhost:5000/results/table
```

### Trigger Automation
```bash
# Start automation
curl -X POST http://localhost:5000/trigger
```

### Check Status
```bash
# Health check
curl http://localhost:5000/api/health

# Status
curl http://localhost:5000/api/status
```

## 🔄 GitHub Integration

### Set up GitHub Actions
1. Copy workflows to `.github/workflows/`
2. Enable GitHub Actions in repository settings
3. Set up secrets if needed
4. Trigger manually or on schedule

### GitHub Webhook
1. Deploy webhook to public URL
2. Add webhook in GitHub repository settings
3. Set payload URL to your webhook endpoint
4. Configure events (push, pull request, etc.)

## 🐛 Troubleshooting

### Common Issues

**Selenium not starting:**
```bash
# Check Chrome installation
google-chrome --version

# Install ChromeDriver
pip install chromedriver-autoinstaller
```

**Webhook not accessible:**
```bash
# Check if port is available
netstat -an | grep 5000

# Try different port
export WEBHOOK_PORT="8080"
```

**Downloader not working:**
```bash
# Check webhook URL
curl http://localhost:5000/api/health

# Test download
python download_from_webhook.py http://localhost:5000
```

### Debug Mode
```bash
# Enable debug mode
export WEBHOOK_DEBUG="true"
python webhook_app.py
```

## 📚 Next Steps

1. **Read the full documentation** in `README.md`
2. **Configure advanced options** in `config.json`
3. **Set up monitoring** and alerts
4. **Deploy to production** using cloud platforms
5. **Integrate with other tools** using the API

## 🆘 Need Help?

- **Documentation**: Check the `documentation/` folder
- **Issues**: Create a GitHub issue
- **Examples**: Look in the `examples/` folder
- **Support**: Contact the maintainers

---

**🎉 You're all set! Happy automating!**
