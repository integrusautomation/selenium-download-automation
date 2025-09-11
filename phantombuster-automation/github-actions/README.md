# GitHub Actions

Automated workflows for running Phantombuster automation and managing results.

## Files

- `selenium-download.yml` - Main automation workflow
- `github-webhook-trigger.yml` - Webhook trigger workflow
- `README.md` - This documentation

## Workflows

### Selenium Download Workflow
- **Trigger**: Daily at 2 AM UTC, manual, on push
- **Features**: Chrome setup, automation execution, result management
- **Output**: CSV files, debug screenshots, webhook updates

### GitHub Webhook Trigger Workflow
- **Trigger**: Manual, scheduled, on push
- **Features**: Webhook server, automation triggering, result collection
- **Output**: Results JSON, artifacts, PR comments

## Setup

1. **Copy workflows** to `.github/workflows/` in your repository
2. **Enable GitHub Actions** in repository settings
3. **Set up secrets** if needed
4. **Configure triggers** as desired

## Manual Trigger

1. Go to **Actions** tab in your repository
2. Select the workflow you want to run
3. Click **"Run workflow"**
4. Monitor the execution

## Configuration

### Environment Variables
```yaml
env:
  CHROME_BIN: /usr/bin/google-chrome
  CHROMEDRIVER: /usr/local/bin/chromedriver
  WEBHOOK_URL: https://your-webhook.herokuapp.com
```

### Secrets
- `GITHUB_TOKEN` - For repository access
- `WEBHOOK_SECRET` - For webhook verification (optional)

## Monitoring

- **Workflow runs**: Check Actions tab
- **Logs**: View detailed execution logs
- **Artifacts**: Download result files
- **Status**: Monitor success/failure rates

See the main README for complete documentation.
