#!/usr/bin/env python3
"""
Webhook Downloader - Downloads CSV files based on webhook results
This script fetches results from the webhook API and downloads the corresponding CSV files
"""

import requests
import os
import json
import time
from datetime import datetime
from urllib.parse import urljoin

class WebhookDownloader:
    def __init__(self, webhook_url, download_dir="downloaded_files"):
        """
        Initialize the webhook downloader
        
        Args:
            webhook_url (str): Base URL of the webhook API
            download_dir (str): Directory to save downloaded files
        """
        self.webhook_url = webhook_url.rstrip('/')
        self.download_dir = download_dir
        self.session = requests.Session()
        
        # Create download directory
        os.makedirs(download_dir, exist_ok=True)
        
        # Set up session headers
        self.session.headers.update({
            'User-Agent': 'WebhookDownloader/1.0',
            'Accept': 'application/json'
        })
    
    def fetch_results(self):
        """
        Fetch results from the webhook API
        
        Returns:
            dict: Results data from webhook
        """
        try:
            print(f"Fetching results from {self.webhook_url}/results...")
            response = self.session.get(f"{self.webhook_url}/results", timeout=30)
            response.raise_for_status()
            
            data = response.json()
            print(f"✓ Successfully fetched results: {data['total_folders']} folders, {data['total_files']} files")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching results: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing JSON response: {e}")
            return None
    
    def fetch_summary(self):
        """
        Fetch summary statistics from the webhook API
        
        Returns:
            dict: Summary data from webhook
        """
        try:
            print(f"Fetching summary from {self.webhook_url}/results/summary...")
            response = self.session.get(f"{self.webhook_url}/results/summary", timeout=30)
            response.raise_for_status()
            
            data = response.json()
            print(f"✓ Summary: {data['summary']['total_folders']} folders, {data['summary']['total_files']} files")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching summary: {e}")
            return None
    
    def check_health(self):
        """
        Check if the webhook is healthy
        
        Returns:
            bool: True if healthy, False otherwise
        """
        try:
            response = self.session.get(f"{self.webhook_url}/health", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 'healthy':
                print("✓ Webhook is healthy")
                return True
            else:
                print("✗ Webhook is not healthy")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Health check failed: {e}")
            return False
    
    def build_download_url(self, folder_name, file_id):
        """
        Build the download URL for a specific file
        
        Args:
            folder_name (str): Folder name (without trailing slash)
            file_id (str): File ID
            
        Returns:
            str: Complete download URL
        """
        # Remove trailing slash if present
        folder_name = folder_name.rstrip('/')
        
        # Build the download URL using the same pattern as the selenium script
        download_url = f"https://cache1.phantombooster.com/URYtknGfxvU/{folder_name}/{file_id}/result.csv"
        return download_url
    
    def download_file(self, folder_name, file_id, retries=3):
        """
        Download a single CSV file
        
        Args:
            folder_name (str): Folder name
            file_id (str): File ID
            retries (int): Number of retry attempts
            
        Returns:
            bool: True if successful, False otherwise
        """
        download_url = self.build_download_url(folder_name, file_id)
        filename = f"{folder_name}_{file_id}_result.csv"
        filepath = os.path.join(self.download_dir, filename)
        
        for attempt in range(retries):
            try:
                print(f"  Downloading {filename} (attempt {attempt + 1}/{retries})...")
                response = self.session.get(download_url, timeout=30)
                response.raise_for_status()
                
                # Check if we got actual CSV content
                if response.headers.get('content-type', '').startswith('text/csv') or 'csv' in response.text[:100].lower():
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    file_size = os.path.getsize(filepath)
                    print(f"  ✓ Downloaded {filename} ({file_size} bytes)")
                    return True
                else:
                    print(f"  ✗ Invalid content type for {filename}")
                    return False
                    
            except requests.exceptions.RequestException as e:
                print(f"  ✗ Download failed for {filename}: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return False
        
        return False
    
    def download_all_files(self, results_data=None):
        """
        Download all files from the webhook results
        
        Args:
            results_data (dict, optional): Results data. If None, will fetch from webhook.
            
        Returns:
            dict: Download statistics
        """
        if results_data is None:
            results_data = self.fetch_results()
            if not results_data:
                return None
        
        results = results_data.get('results', {})
        if not results:
            print("✗ No results found to download")
            return None
        
        print(f"\nStarting download of {len(results)} folders...")
        
        stats = {
            'total_folders': len(results),
            'total_files': 0,
            'successful_downloads': 0,
            'failed_downloads': 0,
            'skipped_files': 0,
            'start_time': datetime.now(),
            'folder_stats': {}
        }
        
        for folder_name, file_ids in results.items():
            if not file_ids:
                print(f"  Skipping {folder_name} (no files)")
                stats['folder_stats'][folder_name] = {'total': 0, 'successful': 0, 'failed': 0}
                continue
            
            print(f"\nProcessing folder: {folder_name} ({len(file_ids)} files)")
            stats['total_files'] += len(file_ids)
            stats['folder_stats'][folder_name] = {'total': len(file_ids), 'successful': 0, 'failed': 0}
            
            for file_id in file_ids:
                # Check if file already exists
                filename = f"{folder_name}_{file_id}_result.csv"
                filepath = os.path.join(self.download_dir, filename)
                
                if os.path.exists(filepath):
                    print(f"  Skipping {filename} (already exists)")
                    stats['skipped_files'] += 1
                    continue
                
                if self.download_file(folder_name, file_id):
                    stats['successful_downloads'] += 1
                    stats['folder_stats'][folder_name]['successful'] += 1
                else:
                    stats['failed_downloads'] += 1
                    stats['folder_stats'][folder_name]['failed'] += 1
        
        stats['end_time'] = datetime.now()
        stats['duration'] = (stats['end_time'] - stats['start_time']).total_seconds()
        
        return stats
    
    def print_stats(self, stats):
        """
        Print download statistics
        
        Args:
            stats (dict): Download statistics
        """
        if not stats:
            return
        
        print("\n" + "="*60)
        print("DOWNLOAD STATISTICS")
        print("="*60)
        print(f"Total folders: {stats['total_folders']}")
        print(f"Total files: {stats['total_files']}")
        print(f"Successful downloads: {stats['successful_downloads']}")
        print(f"Failed downloads: {stats['failed_downloads']}")
        print(f"Skipped files: {stats['skipped_files']}")
        print(f"Duration: {stats['duration']:.2f} seconds")
        
        if stats['total_files'] > 0:
            success_rate = (stats['successful_downloads'] / stats['total_files']) * 100
            print(f"Success rate: {success_rate:.1f}%")
        
        print("\nFolder breakdown:")
        for folder, folder_stats in stats['folder_stats'].items():
            if folder_stats['total'] > 0:
                folder_success_rate = (folder_stats['successful'] / folder_stats['total']) * 100
                print(f"  {folder}: {folder_stats['successful']}/{folder_stats['total']} ({folder_success_rate:.1f}%)")
        
        print("="*60)
    
    def save_stats(self, stats, filename="download_stats.json"):
        """
        Save download statistics to a JSON file
        
        Args:
            stats (dict): Download statistics
            filename (str): Output filename
        """
        if not stats:
            return
        
        # Convert datetime objects to strings for JSON serialization
        stats_copy = stats.copy()
        stats_copy['start_time'] = stats_copy['start_time'].isoformat()
        stats_copy['end_time'] = stats_copy['end_time'].isoformat()
        
        filepath = os.path.join(self.download_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(stats_copy, f, indent=2)
        
        print(f"Statistics saved to: {filepath}")

def main():
    """
    Main function to run the webhook downloader
    """
    print("Phantombuster Webhook Downloader")
    print("="*40)
    
    # Configuration
    webhook_url = input("Enter webhook URL (or press Enter for localhost:5000): ").strip()
    if not webhook_url:
        webhook_url = "http://localhost:5000"
    
    download_dir = input("Enter download directory (or press Enter for 'downloaded_files'): ").strip()
    if not download_dir:
        download_dir = "downloaded_files"
    
    # Initialize downloader
    downloader = WebhookDownloader(webhook_url, download_dir)
    
    # Check webhook health
    if not downloader.check_health():
        print("Webhook is not healthy. Exiting.")
        return
    
    # Fetch summary first
    summary = downloader.fetch_summary()
    if summary:
        print(f"Latest data: {summary['summary']['total_folders']} folders, {summary['summary']['total_files']} files")
    
    # Ask user what to do
    print("\nOptions:")
    print("1. Download all files")
    print("2. Download specific folder")
    print("3. Show results only (no download)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Download all files
        stats = downloader.download_all_files()
        if stats:
            downloader.print_stats(stats)
            downloader.save_stats(stats)
    
    elif choice == "2":
        # Download specific folder
        results = downloader.fetch_results()
        if not results:
            return
        
        print("\nAvailable folders:")
        for i, folder in enumerate(results['results'].keys(), 1):
            file_count = len(results['results'][folder])
            print(f"  {i}. {folder} ({file_count} files)")
        
        try:
            folder_choice = int(input("\nEnter folder number: ")) - 1
            folder_names = list(results['results'].keys())
            if 0 <= folder_choice < len(folder_names):
                selected_folder = folder_names[folder_choice]
                folder_data = {selected_folder: results['results'][selected_folder]}
                
                # Create a modified results data structure
                modified_results = {
                    'results': folder_data,
                    'total_folders': 1,
                    'total_files': len(folder_data[selected_folder])
                }
                
                stats = downloader.download_all_files(modified_results)
                if stats:
                    downloader.print_stats(stats)
                    downloader.save_stats(stats)
            else:
                print("Invalid folder number")
        except ValueError:
            print("Invalid input")
    
    elif choice == "3":
        # Show results only
        results = downloader.fetch_results()
        if results:
            print(f"\nResults from {webhook_url}:")
            print(f"Total folders: {results['total_folders']}")
            print(f"Total files: {results['total_files']}")
            print(f"Last updated: {results['timestamp']}")
            
            print("\nFolder breakdown:")
            for folder, files in results['results'].items():
                print(f"  {folder}: {len(files)} files")
                if files:
                    print(f"    Files: {', '.join(files[:5])}{'...' if len(files) > 5 else ''}")
    
    elif choice == "4":
        print("Exiting...")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
