import requests
from firebase_admin import credentials, db, initialize_app
import time

cred = credentials.Certificate('firebase-key.json')
initialize_app(cred, {'databaseURL': 'https://cricfantasy-4b50b-default-rtdb.firebaseio.com'})  # Your URL
API_KEY = 'f85d5c48-411e-42ee-897a-97920d6249fa'  # Your key

def fetch_matches():
    url = f"https://api.cricapi.com/v1/cricScore?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json().get('data', [])
    print("API Response:", data)  # Debug
    upcoming = {}
    for match in data:
        if match.get('series') == "Indian Premier League 2025" and match.get('status') == "Match not started":
            match_id = match.get('id')
            upcoming[match_id] = {
                'name': f"{match.get('t1')} vs {match.get('t2')}",
                'dateTimeGMT': match.get('dateTimeGMT')
            }
    print("Upcoming IPL Matches:", upcoming)  # Debug
    if upcoming:
        db.reference('matches').set(upcoming)
    else:
        print("No upcoming IPL matches found")

if __name__ == "__main__":
    fetch_matches()