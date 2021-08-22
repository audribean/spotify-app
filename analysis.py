from dotenv import load_dotenv
load_dotenv()
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

"""
This file contains functions to determine what a typical mood will look
like according to Spotify's audio features. It can then filter through a user's
saved tracks and filter according to these audio features.

To-Do List:
- Adjust the algorithm for finding ideal attribute values
- Get the user's uri
- If the generated playlist is too short, pull songs from Spotify's recommended tracks
- Make a playlist function that will compile tracks from a particular period of time

"""

scope = "user-library-read"
auth_manager = SpotifyClientCredentials()
# for requests that don't require authentication (faster)
sp = spotipy.Spotify(auth_manager=auth_manager)
# for requests that require authentication
sp1 = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# class variables
class Track:
    energy = 0
    liveness = 0
    tempo = 0
    instrumentalness = 0
    danceability = 0
    loudness = 0
    valence = 0
    n = 1
    playlist = []

# two class instances for each playlist
calm = Track()
happy = Track()

# helper function: prints computed means of a playlist's features
def print_vals(track, type):
    print(type + " music values:\n" +
        "Energy: " + str(track.energy) + "\n" +
        "Liveness: " + str(track.liveness) + "\n" +
        "Tempo: " + str(track.tempo) + "\n" +
        "Instrumentalness: " + str(track.instrumentalness) + "\n" +
        "Danceability: " + str(track.danceability) + "\n" +
        "Loudness: " + str(track.loudness) + "\n" +
        "Valence: " + str(track.valence) + "\n")

# gets playlist IDs and prints their average features
def compute_calm():
    calm_id_1 = 'spotify:user:spotifycharts:playlist:7LI3zw8HLkjKo5YpvA26KG?si=462974e21f2243e8'
    calm_id_2 = 'spotify:user:spotifycharts:playlist:6vjh7HbGlTNEwy3nxj5rqj?si=6f1cb54e9cc04779'
    calm_id_3 = 'spotify:user:spotifycharts:playlist:1r4hnyOWexSvylLokn2hUa?si=90ac81d0bdb94bf2'
    calm_playlist_1 = sp.playlist(calm_id_1)
    calm_playlist_2 = sp.playlist(calm_id_2)
    calm_playlist_3 = sp.playlist(calm_id_3)
    compute_averages(calm, calm_playlist_1)
    compute_averages(calm, calm_playlist_2)
    compute_averages(calm, calm_playlist_3)
    print_vals(calm, "Calm")

# # gets playlist IDs and prints their average features
def compute_happy():
    happy_id_1 = 'spotify:user:spotifycharts:playlist:0lU86qLkSQVI991j4BUTDF?si=190e3e6c72d64b4e'
    happy_id_2 = 'spotify:user:spotifycharts:playlist:5yI34GDYLxUxfSrpshdNVE?si=8329487b21cd458a'
    happy_id_3 = 'spotify:user:spotifycharts:playlist:37i9dQZF1DX3rxVfibe1L0?si=e6f30eb51d504636'
    happy_playlist_1 = sp.playlist(happy_id_1)
    happy_playlist_2 = sp.playlist(happy_id_2)
    happy_playlist_3 = sp.playlist(happy_id_3)
    compute_averages(happy, happy_playlist_1)
    compute_averages(happy, happy_playlist_2)
    compute_averages(happy, happy_playlist_3)   
    print_vals(happy, "happy") 

# helper function: gets each track and keeps track of the tabulated averages
def compute_averages(track, playlist):
    tracks = playlist['tracks']['items']
    for item in range(len(tracks)):
        # take only the first 50
        if (track.n % 50 == 0):
            break
        # get track and audio features
        uri = tracks[item]['track']['uri']
        analysis = sp.audio_features(uri)
    # compute mean of each feature
    # TODO: something ~mysterious~ is going on with these numbers
        track.energy += analysis[0]['energy']
        track.liveness += track.liveness + analysis[0]['liveness']
        track.tempo += track.tempo + analysis[0]['tempo']
        track.instrumentalness += track.instrumentalness + analysis[0]['instrumentalness']
        track.danceability += track.danceability + analysis[0]['danceability']
        track.loudness += track.loudness + analysis[0]['loudness']
        track.valence += track.valence + analysis[0]['valence']
        track.n += 1
    track.energy /= track.n
    track.liveness /= track.n
    track.tempo /= track.n
    track.instrumentalness /= track.n
    track.danceability /= track.n
    track.loudness /= track.n
    track.valence /= track.n

# helper function: takes the track's array and makes it a playlist
# TODO: get the user uri and assign it to 'username'
def add_to_playlist(track):
    user = sp1.user(username)
    if (track == "calm"):
        title = "Your calming playlist"
        desc = "A playlist to wind down to, based on your favorite tracks"
    else:
        title = "Something upbeat"
        desc = "Your all-time favorite pick-me-ups"
    for item in track.playlist:
        new_pl = sp1.user_playlist_create(user, name=title, public=False, collaborative=False, description=desc)
        playlist_id = ''
        playlists = sp1.user_playlists(username)
        for item in playlists['items']: 
            if (item['name'] == title): 
                playlist_id = item['id']
                break
        sp1.user_playlist_add_tracks(username, playlist_id, track.playlist)

# Will gather user's library of saved songs and add those that meet a certain criterion
# into a new playlist
def make_playlist(genre):
    user_library = sp1.current_user_top_tracks(limit=50, offset=0, time_range="long_term")
    tracks = user_library['tracks']['items']
    if (genre == "calm"):
        track = calm
    else: track = happy
    for item in range(len(tracks)):
        # get track and audio features
        uri = tracks[item]['track']['uri']
        analysis = sp.audio_features(uri)
        # add uri to array if it fits criteria
        if ((track.energy - 0.1 > analysis[0]['energy']) | (analysis[0]['energy'] > track.energy + 0.1)):
            break
        if ((track.liveness - 0.1 > analysis[0]['liveness']) | (analysis[0]['liveness'] > track.liveness + 0.1)):
            break
        if ((track.liveness - 15 > analysis[0]['tempo']) | (analysis[0]['tempo'] > track.tempo + 15)):
            break
        if ((track.instrumentalness - 15 > analysis[0]['instrumentalness']) | (analysis[0]['instrumentalness'] > track.instrumentalness + 15)):
            break
        if ((track.danceability - 0.1 > analysis[0]['danceability']) | (analysis[0]['danceability'] > track.danceability + 0.1)):
            break
        if ((track.loudness - 15 > analysis[0]['loudness']) | (analysis[0]['loudness'] > track.loudness + 15)):
            break
        if ((track.valence - 0.1 > analysis[0]['valence']) | (analysis[0]['valence'] > track.valence + 0.1)):
            break
        else:
            track.playlist.append(uri)
            add_to_playlist(track)

# In case authentication goes wack again, one of these should do it

#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
#client_credentials_manager = SpotifyClientCredentials()
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
#token = os.environ.get("SPOTIPY_CLIENT_SECRET")
#sp = spotipy.Spotify(auth = token)