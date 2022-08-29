import requests
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
URL = "https://www.billboard.com/charts/hot-100"
SONG_URIS = []

# ********************************* Data from BillBoards ************************************* #

date = input("Which year top 100 songs do you want to listen? Type the date in this format YYYY-MM-DD: ")
year = date.split('-')[0]

response = requests.get(url=f"{URL}/{date}")
data = response.text
soup = BeautifulSoup(data, "html.parser")
filtered_list = [(song.get_text()).split() for song in soup.select("h3" ".c-title" ".a-no-trucate" 
                                                                   ".a-font-primary-bold-s" "#title-of-a-story")]

song_list = []

for song in filtered_list:
    if len(song) > 1:
        song_list.append(' '.join(song))
    else:
        song_list.append(song)

# ********************************* Spotify Autentication ************************************* #
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                               client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=os.getenv('redirect_uri'),
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))

# ********************************* Searching Songs ************************************* #
for song in song_list:
    result = sp.search(q=f'track:{song} year:{year}', type='track')

    try:
        uri = result['tracks']['items'][0]['uri']
    except IndexError:
        print(f"{song} doesn't exist in spotify.")

    else:
        SONG_URIS.append(uri)

# ********************************* Creating Playlist ************************************* #


user_id = sp.current_user()["id"]
my_playlist = sp.user_playlist_create(user=f"{user_id}", name=f"{year}'s Billboard Top Tracks", public=False,
                                      description="Top Tracks from back in the Days of Brunel")
playlist_id = my_playlist['id']

# ********************************* Adding songs to playlist ************************************* #

post_spotify = sp.playlist_add_items(playlist_id=playlist_id, items=SONG_URIS)
print(post_spotify)
