import base64
import os
import urllib.parse
import webbrowser
from requests import post, get
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# TO EDIT 
# You choose your personal redirect URI, this one can work fine but you need to register 
# it on the Spotify developer page where they ask all the redirect URIs that you use.
redirect_uri = 'http://localhost:8888/callback'

####################################################

state = os.urandom(16).hex()
scope = 'user-read-private user-read-email playlist-modify-private'

query_params = {
    'response_type': 'code',
    'client_id': client_id,
    'scope': scope,
    'redirect_uri': redirect_uri,
    'state': state
}

query_string = urllib.parse.urlencode(query_params)
url = f'https://accounts.spotify.com/authorize?{query_string}'

# Open the authorization URL in the user's default web browser
webbrowser.open(url)
