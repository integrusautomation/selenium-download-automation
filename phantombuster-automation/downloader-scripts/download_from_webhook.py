#!/usr/bin/env python3
"""
Simple script to download CSV files from webhook results
Usage: python download_from_webhook.py [webhook_url] [download_dir]
"""

import sys
import requests
import os
import json
import time
from datetime import datetime

def download_from_webhook(webhook_url="http://localhost:5000", download_dir="downloaded_files"):
    """
    Download CSV files from webhook results
    
    Args:
        webhook_url (str): Base URL of the webhook API
        download_dir (str): Directory to save downloaded files
    """
    
    # Clean up URL
    webhook_url = webhook_url.rstrip('/')
    
    # Create download directory
    os.makedirs(download_dir, exist_ok=True)
    
    print(f"Fetching results from {webhook_url}/results...")
    
    try:
        # Fetch results from webhook
        response = requests.get(f"{webhook_url}/results", timeout=30)
        response.raise_for_status()
        data = response.json()
        
        print(f"✓ Found {data['total_folders']} folders with {data['total_files']} files")
        
        results = data.get('results', {})
        if not results:
            print("No results found to download")
            return
        
        # Download statistics
        total_files = 0
        successful_downloads = 0
        failed_downloads = 0
        skipped_files = 0
        
        start_time = datetime.now()
        
        # Process each folder
        for folder_name, file_ids in results.items():
            if not file_ids:
                print(f"Skipping {folder_name} (no files)")
                continue
            
            print(f"\nProcessing {folder_name} ({len(file_ids)} files)...")
            
            for file_id in file_ids:
                total_files += 1
                
                # Check if file already exists
                filename = f"{folder_name}_{file_id}_result.csv"
                filepath = os.path.join(download_dir, filename)
                
                if os.path.exists(filepath):
                    print(f"  Skipping {filename} (already exists)")
                    skipped_files += 1
                    continue
                
                # Build download URL
                folder_name_clean = folder_name.rstrip('/')
                download_url = f"https://cache1.phantombooster.com/URYtknGfxvU/{folder_name_clean}/{file_id}/result.csv"
                
                # Download file
                try:
                    print(f"  Downloading {filename}...")
                    file_response = requests.get(download_url, timeout=30)
                    file_response.raise_for_status()
                    
                    # Save file
                    with open(filepath, 'wb') as f:
                        f.write(file_response.content)
                    
                    file_size = os.path.getsize(filepath)
                    print(f"  ✓ Downloaded {filename} ({file_size} bytes)")
                    successful_downloads += 1
                    
                except requests.exceptions.RequestException as e:
                    print(f"  ✗ Failed to download {filename}: {e}")
                    failed_downloads += 1
        
        # Print statistics
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "="*50)
        print("DOWNLOAD COMPLETE")
        print("="*50)
        print(f"Total files processed: {total_files}")
        print(f"Successful downloads: {successful_downloads}")
        print(f"Failed downloads: {failed_downloads}")
        print(f"Skipped files: {skipped_files}")
        print(f"Duration: {duration:.2f} seconds")
        
        if total_files > 0:
            success_rate = (successful_downloads / total_files) * 100
            print(f"Success rate: {success_rate:.1f}%")
        
        print(f"Files saved to: {os.path.abspath(download_dir)}")
        print("="*50)
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to webhook: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"Error parsing webhook response: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main function"""
    # Parse command line arguments
    webhook_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    download_dir = sys.argv[2] if len(sys.argv) > 2 else "downloaded_files"
    
    print("Phantombuster Webhook Downloader")
    print("="*40)
    print(f"Webhook URL: {webhook_url}")
    print(f"Download directory: {download_dir}")
    print()
    
    # Check if webhook is accessible
    try:
        health_response = requests.get(f"{webhook_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✓ Webhook is accessible")
        else:
            print("⚠ Webhook returned non-200 status")
    except requests.exceptions.RequestException:
        print("⚠ Could not connect to webhook (will try anyway)")
    
    # Download files
    success = download_from_webhook(webhook_url, download_dir)
    
    if success:
        print("\nDownload completed successfully!")
    else:
        print("\nDownload failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
