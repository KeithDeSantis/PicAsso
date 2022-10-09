import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import *
import random
from spotipy.oauth2 import SpotifyOAuth
import json
import requests

scope = "user-library-read"
SP = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))


''' Given a limit and offset write the liked songs to the JSON '''
def write_songs_to_json(limit, offset):
    results1 = SP.current_user_saved_tracks(limit=limit, offset=offset)
    s = open('songs.json', 'w')
    json_object = json.dumps(results1,indent=4)
    s.write(json_object)


''' Save the album covers from the JSON urls for now goes to IMAGES2 '''
def save_images_from_json():
    s = open('songs.json', 'r')
    json_dict = json.load(s)
    songs = json_dict['items']
    image_urls = []

    for song in songs:
        image_urls.append(song['track']['album']['images'][1]['url']) # gets the 300x300 url


    for url in image_urls:
        img_data = requests.get(url).content
        name = url.split('/')[-1]
        with open(f'images_main/{name}.jpg', 'wb') as handler:
            handler.write(img_data)


def user_playlist_tracks_full(limit, offset, playlist_id=None, fields=None, market=None):

    # first run through also retrieves total no of songs in library
    response = SP.user_playlist_tracks(user=SP.current_user(), playlist_id=playlist_id, fields=fields, limit=limit, offset=offset, market=market)
    s = open('songs.json', 'w')
    json_object = json.dumps(response,indent=4)
    s.write(json_object)