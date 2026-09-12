# openai whisper can be used offline voice recognition
import random
import pyttsx3
import os
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI
from utils import is_morning
from commands import (
    handle_stop,
    handle_time,
    handle_say_name,
    handle_change_name,
    handle_ai,
    handle_create_file,
    handle_open_file,
    handle_timer,
    handle_open_website,
    handle_open_app, 
    handle_play_music, 
    handle_skip_track,
)

# setup
print("Booting up Jarvis...")
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
ai_bot = OpenAI(api_key=openai_api_key)
recognizer = sr.Recognizer()
my_name = "Mr. Bibb"
ai_cache = {}

# functions
def get_ai_response(prompt):
    prompt = prompt.lower()

    if prompt in ai_cache.keys():
        print("Returning caches prompt")
        return ai_cache[prompt]
    
    # $0.20/1M output tokens -> each reponse probably costs a fraction of a cent
    response = ai_bot.chat.completions.create(
        model="gpt-4o-mini",  # cheap, fast model
        messages=[
            {"role": "system", "content": "My name is Mr. Bibb. You are Jarvis, a helpful assistant similar to Tony Stark's, aka Iron Man's Jarvis."},
            {"role": "user", "content": prompt}
        ]
    )

    print("Caching response")
    response = response.choices[0].message.content
    ai_cache[prompt] = response 

    return response

def listen():
    print("Listening...")
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
    except Exception as error:
        print(f"Some error has occured: {error}")

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}")
        return ""
    except sr.WaitTimeoutError:
        print("Listening timed out")
        return ""

def speak(line):
    print("Speaking...")
    voice_engine = pyttsx3.init()
    voice_id = 'com.apple.voice.compact.en-GB.Daniel'
    voice_engine.stop()
    voice_engine.setProperty('voice', voice_id)
    voice_engine.say(line)
    voice_engine.runAndWait()

def determine_line():
    global my_name
    time_of_day = "morning" if is_morning() else "afternoon"
    intro_lines = [
        f"Hello, how can I help you today, {my_name}?", 
        "What can I help you with today, sir?", 
        f"Welcome, {my_name}, is there anything you need?", 
        f"Good {time_of_day}, {my_name} what can I help you with today?"]
    speak(random.choice(intro_lines))
    voice_text = listen()
    print(f"Voice text: {voice_text}")
    try:
        # turn jarvis off
        stop_phrases = ["stop", "turn off", "shut down", "shut off"]
        if voice_text.lower() in stop_phrases:
            handle_stop(speak, my_name)
            return

        # get the time
        time_phrases = ["time", "what time is it"]
        if voice_text.lower() in time_phrases:
            handle_time(speak)
            return

        # say my name
        say_name_phrases = ["what's my name", "what is my name"]
        if voice_text.lower() in say_name_phrases:
            handle_say_name(speak, my_name)
            return

        # change my name
        change_name_phrases = ["change my name"]
        if voice_text.lower() in change_name_phrases:
            my_name = handle_change_name(speak, listen, my_name)
            return

        # ai responses
        ai_phrases = ["optimize"]
        if voice_text.lower() in ai_phrases:
            handle_ai(speak, listen, get_ai_response)
            return

        # creating a text file
        create_txt_file_phrases = ["create a text file"]
        if voice_text.lower() in create_txt_file_phrases:
            handle_create_file(speak, listen)
            return

        # opening a text file
        open_txt_file_phrases = ["open a text file"]
        if voice_text.lower() in open_txt_file_phrases:
            handle_open_file(speak, listen)
            return

        # starting a timer
        # TODO: following voice command needs verbal creating
        start_timer_phrases = ["start a timer", "timer"]
        if voice_text.lower() in start_timer_phrases:
            handle_timer(speak, listen)
            return


        # opening a handle_open_website
        open_website_phrases = ["open a website", "open website", "website"]
        if voice_text.lower() in open_website_phrases:
            handle_open_website(speak, listen)
            return

        open_app_phrases = ["open an app", "open a app", "open app", "app"]
        if voice_text.lower() in open_app_phrases:
            handle_open_app(speak, listen)
            return

        #  play a song on Spotify
        play_music_phrases = ["play a song", "play music", "song", "music"]
        if voice_text.lower() in play_music_phrases:
            handle_play_music(speak, listen)
            return

        # skip song on Spotify
        skip_phrases = ["skip", "skip song", "skip this song", "next song", "skip this track", "skip track", "next track"]
        if voice_text.lower() in skip_phrases:
            handle_skip_track(speak, listen)
            return

        default_responses = ["Sorry, I didn't catch that"]
        speak(random.choice(default_responses))
    except Exception as error:
        print(f"Something went wrong: {error}")
        speak("Something went wrong with that command")


# event load
speak("Booting up...")

while True:
    voice_text = listen()

    if voice_text.lower() == "jarvis":
        determine_line()
