#!/usr/bin/env python3
"""
Deploy GitHub Webhook for Phantombuster Automation
This script helps deploy the webhook to various platforms
"""

import os
import subprocess
import sys
import json
from datetime import datetime

def create_procfile():
    """Create Procfile for Heroku deployment"""
    with open("Procfile", "w") as f:
        f.write("web: python github_webhook.py")
    print("✓ Created Procfile")

def create_runtime():
    """Create runtime.txt for Python version"""
    with open("runtime.txt", "w") as f:
        f.write("python-3.9.23")
    print("✓ Created runtime.txt")

def create_requirements():
    """Create requirements.txt for webhook"""
    requirements = [
        "flask==2.3.3",
        "requests==2.31.0",
        "selenium==4.15.2",
        "chromedriver-autoinstaller==0.6.2"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    print("✓ Created requirements.txt")

def create_dockerfile():
    """Create Dockerfile for containerized deployment"""
    dockerfile_content = """FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    wget \\
    gnupg \\
    unzip \\
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \\
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \\
    && apt-get update \\
    && apt-get install -y google-chrome-stable \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directories
RUN mkdir -p result_files debug_screenshots

# Expose port
EXPOSE 5000

# Set environment variables
ENV PORT=5000
ENV DEBUG=false

# Run the application
CMD ["python", "github_webhook.py"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print("✓ Created Dockerfile")

def create_docker_compose():
    """Create docker-compose.yml for local development"""
    compose_content = """version: '3.8'

services:
  phantombuster-webhook:
    build: .
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
      - DEBUG=true
    volumes:
      - ./result_files:/app/result_files
      - ./debug_screenshots:/app/debug_screenshots
    restart: unless-stopped
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    print("✓ Created docker-compose.yml")

def create_env_file():
    """Create .env file template"""
    env_content = """# Phantombuster GitHub Webhook Configuration
PORT=5000
DEBUG=false

# Optional: Add your webhook secret for GitHub
# GITHUB_WEBHOOK_SECRET=your-secret-here

# Optional: Add authentication
# WEBHOOK_USERNAME=admin
# WEBHOOK_PASSWORD=your-password
"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)
    print("✓ Created .env.example")

def deploy_to_heroku():
    """Deploy to Heroku"""
    print("🚀 Deploying to Heroku...")
    
    try:
        # Check if Heroku CLI is available
        subprocess.run(["heroku", "--version"], check=True, capture_output=True)
        
        # Create Heroku app
        app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
        if app_name:
            subprocess.run(["heroku", "create", app_name], check=True)
        else:
            subprocess.run(["heroku", "create"], check=True)
        
        # Deploy
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Deploy GitHub webhook"], check=True)
        subprocess.run(["git", "push", "heroku", "main"], check=True)
        
        print("✅ Successfully deployed to Heroku!")
        subprocess.run(["heroku", "open"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error deploying to Heroku: {e}")
    except FileNotFoundError:
        print("❌ Heroku CLI not found. Please install it first.")

def deploy_to_railway():
    """Deploy to Railway"""
    print("🚀 Deploying to Railway...")
    
    try:
        # Check if Railway CLI is available
        subprocess.run(["railway", "--version"], check=True, capture_output=True)
        
        # Deploy
        subprocess.run(["railway", "deploy"], check=True)
        
        print("✅ Successfully deployed to Railway!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error deploying to Railway: {e}")
    except FileNotFoundError:
        print("❌ Railway CLI not found. Please install it first.")

def run_locally():
    """Run the webhook locally"""
    print("🏠 Starting webhook locally...")
    
    try:
        # Install dependencies
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        # Start the webhook
        print("🌐 Webhook will be available at: http://localhost:5000")
        print("🔗 GitHub webhook URL: http://localhost:5000/webhook/github")
        print("📊 Results page: http://localhost:5000")
        print("🔧 API endpoint: http://localhost:5000/api/results")
        print("\nPress Ctrl+C to stop the server")
        
        subprocess.run([sys.executable, "github_webhook.py"])
        
    except KeyboardInterrupt:
        print("\n👋 Webhook server stopped")
    except Exception as e:
        print(f"❌ Error running webhook: {e}")

def setup_github_webhook():
    """Instructions for setting up GitHub webhook"""
    print("\n🔧 GitHub Webhook Setup Instructions:")
    print("="*50)
    print("1. Go to your GitHub repository")
    print("2. Click on 'Settings' tab")
    print("3. Click on 'Webhooks' in the left sidebar")
    print("4. Click 'Add webhook'")
    print("5. Set the following values:")
    print("   - Payload URL: https://your-webhook-url.herokuapp.com/webhook/github")
    print("   - Content type: application/json")
    print("   - Events: Just the push event")
    print("   - Active: ✓")
    print("6. Click 'Add webhook'")
    print("\n📝 Note: Replace 'your-webhook-url' with your actual deployment URL")

def main():
    """Main deployment function"""
    print("🤖 Phantombuster GitHub Webhook Deployment")
    print("="*50)
    
    # Create necessary files
    create_procfile()
    create_runtime()
    create_requirements()
    create_dockerfile()
    create_docker_compose()
    create_env_file()
    
    print("\n📁 Deployment files created successfully!")
    
    # Ask user what to do
    print("\n🚀 Deployment Options:")
    print("1. Run locally for testing")
    print("2. Deploy to Heroku")
    print("3. Deploy to Railway")
    print("4. Deploy with Docker")
    print("5. Show GitHub webhook setup instructions")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        run_locally()
    elif choice == "2":
        deploy_to_heroku()
    elif choice == "3":
        deploy_to_railway()
    elif choice == "4":
        print("🐳 Docker deployment:")
        print("   docker-compose up -d")
        print("   # Or build and run manually:")
        print("   docker build -t phantombuster-webhook .")
        print("   docker run -p 5000:5000 phantombuster-webhook")
    elif choice == "5":
        setup_github_webhook()
    elif choice == "6":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
