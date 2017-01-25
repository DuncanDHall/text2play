
username='redunculous'

createNewPlaylist = True
newPlaylistName = 'Kyle LaPatin WCS 2016'

clientID = '04102ce6ed0b4180be572833329f27de'
clientSecret = open('key').read()
print clientSecret

dataFile = '/Users/duncan/Desktop/WCS/playlists/KyleWCS2016.csv'

import sys
import spotipy
import spotipy.util as util
import requests

scope = 'user-library-read playlist-modify-public playlist-modify-private'

data = open(dataFile).readlines()

token = util.prompt_for_user_token(username, scope)
myAuth = "Bearer " + token

notFound = []

if token:
    sp = spotipy.Spotify(auth=token)

    r = sp.user_playlist_create(username, newPlaylistName, False)
    playlistID = ['id']

    for line in data:
        print line
