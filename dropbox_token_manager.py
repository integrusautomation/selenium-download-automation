"""
Dropbox Token Manager for handling Dropbox authentication
"""
import os
import json
import requests
from datetime import datetime, timedelta

class DropboxTokenManager:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        self.app_key = os.environ.get('DROPBOX_APP_KEY')
        self.app_secret = os.environ.get('DROPBOX_APP_SECRET')
        self.refresh_token_env = os.environ.get('DROPBOX_REFRESH_TOKEN')
        
    def get_current_token(self):
        """Get the current access token, refreshing if necessary"""
        if not self.access_token or self._is_token_expired():
            if not self._refresh_token():
                return None
        return self.access_token
    
    def _is_token_expired(self):
        """Check if the current token is expired"""
        if not self.token_expires_at:
            return True
        return datetime.now() >= self.token_expires_at
    
    def _refresh_token(self):
        """Refresh the access token using the refresh token"""
        if not self.refresh_token_env or not self.app_key or not self.app_secret:
            return False
        
        try:
            url = "https://api.dropbox.com/oauth2/token"
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token_env,
                'client_id': self.app_key,
                'client_secret': self.app_secret
            }
            
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.refresh_token = token_data.get('refresh_token', self.refresh_token_env)
            
            # Set expiration time (typically 4 hours)
            expires_in = token_data.get('expires_in', 14400)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)  # 1 minute buffer
            
            return True
            
        except Exception as e:
            print(f"Error refreshing Dropbox token: {e}")
            return False
    
    def test_token(self, token):
        """Test if a token is valid by making a simple API call"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(
                'https://api.dropboxapi.com/2/users/get_current_account',
                headers=headers,
                json={}
            )
            
            if response.status_code == 200:
                account_info = response.json()
                return {
                    'valid': True,
                    'account_name': account_info.get('name', {}).get('display_name', 'Unknown')
                }
            else:
                return {
                    'valid': False,
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }

# Global instance
_token_manager = None

def get_token_manager():
    """Get the global token manager instance"""
    global _token_manager
    if _token_manager is None:
        _token_manager = DropboxTokenManager()
    return _token_manager
