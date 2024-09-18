# Pseudocode and TODOs

# 2
# given multiple Artist names and Album titles in a CSV, retrieve album info
# output the average length (calculate), and visualize number of tracks as a bar graph

from dotenv import load_dotenv
import os
import pandas as pd
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
        return None #or should I use "album not found"?


def main():
    # csv file path
    csv_file_path = 'albums.csv'

    # read csv into pandas dataframe
    df = pd.read_csv(csv_file_path)

   
    # process the df 
    album_data_list = []
    # go through each row of the df (each album) and get the data 
    for index, row in df.iterrows():
        album_title = row['album_title']
        artist_name = row['artist_name']

        album_data = get_album_info(album_title, artist_name)

        if album_data:
            album_data_list.append(album_data)

    # convert this album data list to a new df with all the info it pulled
    album_data_df = pd.DataFrame(album_data_list)

    # here, we can analyze the data or do more with it
    print(album_data_df)

if __name__ == "__main__":
    main()