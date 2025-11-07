# Selenium Download Automation

This repository contains an automated script that downloads CSV files from Phantombuster agents using Selenium WebDriver.

## Files

- `selenium_download.py` - Main script that automates the download process
- `requirements.txt` - Python dependencies
- `.github/workflows/selenium-download.yml` - GitHub Actions workflow
- `.gitignore` - Git ignore rules

## GitHub Actions Workflow

The workflow is configured to:

1. **Schedule**: Run daily at 2 AM UTC
2. **Manual trigger**: Can be triggered manually via GitHub Actions tab
3. **Push trigger**: Runs when `selenium_download.py` is updated

### Workflow Steps

1. Checkout code
2. Set up Python 3.9
3. Install Google Chrome and ChromeDriver
4. Install Python dependencies
5. Run the selenium download script
6. Check for new files in `result_files/`
7. Commit and push any new files

## Setup

1. Push this code to a GitHub repository
2. The workflow will automatically run on the schedule
3. Downloaded files will be committed to the `result_files/` directory

## Manual Execution

To run the workflow manually:

1. Go to the "Actions" tab in your GitHub repository
2. Select "Selenium Download Automation" workflow
3. Click "Run workflow"

## Public Trigger Endpoint

You can expose `/api/trigger-selenium` publicly. The route accepts requests without any authentication when no API key is configured on the server.

Optionally, you can set a shared secret to restrict access:

1. Set a repository secret named `SELENIUM_TRIGGER_API_KEY` and configure the same value on the server hosting `github_webhook.py`.
2. Update your GitHub Actions workflow to call the endpoint using that secret, for example:

```yaml
- name: Trigger hosted Selenium download
  run: |
    curl -X POST "https://your-public-domain/api/trigger-selenium" \
      -H "X-API-Key: ${{ secrets.SELENIUM_TRIGGER_API_KEY }}"
```

The Flask route now requires the `X-API-Key` header (or `api_key` query string) to match the server’s `SELENIUM_TRIGGER_API_KEY` environment variable before it will trigger the Selenium automation.

## Dependencies

The script requires:
- Python 3.9+
- Google Chrome browser
- ChromeDriver
- Various Python packages (listed in requirements.txt)

## Output

- CSV files are saved to `result_files/` directory
- Debug screenshots are saved to `debug_screenshots/` directory
- All new files are automatically committed to the repository
