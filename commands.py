import os
import sys
import time
import webbrowser
import subprocess
import platform
import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from word2number import w2n
from utils import get_local_time, is_morning, start_timer, open_app

load_dotenv()

def handle_stop(speak, my_name):
    line = f"Goodbye, {my_name}"
    speak(line)
    sys.exit()


def handle_time(speak):
    time_str = get_local_time()
    time_indicator = "AM" if is_morning() else "PM"
    line = time_str + " " + time_indicator
    speak(line)

def _wait_for_spotify_device(spotify, timeout=10, interval=1):
    """Poll for a Spotify Connect device to become available, returning its id or None."""
    elapsed = 0
    while elapsed < timeout:
        try:
            devices = spotify.devices().get("devices", [])
        except Exception:
            devices = []

        if devices:
            active = next((d for d in devices if d.get("is_active")), devices[0])
            return active["id"]

        time.sleep(interval)
        elapsed += interval

    return None


# must have Spotify
def handle_play_music(speak, listen):
    speak("Do you have a specific song you want or arist you want?")
    response = listen()

    yes_phrases = ["yes", "yeah", "yea", "sure"]

    open_app("Spotify")
    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    try:
        spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="user-library-read user-modify-playback-state user-read-playback-state"
        ))
    except Exception:
        speak("I couldn't connect to Spotify")
        return

    speak("Opening Spotify...")

    device_id = _wait_for_spotify_device(spotify)
    if not device_id:
        speak("I couldn't find an active Spotify device. Make sure Spotify is open and try again.")
        return

    if response.lower() in yes_phrases:
        speak("What song or artist would you like to hear?")
        query = listen()

        if not query:
            speak("I didn't catch a song or artist name")
            return

        try:
            results = spotify.search(q=query, type="track", limit=1)
            tracks = results["tracks"]["items"]
        except Exception:
            speak("Something went wrong searching Spotify")
            return

        if not tracks:
            speak(f"I couldn't find anything for {query}")
            return

        uri = tracks[0]["uri"]
        speak(f"Playing {tracks[0]['name']}")
        spotify.start_playback(device_id=device_id, uris=[uri])
    else:
        speak("Playing a random song of my choice")

        try:
            results = spotify.current_user_saved_tracks(limit=50)
            liked_tracks = results["items"]
        except Exception:
            speak("Something went wrong getting your saved tracks")
            return

        if not liked_tracks:
            speak("You don't have any saved tracks to choose from")
            return

        random_track = random.choice(liked_tracks)
        uri = random_track["track"]["uri"]
        spotify.start_playback(device_id=device_id, uris=[uri])


def handle_skip_track(speak, listen):
    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    try: 
        spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=spotify_client_id, 
            client_secret=spotify_client_secret, 
            redirect_uri="http://127.0.0.1:8888/callback", 
            scope="user-modify-playback-state"
        ))
    except Exception as error:
        speak("I couldn't conncet to spotify")
        return
    
    speak("Skipping track")
    spotify.next_track()
    
def handle_say_name(speak, my_name):
    line = f"You asked my to call you {my_name}"
    speak(line)

# TODO: add more error handling + get list of applicaitons in /Applications folder
def handle_open_app(speak, listen):
    speak("What app to you want to open?")
    app_name = listen()

    if len(app_name) > 0:
        speak(f"Opening {app_name}")
        open_app(app_name)
    else:
        speak("Cannot find that app name")


def handle_open_website(speak, listen):
    speak("What website would you like to open?")
    website_name = listen()

    # TODO: add support for other top level domains like .org
    if len(website_name) > 0:
        speak("Opening website")
        url = f"https://{website_name}.com"
        webbrowser.open(url)
    else:
        speak("Cannot find that website")

def handle_change_name(speak, listen, my_name):
    line = f"You current name is {my_name}, what would you like to change it to?"
    speak(line)
    new_name = listen()
    is_valid = False

    while is_valid == False:
        line = f"Please say confirm to verify you want to change your name to {new_name}"
        speak(line)
        response = listen()

        if response.lower() == "confirm":
            line = f"Confirmed, {new_name}"
            speak(line)
            is_valid = True
            my_name = new_name
            return my_name
        else:
            line = f"Please say another name"
            speak(line)
            new_name = listen()


def handle_ai(speak, listen, get_ai_response):
    speak("Optimizing responses...what do you need?")
    voice_text = listen()

    # verify what this length needs to be
    if len(voice_text) >= 150:
        speak("Too long of a question, please shortern for optimized responses")
        return

    # add error handling
    response = get_ai_response(voice_text)
    speak(response)


def handle_create_file(speak, listen):
    speak("What would you like the name of the file to be")
    file_name = listen()
    confirmed = False

    # only creates txt file in this directory
    while confirmed == False:
        line = f"Say confirm to verify this is the correct name: {file_name}"
        speak(line)
        response = listen()

        if response.lower() == "confirm":
            confirmed = True
            speak("Filename confirmed, creating file")
        else:
            speak("What would you like to rename the file then?")
            file_name = listen()

    speak("What would you like the file to say?")
    file_content = listen()

    file_name = file_name + ".txt"
    with open(file_name, "w") as file:
        file.writelines(file_content)
        file.writelines('\n')

    line = f"File {file_name} successfully created"
    speak(line)


def handle_open_file(speak, listen):
    speak("What text file would you like to open in this directory?")
    file_name = listen()
    file_name = file_name + ".txt"

    try:
        # only opens a txt file in this directory
        with open(file_name, "r") as file:
            file_content = file.read()

        line = f"Opening file...reading contents: {file_content}. Closing file"
        speak(line)
    except FileNotFoundError:
        speak("I was unable to locate that file")


def handle_timer(speak, listen):
    speak("How long would you like your timer to go for?")
    response = listen()
    # TODO: add regex to ensure format
    response = response.strip()

    has_hour, has_minute, has_seconds = False, False, False
    hour, minute, seconds = 0, 0, 0
    hour_index, minute_index, seconds_index = 0, 0, 0
    hour_str, minute_str, seconds_str = "", "", ""

    if response.find("hour") != -1 or response.find("hours") != -1:
        has_hour = True
        if response.find("hour") != -1:
            hour_index = response.find("hour")
        else:
            hour_index = response.find("hours")

    if response.find("minute") != -1 or response.find("minutes") != -1:
        has_minute = True
        if response.find("minute") != -1:
            minute_index = response.find("minute")
        else:
            minute_index = response.find("minutes")

    if response.find("second") != -1 or response.find("seconds") != -1:
        has_seconds = True
        if response.find("second") != -1:
            seconds_index = response.find("second")
        else:
            seconds_index = response.find("seconds")

    if has_hour:
        hour_str = response[0:hour_index]
        hour_str = hour_str.strip()
        # remove first number then remove hour str
        response = response[hour_index:len(response)]
        response = response[response.find(" "):len(response)]
        response = response.strip()

    '''
    I don't think I need to use minute_index here
    regardless of has_hour minute would be the first item in the str
    if we have an hour or not
    '''
    if has_minute:
        minute_str = response[0:response.find(" ")]
        minute_str = minute_str.strip()
        # delete the next two words which should be like "ten minute"
        response = response[response.find("m"):len(response)]
        response = response[response.find(" "):len(response)]
        response = response.strip()

    if has_seconds:
        seconds_str = response[0:response.find("s")]
        seconds_str = seconds_str.strip()

    def parse_num(word_str):
        try:
            return w2n.word_to_num(word_str) if word_str != "" else 0
        except ValueError:
            return 0

    hour = parse_num(hour_str)
    minute = parse_num(minute_str)
    seconds = parse_num(seconds_str)

    if hour == 0 and minute == 0 and seconds == 0:
        speak("I didn't catch a valid time for the timer")
        return

    start_timer(hour, minute, seconds)
    speak("Timer done")
