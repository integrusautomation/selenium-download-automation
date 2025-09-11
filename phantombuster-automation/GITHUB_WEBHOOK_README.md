# GitHub Webhook for Phantombuster Automation

A webhook service that can be triggered by GitHub to run Phantombuster automation and return results in a beautiful table format.

## 🚀 Features

- **GitHub Integration**: Can be triggered by GitHub webhooks
- **Beautiful UI**: Clean, responsive web interface with real-time updates
- **REST API**: JSON API endpoints for programmatic access
- **Real-time Status**: Live progress tracking and status updates
- **Auto-refresh**: Page automatically refreshes during automation
- **Error Handling**: Comprehensive error reporting and logging
- **Multiple Triggers**: Manual, scheduled, and GitHub webhook triggers

## 📁 Files

- `github_webhook.py` - Main webhook application
- `deploy_github_webhook.py` - Deployment helper script
- `.github/workflows/github-webhook-trigger.yml` - GitHub Actions workflow
- `GITHUB_WEBHOOK_README.md` - This documentation

## 🎯 Quick Start

### 1. Local Development

```bash
# Install dependencies
pip install flask requests

# Run the webhook
python github_webhook.py
```

The webhook will be available at:
- **Main page**: http://localhost:5000
- **API**: http://localhost:5000/api/results
- **GitHub webhook**: http://localhost:5000/webhook/github

### 2. Deploy to Cloud

```bash
# Use the deployment script
python deploy_github_webhook.py
```

Choose from:
- Heroku (recommended)
- Railway
- Docker
- Local testing

## 🔧 API Endpoints

### Main Page
```
GET /
```
Returns the beautiful results table with real-time status.

### Trigger Automation
```
POST /trigger
GET /trigger
```
Manually trigger the automation to run.

### API Results
```
GET /api/results
```
Returns results as JSON:
```json
{
  "status": "success",
  "timestamp": "2025-09-11T18:15:00.000Z",
  "running": false,
  "total_folders": 47,
  "total_files": 234,
  "results": {
    "zb3ZwQnVuZcM0cfCNbQoIQ/": ["000000108", "000000107"],
    "EQl5K9ngclSt6QfdgqaWOQ/": ["000000078", "000000077"]
  },
  "error": null
}
```

### Status Check
```
GET /api/status
```
Returns automation status:
```json
{
  "running": false,
  "last_run": "2025-09-11T18:15:00.000Z",
  "last_results": {...},
  "last_error": null,
  "progress": 100
}
```

### Health Check
```
GET /api/health
```
Returns service health status.

### GitHub Webhook
```
POST /webhook/github
```
Endpoint for GitHub webhooks to trigger automation.

## 🎨 Web Interface

The web interface provides:

- **Real-time Status**: Shows if automation is running
- **Progress Bar**: Visual progress indicator
- **Results Table**: Clean table showing all folders and files
- **Auto-refresh**: Page refreshes automatically during automation
- **Manual Controls**: Buttons to trigger automation and refresh
- **Error Display**: Shows any errors that occurred
- **Responsive Design**: Works on desktop and mobile

## 🔗 GitHub Integration

### Setting up GitHub Webhook

1. **Deploy the webhook** to a public URL (Heroku, Railway, etc.)
2. **Go to your GitHub repository**
3. **Click Settings → Webhooks**
4. **Click "Add webhook"**
5. **Configure the webhook:**
   - **Payload URL**: `https://your-webhook-url.herokuapp.com/webhook/github`
   - **Content type**: `application/json`
   - **Events**: Just the `push` event
   - **Active**: ✓
6. **Click "Add webhook"**

### GitHub Actions Integration

The included GitHub Actions workflow can:
- Trigger automation on schedule
- Trigger on code changes
- Run automation and return results
- Upload results as artifacts
- Comment on pull requests

## 🚀 Deployment Options

### Heroku (Recommended)

```bash
# Install Heroku CLI
# Login to Heroku
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

### Railway

```bash
# Install Railway CLI
# Login to Railway
railway login

# Deploy
railway deploy
```

### Docker

```bash
# Build image
docker build -t phantombuster-webhook .

# Run container
docker run -p 5000:5000 phantombuster-webhook
```

### Docker Compose

```bash
# Start with docker-compose
docker-compose up -d
```

## ⚙️ Configuration

### Environment Variables

```bash
PORT=5000                    # Port to run on
DEBUG=false                  # Debug mode
GITHUB_WEBHOOK_SECRET=secret # Optional webhook secret
```

### Configuration File

Create a `config.json`:

```json
{
  "webhook": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false
  },
  "selenium": {
    "script_path": "selenium_download.py",
    "timeout": 1800
  },
  "github": {
    "webhook_secret": "your-secret-here"
  }
}
```

## 🔒 Security

### Webhook Security

- **Secret Verification**: Verify GitHub webhook signatures
- **Rate Limiting**: Prevent abuse
- **Input Validation**: Validate all inputs
- **Error Handling**: Don't expose sensitive information

### Authentication (Optional)

Add basic authentication:

```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == 'admin' and password == 'secret'

@app.route('/trigger')
@auth.login_required
def trigger_automation():
    # ... existing code
```

## 📊 Monitoring

### Health Checks

```bash
# Check if service is running
curl https://your-webhook-url.herokuapp.com/api/health

# Check automation status
curl https://your-webhook-url.herokuapp.com/api/status
```

### Logging

The webhook logs:
- Automation start/stop times
- Progress updates
- Errors and exceptions
- Webhook triggers
- API requests

### Metrics

Track:
- Automation success rate
- Average run time
- Error frequency
- API response times

## 🧪 Testing

### Test Locally

```bash
# Start webhook
python github_webhook.py

# Test trigger
curl -X POST http://localhost:5000/trigger

# Test API
curl http://localhost:5000/api/results
```

### Test GitHub Webhook

```bash
# Simulate GitHub webhook
curl -X POST http://localhost:5000/webhook/github \
  -H "Content-Type: application/json" \
  -d '{"ref": "refs/heads/main", "action": "opened"}'
```

## 🔧 Troubleshooting

### Common Issues

1. **Webhook not triggering**: Check GitHub webhook URL and events
2. **Automation not starting**: Check selenium script path and permissions
3. **Results not showing**: Check if automation completed successfully
4. **Page not loading**: Check if webhook is running and accessible

### Debug Mode

```bash
# Run with debug mode
DEBUG=true python github_webhook.py
```

### Logs

```bash
# Check Heroku logs
heroku logs --tail

# Check Docker logs
docker logs container-name
```

## 📈 Performance

### Optimization Tips

1. **Use headless browser**: Faster execution
2. **Optimize selenium script**: Reduce wait times
3. **Cache results**: Store results in database
4. **Use CDN**: For static assets
5. **Load balancing**: For high traffic

### Scaling

- **Horizontal scaling**: Multiple webhook instances
- **Database**: Store results in database
- **Queue system**: Use Redis/RabbitMQ for job queuing
- **Caching**: Cache results for faster access

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- **Documentation**: Check this README
- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub discussions

---

**Made with ❤️ for automation enthusiasts**
