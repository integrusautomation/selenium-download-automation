#!/usr/bin/env python3
"""
Deploy the webhook to a cloud platform
This script can be used to deploy to Heroku, Railway, or other platforms
"""

import os
import subprocess
import sys

def create_procfile():
    """Create a Procfile for deployment"""
    procfile_content = "web: gunicorn webhook_app:app"
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    print("Created Procfile")

def create_runtime_file():
    """Create runtime.txt for Python version"""
    with open("runtime.txt", "w") as f:
        f.write("python-3.9.23")
    print("Created runtime.txt")

def install_requirements():
    """Install requirements for webhook"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "webhook_requirements.txt"], check=True)
        print("Installed webhook requirements")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False
    return True

def run_webhook_locally():
    """Run the webhook locally for testing"""
    try:
        print("Starting webhook server locally...")
        print("Access the webhook at: http://localhost:5000")
        print("Endpoints available:")
        print("  - http://localhost:5000/results (JSON)")
        print("  - http://localhost:5000/results/table (HTML table)")
        print("  - http://localhost:5000/results/summary (Summary stats)")
        print("  - http://localhost:5000/health (Health check)")
        print("\nPress Ctrl+C to stop the server")
        
        subprocess.run([sys.executable, "webhook_app.py"])
    except KeyboardInterrupt:
        print("\nWebhook server stopped")
    except Exception as e:
        print(f"Error running webhook: {e}")

def main():
    """Main deployment function"""
    print("Phantombuster Results Webhook Deployment")
    print("=" * 40)
    
    # Create necessary files
    create_procfile()
    create_runtime_file()
    
    # Install requirements
    if not install_requirements():
        print("Failed to install requirements")
        return
    
    # Update webhook with latest results
    print("\nUpdating webhook with latest results...")
    try:
        subprocess.run([sys.executable, "update_webhook_results.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error updating webhook: {e}")
    
    # Ask user what to do
    print("\nDeployment options:")
    print("1. Run locally for testing")
    print("2. Deploy to Heroku")
    print("3. Deploy to Railway")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        run_webhook_locally()
    elif choice == "2":
        deploy_to_heroku()
    elif choice == "3":
        deploy_to_railway()
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice")

def deploy_to_heroku():
    """Deploy to Heroku"""
    print("Deploying to Heroku...")
    print("Make sure you have Heroku CLI installed and are logged in")
    
    try:
        # Check if Heroku CLI is available
        subprocess.run(["heroku", "--version"], check=True, capture_output=True)
        
        # Create Heroku app (if not exists)
        app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
        if app_name:
            subprocess.run(["heroku", "create", app_name], check=True)
        else:
            subprocess.run(["heroku", "create"], check=True)
        
        # Deploy
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Deploy webhook"], check=True)
        subprocess.run(["git", "push", "heroku", "main"], check=True)
        
        print("Deployment successful!")
        subprocess.run(["heroku", "open"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error deploying to Heroku: {e}")
    except FileNotFoundError:
        print("Heroku CLI not found. Please install it first.")

def deploy_to_railway():
    """Deploy to Railway"""
    print("Deploying to Railway...")
    print("Make sure you have Railway CLI installed and are logged in")
    
    try:
        # Check if Railway CLI is available
        subprocess.run(["railway", "--version"], check=True, capture_output=True)
        
        # Deploy
        subprocess.run(["railway", "deploy"], check=True)
        
        print("Deployment successful!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error deploying to Railway: {e}")
    except FileNotFoundError:
        print("Railway CLI not found. Please install it first.")

if __name__ == "__main__":
    main()
