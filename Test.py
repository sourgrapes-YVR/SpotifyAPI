import PySimpleGUI as sg
import gpiozero
from gpiozero import RotaryEncoder, Button
from gpiozero.pins.mock import MockFactory
from PIL import Image
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

gpiozero.Device.pin_factory=MockFactory()
button = Button(21, pull_up=False)

API_return_codes = {204: "Success!", 401: "Token Problem", 403: "Bad OAuth Request", 404: "wut",
                    429: "Rate Limit Exceeded"
                    }

album_art = "/Users/davidbrown/PycharmProject/APITutorial/album_arts/newart.png"

# setup for OAuth
scope = "user-read-playback-state,user-read-currently-playing,user-modify-playback-state"
mac_device_id = "0e8b0d59abe381876a84d31bb2a2ce00ec1bd1d7"
os.environ["SPOTIPY_CLIENT_ID"] = "9e31ba09c77c4351884da2e51f35d7ca"
os.environ["SPOTIPY_CLIENT_SECRET"] = "e7259bb4be87456c860223a5afcfe8e2"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:9090"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-read-playback-state,user-read-currently-playing,user-modify-playback-state"))
get_token = spotipy.oauth2.SpotifyOAuth(scope=scope)
token = get_token.get_access_token(code=None, as_dict=False, check_cache=True)


def check_play_status():
    play_status_return = sp.current_playback()
    # print(play_status_return)
    return play_status_return['is_playing']


def see_currently_playing():
    play_status_string = sp.current_playback()
    if check_play_status() is True:
        return f"Spotify is currently playing {(play_status_string['item']['name'])} by {(play_status_string['item']['artists'][0]['name'])} on {(play_status_string['device']['name'])}"
    elif check_play_status() is False:
        return"Spotify is not currently playing"


def get_album_art():
    play_status_string = sp.current_playback()
    album_art_url = (play_status_string['item']['album']['images'])[2]['url']
    img_jpg = Image.open(requests.get(album_art_url,stream=True).raw)
    img_jpg.save("/Users/davidbrown/PycharmProject/APITutorial/album_arts/newart.png")
    return img_jpg

def play_pause():
    if check_play_status() is True:
        sp.pause_playback()
        # print("paused")
    elif check_play_status() is False:
        sp.start_playback(device_id=mac_device_id)

display_elements = [("current_play",see_currently_playing())]
def update_elements():
    for element,target in display_elements:
        window[element].update(target)
    print("done")


sg.theme("Default1")
sg.theme_button_color("#FFFFFF")
sg.theme_background_color("#1DB954")
sg.theme_text_color("#FFFFFF")
sg.theme_text_element_background_color("#1DB954")
layout = [  [sg.Text(see_currently_playing(), key="current_play"), sg.Image(album_art, key="album_art")],
            [sg.Text('What do?')],
            [sg.Button("Play/Pause", key="pp"), sg.Button("Skip", key="next"), sg.Button("Previous", key="previous"), sg.Button("Cancel")]   ]

window = sg.Window("Spotify Controller", layout, default_element_size=(200,2))

while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Cancel":
        break

    button.when_pressed = play_pause


    if user_in == "pp":
        if check_play_status() is True:
            sp.pause_playback()
            # print("paused")
        elif check_play_status() is False:
            sp.start_playback(device_id=mac_device_id)
            # print("playing")

    elif user_in == "next":
        sp.next_track()
        # print("skipped forward")

    elif user_in == "previous":
        sp.previous_track()


    window["current_play"].update(see_currently_playing())
    get_album_art()
    window["album_art"].update(album_art)
