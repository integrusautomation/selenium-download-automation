# Selenium Automation

Automated web scraping using Selenium WebDriver to collect CSV files from Phantombuster agents.

## Files

- `selenium_download.py` - Main automation script
- `requirements.txt` - Python dependencies
- `README.md` - This documentation

## Features

- ✅ Automated login and navigation
- ✅ CAPTCHA handling and solving
- ✅ Multi-agent processing (47 agents)
- ✅ Screenshot capture for debugging
- ✅ Error handling and retry logic
- ✅ Headless browser support
- ✅ Chrome and ChromeDriver auto-installation

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run automation
python selenium_download.py
```

## Configuration

Set environment variables:

```bash
export PHANTOMBUSTER_EMAIL="your-email@example.com"
export PHANTOMBUSTER_PASSWORD="your-password"
export CHROME_BIN="/usr/bin/google-chrome"
export CHROMEDRIVER="/usr/local/bin/chromedriver"
```

## Output

- **CSV files**: Saved to `result_files/` directory
- **Screenshots**: Saved to `debug_screenshots/` directory
- **Logs**: Detailed console output

## GitHub Actions

The script is designed to run in GitHub Actions with:
- Chrome and ChromeDriver setup
- Headless browser configuration
- Result file management
- Webhook updates

See the main README for complete documentation.
