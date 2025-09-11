# Downloader Scripts

Collection of scripts to download CSV files from the webhook API.

## Files

- `webhook_downloader.py` - Full-featured interactive downloader
- `download_from_webhook.py` - Simple command-line downloader
- `download_files.sh` - Unix/Linux shell script
- `download_files.bat` - Windows batch script
- `README.md` - This documentation

## Features

- ✅ Multiple download options
- ✅ Progress tracking
- ✅ Skip existing files
- ✅ Error handling
- ✅ Cross-platform support
- ✅ Detailed statistics

## Quick Start

### Simple Command Line
```bash
python download_from_webhook.py
```

### Interactive Mode
```bash
python webhook_downloader.py
```

### Shell Scripts
```bash
# Linux/macOS
./download_files.sh

# Windows
download_files.bat
```

## Usage Examples

```bash
# Download from local webhook
python download_from_webhook.py

# Download from remote webhook
python download_from_webhook.py https://your-webhook.herokuapp.com

# Download to specific directory
python download_from_webhook.py https://your-webhook.herokuapp.com my_downloads
```

## Configuration

Set environment variables:

```bash
export DOWNLOAD_DIR="downloads"
export MAX_RETRIES="3"
export TIMEOUT="30"
```

See the main README for complete documentation.
