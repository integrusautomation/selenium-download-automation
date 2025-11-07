# Phantombuster Complete Automation

This script provides a complete automation solution that:
1. Triggers the Heroku webhook to start GitHub Actions
2. Waits for the selenium automation to complete
3. Downloads the results using Git clone (no API rate limits)
4. Optionally cleans up the repository

## Usage Examples

### Basic Usage (Recommended)
```bash
python3 phantombuster_automation.py
```
This will:
- Trigger the webhook
- Wait for automation to complete (30 min timeout)
- Wait 10 minutes for files to be committed
- Download files to `./phantombuster_files`

### Quick Test (No Wait)
```bash
python3 phantombuster_automation.py --no-wait --no-file-wait
```
This will:
- Trigger the webhook
- Immediately try to download files (may fail if automation hasn't completed)

### Download Only (Skip Webhook)
```bash
python3 phantombuster_automation.py --download-only
```
This will:
- Skip webhook trigger
- Just download existing files from repository

### Custom Output Directory
```bash
python3 phantombuster_automation.py --output ./my_files
```

### With GitHub Token (for private repos)
```bash
python3 phantombuster_automation.py --token YOUR_GITHUB_TOKEN
```

### Clear Repository After Download
```bash
python3 phantombuster_automation.py --clear-after
```
This will:
- Run full automation
- Download files
- Clear the `result_files` directory from the repository
- Push the cleanup changes

## Configuration

The script uses these default settings:
- **Webhook URL**: `https://phantombuster-webhook-72a87a1e67bb.herokuapp.com`
- **GitHub Repo**: `chughjug/selenium-download-automation`
- **Output Directory**: `./phantombuster_files`
- **Timeout**: 30 minutes
- **File Wait**: 10 minutes

## How It Works

1. **Trigger**: Sends POST request to webhook `/trigger` endpoint
2. **Monitor**: Polls webhook `/api/status` every 30 seconds
3. **Wait**: Waits for GitHub Actions to commit files to repository
4. **Download**: Uses `git clone` to download files (no rate limits)
5. **Cleanup**: Optionally clears repository and pushes changes

## Error Handling

- Webhook connection failures
- Automation timeouts
- Git clone failures
- File not found errors
- Repository cleanup failures

The script provides clear error messages and suggestions for each failure mode.


