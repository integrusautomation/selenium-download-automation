# DeletePB GitHub Actions Webhook Guide

## Overview
The `deletepb.yml` workflow runs the `deletepb.py` script and can be triggered via webhook.

## How to Trigger via Webhook

### 1. Create a GitHub Personal Access Token (PAT)
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with `repo` scope
3. Copy the token (you'll need it for the webhook)

### 2. Webhook URL
Use this endpoint to trigger the workflow:

```
POST https://api.github.com/repos/{OWNER}/{REPO}/dispatches
```

Replace:
- `{OWNER}` with your GitHub username or organization
- `{REPO}` with your repository name

### 3. Webhook Request Example

**Using curl:**
```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/{OWNER}/{REPO}/dispatches \
  -d '{"event_type":"deletepb"}'
```

**Using Python:**
```python
import requests

url = "https://api.github.com/repos/{OWNER}/{REPO}/dispatches"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer YOUR_GITHUB_TOKEN",
    "X-GitHub-Api-Version": "2022-11-28"
}
data = {"event_type": "deletepb"}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
```

**Using JavaScript/Node.js:**
```javascript
fetch('https://api.github.com/repos/{OWNER}/{REPO}/dispatches', {
  method: 'POST',
  headers: {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer YOUR_GITHUB_TOKEN',
    'X-GitHub-Api-Version': '2022-11-28',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    event_type: 'deletepb'
  })
})
```

## Manual Trigger
You can also trigger the workflow manually from the GitHub Actions tab:
1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. Select "Run DeletePB Script" from the workflow list
4. Click "Run workflow"

## Workflow Features
- Automatically sets up Python 3.9
- Installs Chrome and ChromeDriver
- Installs all dependencies from `requirements.txt`
- Runs `deletepb.py` script
- Uploads debug screenshots as artifacts (retained for 7 days)

## Notes
- The workflow uses `repository_dispatch` event type `deletepb`
- Make sure your GitHub token has the `repo` scope
- The workflow runs on `ubuntu-latest` runner
- Debug screenshots are automatically uploaded as artifacts

