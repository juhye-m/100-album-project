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

def format_duration(duration_ms):
    seconds = (duration_ms // 1000) % 60
    minutes = (duration_ms // (1000 * 60)) % 60
    hours = (duration_ms // (1000 * 60 * 60))
    return f"{hours}:{minutes:02}:{seconds:02}"

def get_tracks_for_album(album_id):
    album_tracks = sp.album_tracks(album_id)
    return album_tracks['items']

# function that takes in album and artist, and outputs the album info
def get_album_info(album_title, artist_name):
    query = f'album:{album_title} artist:{artist_name}' # spotify api syntax for this search query
    result = sp.search(q=query, type='album', limit=1) # returns the album, 1
    
    # print(result)
    if result['albums']['items']:
        # parse JSON to get the first (and only) album for its info
        album = result['albums']['items'][0]
        album_id = album['id']

        # detailed info like genre and popularity
        album_details = sp.album(album['id'])
        print(album_details['popularity'])
        # print(album_details['genres'])

        # Get album tracks
        tracks = get_tracks_for_album(album_id)

        # track duration sum for album duration
        track_durations = [track['duration_ms'] for track in tracks]
        total_duration_ms = sum(track_durations)

        # extract details from JSON and put into new dict of info for the album
        album_data = {
            'album_name': album['name'],
            'album_id': album['id'],
            'artist_name': album['artists'][0]['name'], #this is just 1 artist for now, but later can make a list if theres multiple primary artists
            'release_date': album['release_date'],
            'total_tracks': album['total_tracks'],
            'duration': format_duration(total_duration_ms),
            'genres': album.get('genres', []), #avoid error if no genres specified
            'popularity': album_details['popularity'],
            'uri': album['uri']
        }
        return album_data
    else:
        return None

def get_song_features(track_id):
    song_features = sp.audio_features(track_id)
    return song_features[0] if song_features else None

# this is a list of dicts, and which track it comes from is unspecified
def get_all_audio_features(track_ids):
    features_list = []
    for track_id in track_ids:
        features = get_song_features(track_id)
        if features:
            features_list.append(features)
    return features_list

def read_csv(file_path):
    return pd.read_csv(file_path)

def main():
    # csv file path
    csv_file_path = 'albums.csv'

    # read csv into pandas dataframe
    df = read_csv(csv_file_path)

    # process the df 
    album_data_list = []
    # go through each row of the df (each album) and get the data 
    for index, row in df.iterrows():
        album_title = row['album_title']
        artist_name = row['artist_name']

        album_data = get_album_info(album_title, artist_name)

        if album_data:
            track_ids = [track['id'] for track in get_tracks_for_album(album_data['album_id'])]
            audio_features = get_all_audio_features(track_ids)
            album_data['audio_features'] = audio_features  # Store audio features in the album data
            album_data_list.append(album_data)

    # convert this album data list to a new df with all the info it pulled
    album_data_df = pd.DataFrame(album_data_list)

    # here, we can analyze the data or do more with it
    print(album_data_df)
    # output the average length (calculate)
        # Calculate average album length
    # if not album_data_df.empty:
    #     average_length = album_data_df['total_duration_min'].mean()
    #     print(f'Average album duration: {average_length:.2f} minutes') # add a MM:SS function later
    # else:
    #     print('No album data available.')

    # access genre by album name
    # album_name = 'GUTS'
    # first_album_genre = album_data_df[album_data_df['album_name'] == album_name]['genres'].values[0]
    # print(first_album_genre)


if __name__ == "__main__":
    main()