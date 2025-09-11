# Phantombuster Results Webhook

A simple webhook service that provides access to the results from the Phantombuster selenium automation script.

## Features

- **JSON API** - Get results as structured JSON data
- **HTML Table** - View results in a formatted HTML table
- **Summary Statistics** - Get aggregated statistics about the results
- **Health Check** - Monitor service status
- **Auto-update** - Results are automatically updated after each selenium run

## API Endpoints

### 1. Get Results (JSON)
```
GET /results
```

Returns the complete results as JSON with metadata:
```json
{
  "status": "success",
  "timestamp": "2025-09-11T18:15:00.000Z",
  "total_folders": 47,
  "total_files": 234,
  "results": {
    "zb3ZwQnVuZcM0cfCNbQoIQ/": ["000000108", "000000107", "000000106"],
    "EQl5K9ngclSt6QfdgqaWOQ/": ["000000078", "000000077", "000000076"]
  }
}
```

### 2. Get Results (HTML Table)
```
GET /results/table
```

Returns a formatted HTML table showing all results with:
- Folder names
- File counts
- File IDs
- Summary statistics

### 3. Get Summary Statistics
```
GET /results/summary
```

Returns aggregated statistics:
```json
{
  "status": "success",
  "timestamp": "2025-09-11T18:15:00.000Z",
  "summary": {
    "total_folders": 47,
    "total_files": 234,
    "folders_with_files": 46,
    "empty_folders": 1,
    "max_files_per_folder": 6,
    "min_files_per_folder": 0,
    "avg_files_per_folder": 4.98
  },
  "top_folders_by_file_count": [
    ["Zy19AY3hC3sR7Q0USiwj5w/", 6],
    ["JUTbwdhFNqk0kXFfJGGKwA/", 5]
  ]
}
```

### 4. Health Check
```
GET /health
```

Returns service health status:
```json
{
  "status": "healthy",
  "timestamp": "2025-09-11T18:15:00.000Z"
}
```

## Local Development

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
# Install dependencies
pip install -r webhook_requirements.txt

# Update webhook with latest results
python update_webhook_results.py

# Run the webhook locally
python webhook_app.py
```

The webhook will be available at `http://localhost:5000`

## Deployment

### Option 1: Deploy Script
```bash
python deploy_webhook.py
```

This interactive script will help you:
- Deploy to Heroku
- Deploy to Railway
- Run locally for testing

### Option 2: Manual Deployment

#### Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-app-name

# Deploy
git add .
git commit -m "Deploy webhook"
git push heroku main

# Open app
heroku open
```

#### Railway
```bash
# Install Railway CLI and login
railway login

# Deploy
railway deploy
```

## Integration with GitHub Actions

The webhook is automatically updated after each selenium script run through the GitHub Actions workflow. The workflow:

1. Runs the selenium script
2. Updates the webhook with latest results
3. Commits and pushes changes to the repository

## File Structure

```
├── webhook_app.py              # Main Flask application
├── update_webhook_results.py   # Script to update webhook data
├── deploy_webhook.py           # Deployment script
├── webhook_requirements.txt    # Python dependencies
├── Procfile                    # Heroku deployment config
├── runtime.txt                 # Python version specification
└── WEBHOOK_README.md          # This file
```

## Usage Examples

### cURL Examples

```bash
# Get JSON results
curl https://your-webhook-url.herokuapp.com/results

# Get HTML table
curl https://your-webhook-url.herokuapp.com/results/table

# Get summary
curl https://your-webhook-url.herokuapp.com/results/summary

# Health check
curl https://your-webhook-url.herokuapp.com/health
```

### JavaScript Example

```javascript
// Fetch results
fetch('https://your-webhook-url.herokuapp.com/results')
  .then(response => response.json())
  .then(data => {
    console.log('Total folders:', data.total_folders);
    console.log('Total files:', data.total_files);
    console.log('Results:', data.results);
  });
```

### Python Example

```python
import requests

# Get results
response = requests.get('https://your-webhook-url.herokuapp.com/results')
data = response.json()

print(f"Total folders: {data['total_folders']}")
print(f"Total files: {data['total_files']}")

# Process results
for folder, files in data['results'].items():
    print(f"{folder}: {len(files)} files")
```

## Monitoring

The webhook includes a health check endpoint that can be used for monitoring:

- **Uptime monitoring**: Check `/health` endpoint
- **Data freshness**: Check `timestamp` in responses
- **Error handling**: All endpoints return proper HTTP status codes

## Security

- No authentication required (public API)
- Rate limiting can be added if needed
- CORS enabled for web access
- Input validation on all endpoints

## Troubleshooting

### Common Issues

1. **Webhook not updating**: Check if `update_webhook_results.py` is running
2. **Empty results**: Verify selenium script is completing successfully
3. **Deployment issues**: Check platform-specific logs (Heroku logs, Railway logs)

### Debug Mode

Run locally with debug mode:
```bash
export FLASK_DEBUG=1
python webhook_app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is part of the Phantombuster automation system.
