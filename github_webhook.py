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
    """Run the selenium automation in a separate thread"""
    global automation_status
    
    try:
        automation_status['running'] = True
        automation_status['progress'] = 0
        automation_status['last_error'] = None
        
        print("Starting selenium automation...")
        
        # Change to the selenium automation directory
        selenium_dir = os.path.join(os.path.dirname(__file__), 'selenium-automation')
        if not os.path.exists(selenium_dir):
            selenium_dir = os.path.dirname(__file__)
        
        # Run the selenium script
        result = subprocess.run(
            ['python', 'selenium_download.py'],
            cwd=selenium_dir,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout
        )
        
        automation_status['progress'] = 50
        
        if result.returncode == 0:
            # Parse results from the output
            output = result.stdout
            results = parse_results_from_output(output)
            
            automation_status['last_results'] = results
            automation_status['progress'] = 100
            print("Automation completed successfully")
        else:
            automation_status['last_error'] = f"Automation failed: {result.stderr}"
            print(f"Automation failed: {result.stderr}")
    
    except subprocess.TimeoutExpired:
        automation_status['last_error'] = "Automation timed out after 30 minutes"
        print("Automation timed out")
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

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    """GitHub webhook endpoint"""
    try:
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
