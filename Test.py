import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

API_return_codes = {204: "Success!", 401: "Token Problem", 403: "Bad OAuth Request", 404: "wut",
                    429: "Rate Limit Exceeded"
                    }
allowed_inputs = "play", "pause", "see", "next", "previous"
scope = "user-read-playback-state,user-read-currently-playing,user-modify-playback-state"

os.environ["SPOTIPY_CLIENT_ID"] = "9e31ba09c77c4351884da2e51f35d7ca"
os.environ["SPOTIPY_CLIENT_SECRET"] = "e7259bb4be87456c860223a5afcfe8e2"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:9090"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-read-playback-state,user-read-currently-playing,user-modify-playback-state"))
get_token = spotipy.oauth2.SpotifyOAuth(scope=scope)
token = get_token.get_access_token(code=None, as_dict=False, check_cache=True)


# print(token)
def check_play_status():
    currently_playing_URL = "https://api.spotify.com/v1/me/player/"
    play_status_string = requests.get(currently_playing_URL, headers={"Authorization": f"Bearer {token}"}
                                      )
    play_status_return = play_status_string.json()
    return (play_status_return['is_playing'])


while True:
    user_in = input("do you want to 'play', 'pause', 'next', 'previous' or 'see' status?: ")

    if user_in == "see":
        currently_playing_URL = "https://api.spotify.com/v1/me/player/"
        play_status_string = requests.get(currently_playing_URL, headers={"Authorization": f"Bearer {token}"}
                                          )
        play_status_return = play_status_string.json()
        if check_play_status() == True:
            print("Spotify is currently playing", (play_status_return['item']['name']), "by",
                  (play_status_return['item'] \
                      ['artists'][0]['name']), "on", (play_status_return['device']['name']))
        elif play_status_return['is_playing'] == False:
            print("Spotify is not currently playing")

    if user_in == "pause" or "play":
        if check_play_status() == True and user_in == "pause" or check_play_status() == False and user_in == "play":
            pause_URL = f"https://api.spotify.com/v1/me/player/{user_in}"
            pause_string = requests.put(pause_URL,
                                        headers={"Authorization": f"Bearer {token}"})
            returned_code = pause_string.status_code
            print(API_return_codes[returned_code])
            print(returned_code)
        elif user_in == "pause":
            print("Already Paused!")
        elif user_in == "play":
            print("Already Playing!")

    elif user_in == "next" or "previous":
        pause_URL = f"https://api.spotify.com/v1/me/player/{user_in}"
        pause_string = requests.post(pause_URL,
                                     headers={"Authorization": f"Bearer {token}"})
        returned_code = pause_string.status_code
        print(API_return_codes[returned_code])

    else:
        print("somehow hit the end?")
