#!/usr/bin/env python3
"""
Phantombuster Complete Automation
This is the main script that handles everything: trigger webhook, wait, and download files.
No rate limit issues - uses Git clone instead of API calls.
"""

import os
import sys
import time
import subprocess
import shutil
import argparse
import requests
from datetime import datetime

# Configuration (override via environment variables)
# PHANTOMBUSTER_WEBHOOK_URL: Base URL of the Heroku webhook app (e.g., https://your-app.herokuapp.com)
# GITHUB_REPOSITORY: GitHub repo in owner/name format
WEBHOOK_URL = os.getenv("PHANTOMBUSTER_WEBHOOK_URL", "https://phantombuster-webhook-72a87a1e67bb.herokuapp.com")
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY", "integrusautomation/selenium-download-automation")

def _heroku_warmup(base_url: str, attempts: int = 3) -> None:
    """Best-effort warm-up for Heroku dyno cold starts."""
    try:
        for _ in range(attempts):
            try:
                # Prefer explicit health endpoint if available
                requests.get(f"{base_url}/api/health", timeout=8)
                return
            except Exception:
                try:
                    # Fallback to root
                    requests.get(base_url, timeout=8)
                    return
                except Exception:
                    time.sleep(2)
    except Exception:
        # Non-fatal
        pass

def trigger_webhook():
    """Trigger the webhook to start the automation"""
    print("🚀 Triggering Phantombuster webhook...")

    try:
        # Warm up Heroku (cold start mitigation)
        _heroku_warmup(WEBHOOK_URL)

        # Retry a few times in case the dyno is still spinning up
        # Try the dedicated selenium endpoint first, fallback to generic trigger
        endpoints = [
            f"{WEBHOOK_URL}/api/trigger-selenium",
            f"{WEBHOOK_URL}/trigger"
        ]
        
        last_status = None
        for endpoint in endpoints:
            for attempt in range(1, 6):
                try:
                    response = requests.post(
                        endpoint,
                        json={"triggered_by": "automation_script", "timestamp": datetime.now().isoformat()},
                        timeout=35
                    )
                    last_status = response.status_code
                    if response.status_code in [200, 202]:
                        result = response.json()
                        print(f"✅ Webhook triggered via {endpoint}: {result.get('message', 'OK')}")
                        return True
                    else:
                        print(f"⚠️  Trigger attempt {attempt}/5 on {endpoint} failed: {response.status_code}")
                except Exception as e:
                    print(f"⚠️  Trigger attempt {attempt}/5 on {endpoint} error: {e}")

                # Exponential backoff between attempts
                time.sleep(min(2 ** attempt, 15))
            
            # If first endpoint worked, don't try the second
            if last_status in [200, 202]:
                break

        print(f"❌ Failed to trigger webhook after retries. Last status: {last_status}")
        return False
            
    except Exception as e:
        print(f"❌ Error triggering webhook: {e}")
        return False

def check_webhook_status():
    """Check the current status of the webhook"""
    try:
        response = requests.get(f"{WEBHOOK_URL}/api/status", timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def wait_for_completion(timeout_minutes=30):
    """Wait for the automation to complete"""
    print(f"⏳ Waiting for automation to complete (timeout: {timeout_minutes} minutes)...")
    
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60
    
    while time.time() - start_time < timeout_seconds:
        status = check_webhook_status()
        if status:
            if status.get('running'):
                progress = status.get('progress', 0)
                print(f"🔄 Automation running... Progress: {progress}%")
            else:
                if status.get('last_error'):
                    print(f"❌ Automation failed: {status['last_error']}")
                    return False
                else:
                    print("✅ Automation completed successfully!")
                    return True
        
        time.sleep(30)  # Check every 30 seconds
    
    print(f"⏰ Timeout reached ({timeout_minutes} minutes)")
    return False

def wait_for_files_to_be_committed():
    """Wait additional time for files to be committed to repository"""
    print("⏳ Waiting 10 minutes for files to be committed to repository...")
    print("   (GitHub Actions needs time to process and commit the downloaded files)")
    
    for i in range(10):
        remaining = 10 - i
        print(f"   ⏰ {remaining} minutes remaining...")
        time.sleep(60)  # Wait 1 minute
    
    print("✅ Wait period completed - files should now be available")

def download_files(output_dir, token=None):
    """Download files using Git clone (no rate limits)"""
    print(f"📥 Downloading files to: {output_dir}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Clone repository
    repo_url = f"https://github.com/{GITHUB_REPO}.git"
    if token:
        repo_url = f"https://{token}@github.com/{GITHUB_REPO}.git"
    
    temp_dir = os.path.join(output_dir, "temp_clone")
    
    try:
        # Remove existing temp directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
        print("🔄 Cloning repository...")
        result = subprocess.run(
            ['git', 'clone', repo_url, temp_dir],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"❌ Clone failed: {result.stderr}")
            return False
        
        print("✅ Repository cloned")
        
        # Copy result_files
        result_files_source = os.path.join(temp_dir, "result_files")
        result_files_target = os.path.join(output_dir, "result_files")
        
        if os.path.exists(result_files_source):
            if os.path.exists(result_files_target):
                shutil.rmtree(result_files_target)
            shutil.copytree(result_files_source, result_files_target)
            
            # Count files
            file_count = 0
            for root, dirs, files in os.walk(result_files_target):
                file_count += len(files)
            
            print(f"✅ Downloaded {file_count} files")
        else:
            print("❌ result_files directory not found in repository")
            print("   This means the GitHub Actions workflow hasn't run yet or failed")
            print("   The workflow needs to:")
            print("   1. Run selenium_download.py")
            print("   2. Download files from Phantombuster")
            print("   3. Commit files to the repository")
            print("   Try running the full automation with: python phantombuster_automation.py")
            return False
        
        # Clean up
        shutil.rmtree(temp_dir)
        print("🧹 Cleaned up temporary files")
        
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Clone timed out")
        return False
    except Exception as e:
        print(f"❌ Error downloading files: {e}")
        return False

def clear_and_push_repository(token=None):
    """Clear result_files directory and push changes to repository"""
    print("🧹 Clearing result_files directory and pushing changes...")
    
    # Clone repository to a temporary location
    temp_repo_dir = "temp_repo_for_cleanup"
    repo_url = f"https://github.com/{GITHUB_REPO}.git"
    if token:
        repo_url = f"https://{token}@github.com/{GITHUB_REPO}.git"
    
    try:
        # Remove existing temp directory
        if os.path.exists(temp_repo_dir):
            shutil.rmtree(temp_repo_dir)
        
        print("🔄 Cloning repository for cleanup...")
        result = subprocess.run(
            ['git', 'clone', repo_url, temp_repo_dir],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"❌ Clone failed: {result.stderr}")
            return False
        
        # Change to repository directory
        os.chdir(temp_repo_dir)
        
        # Remove result_files directory if it exists
        if os.path.exists("result_files"):
            print("🗑️  Removing result_files directory...")
            shutil.rmtree("result_files")
            
            # Git add, commit, and push
            print("📝 Committing changes...")
            subprocess.run(['git', 'add', '-A'], check=True)
            subprocess.run(['git', 'commit', '-m', f'Clear result_files directory - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'], check=True)
            
            print("🚀 Pushing changes...")
            push_result = subprocess.run(['git', 'push'], capture_output=True, text=True)
            
            if push_result.returncode == 0:
                print("✅ Successfully cleared and pushed changes")
            else:
                print(f"❌ Push failed: {push_result.stderr}")
                return False
        else:
            print("ℹ️  result_files directory not found, nothing to clear")
        
        # Change back to original directory
        os.chdir("..")
        
        # Clean up
        shutil.rmtree(temp_repo_dir)
        print("🧹 Cleaned up temporary repository")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error clearing repository: {e}")
        return False
    finally:
        # Make sure we're back in the original directory
        try:
            os.chdir("..")
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description='Complete Phantombuster automation')
    parser.add_argument('--output', '-o', default='./phantombuster_files', 
                       help='Output directory (default: ./phantombuster_files)')
    parser.add_argument('--token', '-t', help='GitHub token (optional)')
    parser.add_argument('--timeout', type=int, default=30, 
                       help='Timeout in minutes (default: 30)')
    parser.add_argument('--no-wait', action='store_true', 
                       help='Do not wait for completion, just trigger and download')
    parser.add_argument('--no-file-wait', action='store_true', 
                       help='Skip the 10-minute wait for files to be committed')
    parser.add_argument('--download-only', action='store_true', 
                       help='Skip webhook trigger, just download files')
    parser.add_argument('--clear-after', action='store_true', 
                       help='Clear result_files directory and push changes after download')
    
    args = parser.parse_args()
    
    print("🤖 Phantombuster Complete Automation")
    print("=" * 50)
    print(f"📁 Output directory: {args.output}")
    print(f"⏰ Timeout: {args.timeout} minutes")
    print(f"🔄 Wait mode: {'No' if args.no_wait else 'Yes'}")
    print(f"📥 Download only: {'Yes' if args.download_only else 'No'}")
    print()
    
    if not args.download_only:
        # Step 1: Trigger webhook
        if not trigger_webhook():
            print("❌ Failed to trigger webhook")
            sys.exit(1)
        
        if args.no_wait:
            print("💡 Webhook triggered. Proceeding to download...")
        else:
            # Step 2: Wait for completion
            if not wait_for_completion(args.timeout):
                print("❌ Automation did not complete in time")
                sys.exit(1)
            
            # Step 2.5: Wait for files to be committed (unless skipped)
            if not args.no_file_wait:
                wait_for_files_to_be_committed()
            else:
                print("💡 Skipping file commit wait period")
    
    # Step 3: Download files
    if not download_files(args.output, args.token):
        print("❌ Failed to download files")
        sys.exit(1)
    
    # Step 4: Clear repository (if requested)
    if args.clear_after:
        if not clear_and_push_repository(args.token):
            print("⚠️  Warning: Failed to clear repository, but files were downloaded successfully")
    
    print(f"\n🎉 Automation completed successfully!")
    print(f"📁 Files saved to: {os.path.abspath(args.output)}")
    if args.clear_after:
        print("🧹 Repository cleared and changes pushed")

if __name__ == "__main__":
    main()


