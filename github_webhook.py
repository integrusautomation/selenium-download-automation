#!/usr/bin/env python3
"""
GitHub Webhook for Phantombuster Automation
This webhook can be triggered by GitHub to run the selenium automation and return results
"""

from flask import Flask, request, jsonify, render_template_string
import subprocess
import os
import json
import time
import threading
from datetime import datetime
import tempfile
import shutil

app = Flask(__name__)

# Global variables to track automation status
automation_status = {
    'running': False,
    'last_run': None,
    'last_results': None,
    'last_error': None,
    'progress': 0
}

# Directory where CSV results are stored
RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'result_files')

def clear_results_directory() -> None:
    """Remove all files in the results directory without deleting the folder."""
    try:
        if not os.path.isdir(RESULTS_DIR):
            return
        for entry in os.listdir(RESULTS_DIR):
            entry_path = os.path.join(RESULTS_DIR, entry)
            if os.path.isfile(entry_path) or os.path.islink(entry_path):
                try:
                    os.remove(entry_path)
                except Exception:
                    pass
            elif os.path.isdir(entry_path):
                try:
                    shutil.rmtree(entry_path)
                except Exception:
                    pass
    except Exception:
        # Silently ignore cleanup errors; webhook should still proceed
        pass

# HTML template for results display
RESULTS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Phantombuster Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: #2c3e50; color: white; padding: 20px; margin: -20px -20px 20px -20px; border-radius: 8px 8px 0 0; }
        .status { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .status.running { background: #e3f2fd; border-left: 4px solid #2196f3; }
        .status.success { background: #e8f5e8; border-left: 4px solid #4caf50; }
        .status.error { background: #ffebee; border-left: 4px solid #f44336; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        .folder-name { font-family: monospace; font-size: 12px; }
        .file-count { color: #666; font-weight: bold; }
        .empty { color: #999; font-style: italic; }
        .progress-bar { width: 100%; height: 20px; background-color: #e0e0e0; border-radius: 10px; overflow: hidden; margin: 10px 0; }
        .progress-fill { height: 100%; background-color: #4caf50; transition: width 0.3s ease; }
        .refresh-btn { background: #2196f3; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 10px 5px; }
        .refresh-btn:hover { background: #1976d2; }
        .auto-refresh { color: #666; font-size: 12px; margin: 10px 0; }
    </style>
    <script>
        function refreshPage() {
            location.reload();
        }
        
        function autoRefresh() {
            setTimeout(function() {
                location.reload();
            }, 30000); // Refresh every 30 seconds
        }
        
        // Auto-refresh if automation is running
        if ({{ 'true' if automation_status.running else 'false' }}) {
            autoRefresh();
        }
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Phantombuster Automation Results</h1>
            <p>Last updated: {{ last_updated }}</p>
        </div>
        
        <div class="status {{ status_class }}">
            <strong>Status:</strong> {{ status_text }}
            {% if automation_status.running %}
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ automation_status.progress }}%"></div>
                </div>
                <p>Progress: {{ automation_status.progress }}%</p>
            {% endif %}
        </div>
        
        {% if automation_status.last_error %}
        <div class="status error">
            <strong>Error:</strong> {{ automation_status.last_error }}
        </div>
        {% endif %}
        
        <div style="margin: 20px 0;">
            <button class="refresh-btn" onclick="refreshPage()">🔄 Refresh</button>
            <button class="refresh-btn" onclick="location.href='/trigger'">▶️ Run Automation</button>
            <button class="refresh-btn" onclick="location.href='/api/trigger-selenium'">🤖 Trigger Selenium</button>
            <button class="refresh-btn" onclick="location.href='/api/results'">📊 JSON API</button>
        </div>
        
        {% if results %}
        <h2>📊 Results Summary</h2>
        <p><strong>Total Folders:</strong> {{ total_folders }} | <strong>Total Files:</strong> {{ total_files }}</p>
        
        <table>
            <thead>
                <tr>
                    <th>Folder Name</th>
                    <th>File Count</th>
                    <th>File IDs</th>
                </tr>
            </thead>
            <tbody>
                {% for folder, files in results.items() %}
                <tr>
                    <td class="folder-name">{{ folder }}</td>
                    <td class="file-count">{{ files|length }}</td>
                    <td class="{% if files|length == 0 %}empty{% endif %}">
                        {% if files %}
                            {{ files|join(', ') }}
                        {% else %}
                            No files
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <div class="status">
            <p>No results available. Click "Run Automation" to start the process.</p>
        </div>
        {% endif %}
        
        {% if automation_status.running %}
        <div class="auto-refresh">
            🔄 Page will auto-refresh every 30 seconds while automation is running
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def run_automation():
    """Trigger GitHub Actions workflow for selenium automation"""
    global automation_status
    
    try:
        automation_status['running'] = True
        automation_status['progress'] = 0
        automation_status['last_error'] = None
        
        print("Triggering GitHub Actions workflow...")
        
        # Get GitHub token from environment
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            automation_status['last_error'] = "GITHUB_TOKEN environment variable not set"
            automation_status['running'] = False
            return
        
        # Get repository info from environment or use defaults
        repo_owner = os.environ.get('GITHUB_REPOSITORY_OWNER', 'integrusautomation')
        repo_name = os.environ.get('GITHUB_REPOSITORY_NAME', 'selenium-download-automation')
        
        # Trigger the workflow using repository_dispatch
        import requests
        
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/dispatches"
        
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            'event_type': 'webhook-trigger',
            'client_payload': {
                'triggered_by': 'webhook',
                'timestamp': datetime.now().isoformat()
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 204:
            automation_status['progress'] = 50
            automation_status['last_results'] = {"status": "workflow_triggered", "message": "GitHub Actions workflow started"}
            automation_status['progress'] = 100
            print("GitHub Actions workflow triggered successfully")
        else:
            automation_status['last_error'] = f"Failed to trigger workflow: {response.status_code} - {response.text}"
            print(f"Failed to trigger workflow: {response.status_code} - {response.text}")
    
    except Exception as e:
        automation_status['last_error'] = f"Unexpected error: {str(e)}"
        print(f"Unexpected error: {e}")
    finally:
        automation_status['running'] = False
        automation_status['last_run'] = datetime.now().isoformat()

def parse_results_from_output(output):
    """Parse results from selenium script output"""
    try:
        # Look for the "Results by folder:" line in the output
        lines = output.split('\n')
        results = {}
        
        for line in lines:
            if 'Results by folder:' in line:
                # Extract the dictionary from the line
                import re
                pattern = r"Results by folder:\s*({.*?})"
                match = re.search(pattern, line, re.DOTALL)
                
                if match:
                    results_str = match.group(1)
                    # Convert single quotes to double quotes for JSON parsing
                    results_str = results_str.replace("'", '"')
                    results = json.loads(results_str)
                    break
        
        return results
    except Exception as e:
        print(f"Error parsing results: {e}")
        return {}

@app.route('/')
def home():
    """Main page with results table"""
    results = automation_status.get('last_results', {})
    
    # Handle case where results is None
    if results is None:
        results = {}
    
    total_folders = len(results)
    total_files = sum(len(files) for files in results.values()) if results else 0
    
    # Determine status
    if automation_status['running']:
        status_class = 'running'
        status_text = 'Automation is running...'
    elif automation_status['last_error']:
        status_class = 'error'
        status_text = 'Last run failed'
    elif results:
        status_class = 'success'
        status_text = 'Last run completed successfully'
    else:
        status_class = 'running'
        status_text = 'No automation run yet'
    
    last_updated = automation_status.get('last_run', 'Never')
    if last_updated != 'Never':
        try:
            dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
            last_updated = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
    
    return render_template_string(RESULTS_TEMPLATE, 
                                results=results,
                                total_folders=total_folders,
                                total_files=total_files,
                                status_class=status_class,
                                status_text=status_text,
                                last_updated=last_updated,
                                automation_status=automation_status)

@app.route('/trigger', methods=['POST', 'GET'])
def trigger_automation():
    """Trigger the automation to run"""
    if automation_status['running']:
        return jsonify({
            'status': 'error',
            'message': 'Automation is already running'
        }), 400
    
    # Start automation in a separate thread
    thread = threading.Thread(target=run_automation)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'status': 'success',
        'message': 'Automation started',
        'redirect': '/'
    })

@app.route('/api/results')
def api_results():
    """API endpoint to get results as JSON"""
    results = automation_status.get('last_results', {})
    
    # Handle case where results is None
    if results is None:
        results = {}
    
    return jsonify({
        'status': 'success',
        'timestamp': automation_status.get('last_run'),
        'running': automation_status['running'],
        'total_folders': len(results),
        'total_files': sum(len(files) for files in results.values()) if results else 0,
        'results': results,
        'error': automation_status.get('last_error')
    })

@app.route('/api/status')
def api_status():
    """API endpoint to get automation status"""
    return jsonify(automation_status)

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'automation_running': automation_status['running']
    })

def trigger_selenium_download_workflow():
    """Trigger the selenium-download GitHub Actions workflow directly"""
    global automation_status
    
    try:
        automation_status['running'] = True
        automation_status['progress'] = 0
        automation_status['last_error'] = None
        
        print("Triggering Selenium Download Automation workflow...")
        
        # Get GitHub token from environment
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            automation_status['last_error'] = "GITHUB_TOKEN environment variable not set"
            automation_status['running'] = False
            return False
        
        # Get repository info from environment or use defaults
        repo_owner = os.environ.get('GITHUB_REPOSITORY_OWNER', 'integrusautomation')
        repo_name = os.environ.get('GITHUB_REPOSITORY_NAME', 'selenium-download-automation')
        workflow_name = os.environ.get('SELENIUM_WORKFLOW_NAME', 'Selenium Download Automation')
        
        import requests
        
        # Try to trigger the workflow using workflow_dispatch API
        # First, get the workflow ID by listing workflows
        workflows_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows"
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        workflows_response = requests.get(workflows_url, headers=headers)
        
        if workflows_response.status_code != 200:
            # Fallback to repository_dispatch if workflow listing fails
            print(f"Could not list workflows, using repository_dispatch fallback")
            dispatch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/dispatches"
            dispatch_data = {
                'event_type': 'selenium-download-trigger',
                'client_payload': {
                    'triggered_by': 'api',
                    'trigger_type': 'selenium-download',
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            response = requests.post(dispatch_url, headers=headers, json=dispatch_data)
            if response.status_code == 204:
                automation_status['progress'] = 100
                automation_status['last_results'] = {
                    "status": "workflow_triggered",
                    "message": "Selenium Download Automation workflow started via repository_dispatch",
                    "trigger_type": "selenium-download"
                }
                print("Selenium Download Automation workflow triggered successfully")
                return True
            else:
                automation_status['last_error'] = f"Failed to trigger workflow: {response.status_code} - {response.text}"
                return False
        
        # Find the selenium-download workflow
        workflows = workflows_response.json().get('workflows', [])
        workflow_id = None
        workflow_file = None
        
        for workflow in workflows:
            if 'selenium' in workflow['name'].lower() or workflow['name'] == workflow_name:
                workflow_id = workflow['id']
                workflow_file = workflow['path']
                break
        
        if not workflow_id:
            # Fallback: try workflow_dispatch on the known workflow file
            workflow_file = "selenium-download.yml"
            if not workflow_file.startswith('.github/workflows/'):
                workflow_file = f".github/workflows/{workflow_file}"
            
            # Use workflow_dispatch API
            dispatch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_file}/dispatches"
            dispatch_data = {
                'ref': 'main',
                'inputs': {
                    'triggered_by': 'api',
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            response = requests.post(dispatch_url, headers=headers, json=dispatch_data)
            if response.status_code == 204:
                automation_status['progress'] = 100
                automation_status['last_results'] = {
                    "status": "workflow_triggered",
                    "message": "Selenium Download Automation workflow started",
                    "trigger_type": "selenium-download",
                    "workflow_file": workflow_file
                }
                print("Selenium Download Automation workflow triggered successfully")
                return True
            else:
                # Final fallback to repository_dispatch
                print(f"workflow_dispatch failed, using repository_dispatch fallback: {response.status_code}")
                dispatch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/dispatches"
                dispatch_data = {
                    'event_type': 'selenium-download-trigger',
                    'client_payload': {
                        'triggered_by': 'api',
                        'trigger_type': 'selenium-download',
                        'timestamp': datetime.now().isoformat()
                    }
                }
                response = requests.post(dispatch_url, headers=headers, json=dispatch_data)
                if response.status_code == 204:
                    automation_status['progress'] = 100
                    automation_status['last_results'] = {
                        "status": "workflow_triggered",
                        "message": "Selenium Download Automation workflow started via repository_dispatch",
                        "trigger_type": "selenium-download"
                    }
                    print("Selenium Download Automation workflow triggered successfully")
                    return True
                else:
                    automation_status['last_error'] = f"Failed to trigger workflow: {response.status_code} - {response.text}"
                    return False
        
        # Use workflow ID to trigger
        dispatch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_id}/dispatches"
        dispatch_data = {
            'ref': 'main',
            'inputs': {
                'triggered_by': 'api',
                'timestamp': datetime.now().isoformat()
            }
        }
        
        response = requests.post(dispatch_url, headers=headers, json=dispatch_data)
        if response.status_code == 204:
            automation_status['progress'] = 100
            automation_status['last_results'] = {
                "status": "workflow_triggered",
                "message": "Selenium Download Automation workflow started",
                "trigger_type": "selenium-download",
                "workflow_id": workflow_id
            }
            print("Selenium Download Automation workflow triggered successfully")
            return True
        else:
            automation_status['last_error'] = f"Failed to trigger workflow: {response.status_code} - {response.text}"
            print(f"Failed to trigger workflow: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        automation_status['last_error'] = f"Unexpected error: {str(e)}"
        print(f"Unexpected error: {e}")
        return False
    finally:
        automation_status['running'] = False
        automation_status['last_run'] = datetime.now().isoformat()

@app.route('/api/trigger-selenium', methods=['POST', 'GET'])
def api_trigger_selenium():
    """Dedicated API endpoint to trigger Selenium Download Automation"""
    if automation_status['running']:
        return jsonify({
            'status': 'error',
            'message': 'Automation is already running',
            'running': True
        }), 400
    
    # Start automation in a separate thread
    thread = threading.Thread(target=trigger_selenium_download_workflow)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'status': 'success',
        'message': 'Selenium Download Automation triggered',
        'endpoint': '/api/trigger-selenium',
        'status_endpoint': '/api/status',
        'results_endpoint': '/api/results',
        'triggered_at': datetime.now().isoformat()
    }), 202

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    """GitHub webhook endpoint"""
    try:
        # Clear out previous results on every webhook call
        clear_results_directory()
        # Verify the webhook (optional - add secret verification)
        payload = request.get_json()
        
        if not payload:
            return jsonify({'error': 'No payload'}), 400
        
        # Check if this is a push to main branch
        if payload.get('ref') == 'refs/heads/main' and payload.get('action') == 'opened':
            # Trigger automation
            if not automation_status['running']:
                thread = threading.Thread(target=run_automation)
                thread.daemon = True
                thread.start()
                
                return jsonify({
                    'status': 'success',
                    'message': 'Automation triggered by GitHub webhook'
                })
            else:
                return jsonify({
                    'status': 'info',
                    'message': 'Automation already running'
                })
        
        return jsonify({'status': 'ignored', 'message': 'Not a relevant event'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    print("🚀 Starting Phantombuster GitHub Webhook")
    print(f"📡 Webhook URL: http://localhost:{port}")
    print(f"🔗 GitHub webhook: http://localhost:{port}/webhook/github")
    print(f"📊 Results page: http://localhost:{port}")
    print(f"🔧 API endpoint: http://localhost:{port}/api/results")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
