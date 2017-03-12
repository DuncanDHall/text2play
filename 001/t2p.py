
username='redunculous'

createNewPlaylist = True
newPlaylistName = 'Kyle LaPatin WCS 2016'

clientID = '04102ce6ed0b4180be572833329f27de'
clientSecret = open('key').read().strip()

dataFile = '/Users/duncan/Desktop/WCS/playlists/KyleWCS2016.csv'
delim = ','

import sys
import spotipy
import spotipy.util as util
import requests

scope = 'user-library-read playlist-modify-public playlist-modify-private'

data = open(dataFile).readlines()

token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret,redirect_uri='http://localhost:8888/callback')
myAuth = "Bearer " + token

notFound = []

if not token:
    raise Exception("Can't get token for", username)

sp = spotipy.Spotify(auth=token)

r = sp.user_playlist_create(username, newPlaylistName, False)
playlistID = r['id']

for line in data:
    l = line.split(delim)
    artist, title, playCount = l[:3]
    r = sp.search(title)

    if playCount <= 5:
        print title + " by " + artist + " skipped (low play count)"
        continue

    found = False
    for track in r['tracks']['items']:
        if track['artists'][0]['name'].lower() in artist.lower().split(' & '):
            trackID = track['id']
            found = True
            break
    
    if not found:
        notFound.append(title + delim + artist)
        print title + " by " + artist + " not found..."
    
    else:
        print title + " by " + artist + " added..."
        requests.post("https://api.spotify.com/v1/users/"+username+"/playlists/"+ playlistID +"/tracks?position=0&uris=spotify%3Atrack%3A"+trackID,headers={"Authorization":myAuth})


print "\n Songs not added: "
for song in notFound:
    print line           

