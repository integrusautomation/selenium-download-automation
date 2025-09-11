#!/bin/bash

# Phantombuster Webhook Downloader Script
# Usage: ./download_files.sh [webhook_url] [download_dir]

# Default values
WEBHOOK_URL=${1:-"http://localhost:5000"}
DOWNLOAD_DIR=${2:-"downloaded_files"}

echo "Phantombuster Webhook Downloader"
echo "================================="
echo "Webhook URL: $WEBHOOK_URL"
echo "Download directory: $DOWNLOAD_DIR"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if required Python packages are available
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required Python packages..."
    pip3 install requests
fi

# Run the downloader
echo "Starting download..."
python3 download_from_webhook.py "$WEBHOOK_URL" "$DOWNLOAD_DIR"

echo "Script completed."
