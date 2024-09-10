import base64
import os
import urllib.parse
import webbrowser
from requests import post, get
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

redirect_uri = 'http://localhost:8888/callback' 

# TO EDIT
# From the previous step, after sign in to your spotify account your are redirected to 
# the redirect_url. Copy paste the entire URL like the one below, and store it in my_url_from_previous_step.
my_url_from_previous_step = "http://localhost:8888/callback?code=AQDGCSxy8hXCXJyig8D0F8NpnB0ZSRmQzcuIbBpcualf2pzOdVOqI0bSEoLv8S6LK4di-wYdLTfu2XLSNJT9QH_mvSx9VBlGJW6gx87FPTvicZQRRjZqWQIJvFnznOaLC9rqsF44Bht5F5iYtDZ10N9OX_KW126UPc6WIt7m4qa30tXWXH7314H5vd9ttgLZyHgurxEKvs2albNhpDgEhyLxv7fhjxcmuOl7GmO2qKYoFiYV5yMY-JZc0XopbDc&state=0f3bda125daeea15bdebc2a7e9bf9467"

# Extract the code and state from the query parameters
query_params = urllib.parse.parse_qs(urllib.parse.urlparse(my_url_from_previous_step).query)
code = query_params.get('code', [None])[0]
state = query_params.get('state', [None])[0]

if state is None:
    print('State mismatch')
else:
    # Exchange the authorization code for an access token
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    token_headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()
    }
    token_response = post(token_url, data=token_data, headers=token_headers)
    token_json = token_response.json()
    
    print("access_token:", token_json['access_token'])
    # With this print copy paste the code in "access token" and put it in ToSpotify.py