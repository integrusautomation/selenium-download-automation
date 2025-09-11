# Webhook API

RESTful API service that serves Phantombuster results and provides webhook functionality.

## Files

- `webhook_app.py` - Main Flask application
- `update_webhook_results.py` - Results update script
- `deploy_webhook.py` - Deployment helper
- `webhook_requirements.txt` - Python dependencies
- `README.md` - This documentation

## Features

- ✅ RESTful API endpoints
- ✅ JSON and HTML data formats
- ✅ Summary statistics
- ✅ Health monitoring
- ✅ Auto-updating results
- ✅ CORS support

## API Endpoints

### Get Results (JSON)
```
GET /results
```

### Get Results (HTML Table)
```
GET /results/table
```

### Get Summary Statistics
```
GET /results/summary
```

### Health Check
```
GET /health
```

## Quick Start

```bash
# Install dependencies
pip install -r webhook_requirements.txt

# Update with latest results
python update_webhook_results.py

# Start webhook server
python webhook_app.py
```

## Deployment

```bash
# Use deployment helper
python deploy_webhook.py
```

Options:
- Heroku
- Railway
- Docker
- Local testing

## Configuration

Set environment variables:

```bash
export WEBHOOK_HOST="0.0.0.0"
export WEBHOOK_PORT="5000"
export WEBHOOK_DEBUG="false"
```

See the main README for complete documentation.
