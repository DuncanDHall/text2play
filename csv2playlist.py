import spotipy.util
from datetime import datetime

USERNAME = 'redunculous'

CLIENT_ID = '04102ce6ed0b4180be572833329f27de'
CLIENT_SECRET = open('spotify_key').read().strip()
SCOPE = 'user-library-read playlist-modify-public playlist-modify-private'


def get_service():
    token = spotipy.util.prompt_for_user_token(
        USERNAME, SCOPE,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='http://localhost:8888/callback'
    )
    if not token:
        raise Exception("Can't get token for ", USERNAME)

    service = spotipy.Spotify(auth=token)
    return service


def new_playlist(name, service):
    r = service.user_playlist_create(USERNAME, name)
    return r['id']


def playlist_from_csv(filepath, service):
    with open(filepath, 'r') as csvf:
        for title, artist in csvf.readlines():
            print(title, " by ", artist)


def get_file_name():
    t = 'playlists/{}-{}-{}_merge.csv'
    d = datetime.today()
    return t.format(d.year, d.month, d.day)


def main():
    service = get_service()
    playlist_from_csv(get_file_name(), service)


if __name__ == "__main__":
    main()
