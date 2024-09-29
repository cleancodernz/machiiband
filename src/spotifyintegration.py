import requests
import os

# Get a spotify token
def get_spotify_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    auth_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(auth_url, headers=headers, data=data)
    token_info = response.json()
    
    return token_info['access_token']

# search for the spotify song
def search_spotify_song(song_name, token):
    search_url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": song_name,
        "type": "track",
        "limit": 1  # Return only the top result
    }
    
    response = requests.get(search_url, headers=headers, params=params)
    
    if response.status_code == 200:
        track_info = response.json()
        tracks = track_info['tracks']['items']
        if tracks:
            return tracks[0]  # Return the first matching track
    return None

