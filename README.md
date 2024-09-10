This personal project is designed to facilitate the transfer of tracks from Deezer Playlists to personal Spotify Playlists using the Spotify API.

# Important Notes :
- Source Media Streaming: This project is not limited to Deezer as the source media streaming service because it does not rely on the source media streaming API. However, to use this tool, you will need a CSV file similar to the example provided in the repository ("csv_example.csv"). Such a file can be created using external services like "Tune My Music". The CSV file should contain the following information for each track, in this order: song_name, artist_name, album_name. Additional information can be included, but it is not necessary for the tool to function.
- Spotify API Limitations: The Spotify API, particularly the "search" endpoint, is not perfect and may not always accurately find the correct track, even if it is easily discoverable on the Spotify app. Therefore, please be aware that there is a high possibility that not all tracks from your source playlist will be successfully exported to Spotify. Some manual addition of tracks may be required.
- Make sure all your spotify playlists are private !
- 
# How to use : 
1) Clone this project in your VSCode.
2) Go to Spotify API page : https://developer.spotify.com/documentation/web-api, and create an App by following the tutorial of their page.
3) When your App is created, go to the settings of your App (still in the Spotify API page) to get your client_id and client_secret. Then, copy paste them in the .env file of the project. DO NOT SHARE THEM PUBLICLY.
4) Create a CSV file for each of your source playlists. Don't bother to put them in a subfolder, just add them in the same root folder as the .py files.
5) Make sure to install all python modules needed :
  - os
  - base64
  - requests
  - json
  - urlib.parse
  - csv
  - dotenv
  - webbrowser
6) You can now start running the code. Begin with RefreshAccessToken1.py. Edit the redirect_url as indicated in the file.
7) Run the script. It will open a Spotify web page asking you to log in to your Spotify account. After logging in, you will be redirected to an error page. This is expected; what you need is the new URL of the page. Copy the entire URL.
8) Go to RefreshAccessToken2.py, paste the URL in my_url_from_previous_step. Run this file.
9) In your console, you should see an access_token displayed. Copy this token. Then, proceed to ToSpotify.py. WARNING: The access_token you just generated is only valid for 1 hour. After that, you will need to repeat steps 7 to 9 (you do not need to modify the redirect_url again).
10) With your access_token, paste it in the function get_auth_token_post() just as indicated.
11) Make sure to edit your : 
- source_file_name = "MyPlaylist"
- target_file_name = "MyPlaylistSpotify"
- target_playlist_id = "to fill with playlist id"
12) Run this file. Done !
13) The file will probably generate another CSV file called '{target_file_name}_excluded.csv', this file contains all the tracks that were not found using the Spotify API.
