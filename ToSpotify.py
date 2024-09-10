from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import urllib.parse
import csv


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#TO EDIT
source_file_name = "MyPlaylist"
target_file_name = "MyPlaylistSpotify"
target_playlist_id = "to fill with playlist id"

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = post(url, headers=headers, data=data)
    json_response = json.loads(response.content)
    print(json_response)
    token_id = json_response["access_token"]
    return token_id

def get_auth_token(token):
    return {"Authorization": "Bearer " + token}

def get_auth_token_post():
    """
    The token below is obtained by refreshing the access token in the refresh.py file, this should allow API request that modify user's 
    content like his playlists.
    This token is not constant and should only last 1hour so it needs to be refreshed every hour. 
    """
    my_new_token = "BQBBbCnqP4chfD9Z3dRdCHuZtrkNwbMyovTGRoQh0QeVVEgLD_TRyKuyq3y6ZY-a9YHrsE1IKDC3aidSU67CU9lNJVTqSyCe0FprK5JZHXw3j__zsaetqkhZRc3WLp1U0vs_JCoDSPNXM6r8uezAY6gQry4W-bCVTGnzmbEp3l8Mp5ZQ8sAK_kT1dpB5Czd_ey1j_LlRJf9i4H8m34YCLsMilkJHQTFfTs8CDg"
    return {"Authorization": "Bearer " + my_new_token, "Content-Type": "application/json"}



def clean_string(s):
    """
    This function cleans a given string by removing all non-alphanumeric characters and converting it to lowercase.
    """
    return ''.join(e for e in s if e.isalnum()).lower()


def add_tracks(track_uri, playlist_id):
    """
    Adds a track to a Spotify playlist.

    Args:
        track_uri (str): The URI of the track to add.
        playlist_id (str): The ID of the playlist to add the track to.
        token (str): The authentication token for the Spotify API.

    Returns:
        The JSON response from the Spotify API.
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_token_post()

    # Encode the track URI using URL encoding
    encoded_track_uri = urllib.parse.quote(track_uri, safe='')

    query_uris = f"uris={encoded_track_uri}"
    query_full_url = url + "?" + query_uris
    response = post(query_full_url, headers=headers)
    response_json = response.json()


def find_spotify_track(song_name, artist_name, album_name, token):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_token(token)
    
    # Join the artist name words with '%20' to handle multiple words
    artist_name_query = artist_name.replace(" ", "%20")
    song_name_query = song_name.replace(" ", "%20")
    album_name_query = album_name.replace(" ", "%20")

    # Default query with album
    query = f"q=remaster%2520track%3A{song_name_query}%2520artist%3A{artist_name_query}%2520album%3A{album_name_query}&type=track&market=FR&limit=3"
    query_url = url + "?" + query
    response = get(query_url, headers=headers)
    # Check for API errors
    response.raise_for_status()
    
    json_response = json.loads(response.content)
    
    # Two cases : if track is found or not, with or without album filter
    if json_response["tracks"]["items"][0]["name"] != song_name:
        # Without album query
        query = f"q=remaster%2520track%3A{song_name_query}%2520artist%3A{artist_name_query}&type=track&market=FR&limit=3"
        query_url = url + "?" + query
        response = get(query_url, headers=headers)
        json_response = json.loads(response.content)
    
    track_name = json_response["tracks"]["items"][0]["name"]
    track_uri = json_response["tracks"]["items"][0]["uri"]
    
    # Write to CSV file based on whether the track name matches the provided song name
    if clean_string(track_name) == clean_string(song_name):
        add_tracks(track_uri, target_playlist_id)
    else:
        csv_file_name = f'{target_file_name}_excluded.csv'
        with open(csv_file_name, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([track_name, track_uri])


#Execute
token = get_token()

with open(f"{source_file_name}.csv", "r" , encoding="utf-8") as file:
    reader = csv.reader(file)
    # reader = list(reader)[:30]

    # Loop through each row in the CSV file
    for row in reader:
        # Get the song title and artist name from the row
        song_title = row[0]
        artist_name = row[1]
        album_name = row[2]
        print(song_title, artist_name)
        find_spotify_track(song_title, artist_name, album_name, token)