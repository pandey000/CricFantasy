import requests
from firebase_admin import credentials, db, initialize_app
import time

cred = credentials.Certificate('firebase-key.json')
initialize_app(cred, {'databaseURL': 'https://ipl-fantasy-123.firebaseio.com'})  # Your URL
API_KEY = 'f85d5c48-411e-42ee-897a-97920d6249fa'  # Get from cricapi.com

def fetch_matches():
    url = f"https://api.cricapi.com/v1/matches?apikey={API_KEY}"
    matches = requests.get(url).json()['data']
    upcoming = {m['id']: {'name': m['name'], 'dateTimeGMT': m['dateTimeGMT']}
               for m in matches if 'IPL' in m['name'] and m['dateTimeGMT'] > time.strftime('%Y-%m-%dT%H:%M:%SZ')}
    db.reference('matches').set(upcoming)

if __name__ == "__main__":
    fetch_matches()