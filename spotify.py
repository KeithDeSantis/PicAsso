from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from config import *
import requests
import spotipy
import json
import sys
import os

# Spotify Connection Object
scope = "user-library-read"
SP = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

song_file_path = "resources/songs.json"


''' Given a limit and offset write the liked songs to the JSON '''
def write_songs_to_json(limit, offset):
    results1 = SP.current_user_saved_tracks(limit=limit, offset=offset)
    s = open(song_file_path, 'w')
    json_object = json.dumps(results1,indent=4)
    s.write(json_object)

''' Save the album covers from the JSON urls for now goes to IMAGES2 '''
def save_images_from_json():
    s = open(song_file_path, 'r')
    json_dict = json.load(s)
    songs = json_dict['items']
    image_urls = []

    for song in songs:
        try:
            image_urls.append(song['track']['album']['images'][1]['url']) # gets the 300x300 url
        except:
            pass

    for url in image_urls:
        img_data = requests.get(url).content
        name = url.split('/')[-1]
        with open(f'images_main/{name}.jpg', 'wb') as handler:
            handler.write(img_data)

''' Get track images from a playlist '''
def user_playlist_tracks_full_to_json(limit, offset, playlist_id=None, fields=None, market=None):

    # first run through also retrieves total no of songs in library
    response = SP.user_playlist_tracks(user=SP.current_user(), playlist_id=playlist_id, fields=fields, limit=limit, offset=offset, market=market)
    s = open(song_file_path, 'w')
    json_object = json.dumps(response,indent=4)
    s.write(json_object)

''' Get the number of songs in a list of songs in order to choose iterations of Spotify API calls'''
def get_num_songs(playlist_id=None):
    # Liked Songs
    if(playlist_id == None):
        results = SP.current_user_saved_tracks(limit=1)
    # Playlist
    else:
        results = SP.user_playlist_tracks(user=SP.current_user(),playlist_id=playlist_id)
    return results['total']


if __name__ == "__main__":

    #! Call this script to load in album images to 'images_main' directory
    # Defaults to loading liked songs
    # If command line argument is 'p', 'P', 'playlist', 'Playlist', or 'PLAYLIST' then it 
    # will load from a playlist based on the playlist ID given as the second arg
    
    # Uses:
    # DEFAULT: python spotify.py
        # Loads liked songs
    # PLAYLIST: python playlist <playlist_id>

    # Clear old images
    for img in os.listdir('./images_main'):
        if(img != '.gitignore'):
            os.remove('./images_main/' + img)

    playlist_args = ['P', 'PLAY', 'PLAYLIST']

    # Are we loading from a playlist?
    if len(sys.argv) > 1:
        if (sys.argv[1].upper() in playlist_args):
            try:
                number_songs = get_num_songs(playlist_id=sys.argv[2])
                iterations = number_songs//50
                remainder = number_songs%50
                for it in range(iterations):
                    try:
                        user_playlist_tracks_full_to_json(50,it*50, sys.argv[2])
                        save_images_from_json()
                    except:
                        pass
                if(remainder > 0):
                    user_playlist_tracks_full_to_json(remainder, iterations*50, sys.argv[2])
                    save_images_from_json()
            except:
                print('Please provide a playlist id to load from.')
                exit()


    # Other wise load liked songs
    else:
        number_songs = get_num_songs()
        iterations = number_songs//50
        remainder = number_songs%50
        for it in range(iterations):
            write_songs_to_json(50,it*50)
            save_images_from_json()
        if(remainder > 0):
            write_songs_to_json(remainder,iterations*50)
            save_images_from_json()