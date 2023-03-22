import requests
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyOAuth


scope = "playlist-modify-private"
client_id = "332bf88c56a6435092b3dcd3afdd6bda"
client_secret = "93d45f8158d9407aa4bbc370de888422"
client_redirect_uri = "https://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=client_redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
 
user_id = sp.current_user()["id"]


date = input("Which year would you like to travel to? Write the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]

bb_url = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(url= bb_url)
data = response.text

soup = BeautifulSoup(data, "html.parser")
no1 = soup.find(name= "h3").getText().strip()
title_data = soup.find_all(name= "h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")

titles = [no1]
for title in title_data:
    titles.append(title.getText().strip())


track_uris = []
for track in titles:
    data = sp.search(q= f"track: {track}", limit= 1)
    track_uri = data["tracks"]["items"][0]["uri"]
    track_uris.append(track_uri)


playlist = sp.user_playlist_create(user= user_id, name= f"{date} Billboard 100", public= False)
playlist_id = playlist["id"]
result = sp.playlist_add_items(playlist_id= playlist_id, items= track_uris)
print(result)