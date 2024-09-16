# Pseudocode and TODOs

# 1
# given one Artist name and Album title, retrieve album info
# output the number of tracks and the length of album

# 2
# given multiple Artist names and Album titles in a CSV (10), retrieve album info
# output the average length (calculate), and visualize number of tracks as a bar graph

from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# load env variables
load_dotenv()

# get the client id and secret from the env
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

# set up spotipy with my client credentials. use the sp object to call methods / interact with the api
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# function that takes in album and artist, and outputs the album info
def get_album_info(album_title, artist_name):
    query = f'album:{album_title} artist:{artist_name}' # spotify api syntax for this search query
    result = sp.search(q=query, type='album', limit=1) # returns the album, 1
    
    if result['albums']['items']:
        # parse JSON to get the first (and only) album for its info
        album = result['albums']['items'][0]

        # extract details from JSON and put into new dict of info for the album
        return {
            'album_name': album['name'],
            'album_id': album['id'],
            'artist_name': album['artists'][0]['name'], #this is just 1 artist for now, but later can make a list if theres multiple primary artists
            'release_date': album['release_date'],
            'total_tracks': album['total_tracks'],
            'uri': album['uri']
        }
    else:
        return "Album not found"
    

if __name__ == "__main__":
    print(get_album_info('GUTS','Olivia Rodrigo'))