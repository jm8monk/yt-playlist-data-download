from google_auth_oauthlib.flow import InstalledAppFlow
import os.path
import pickle

def authenticate(token_suffix):
    """Authentication function"""
    CLIENT_SECRETS_FILE = 'settings/client_secret.json'
    SCOPES = [
        'https://www.googleapis.com/auth/yt-analytics.readonly',
        'https://www.googleapis.com/auth/youtube.readonly'
    ]
    token_path = f'tokens/token_{token_suffix}.pickle'
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            if creds and creds.valid:
                print(f"Reusing existing credentials for {token_suffix}")
                return creds
    
    print(f"\nPlease authenticate for {token_suffix}...")
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    
    with open(token_path, 'wb') as token:
        pickle.dump(creds, token)
        
    return creds
