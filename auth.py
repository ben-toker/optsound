import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables for Spotify credentials
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "user-library-read"  # Scope for accessing Liked Songs

# Authenticate using SpotifyOAuth
def authenticate_spotify():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE
        )
    )
    return sp

# Fetch user's liked songs
def get_liked_songs(sp):
    print("Fetching liked songs...")
    results = sp.current_user_saved_tracks(limit=50)  # Fetch first 50 liked songs
    track_ids = []

    for idx, item in enumerate(results['items']):
        track = item['track']
        track_ids.append(track['id'])
        print(f"{idx + 1}. {track['name']} - {track['artists'][0]['name']}")

    return track_ids

# Main function
if __name__ == "__main__":
    sp = authenticate_spotify()
    track_ids = get_liked_songs(sp)
    print("\nTrack IDs:", track_ids)

