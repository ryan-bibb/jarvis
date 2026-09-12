## Summary

A voice-activated assistant that runs entirely on your computer, no extra hardware required. Say `Jarvis` followed by a command to trigger any of the actions below.

## Commands

- What time is it?
  - tells local time

- What is my name?
  - tells you the name to call you 
  - by default it is my name

- Change my name.
  - allows you to set a custom name to be called

- Create a text file.
  - allows you to create a txt file, and set its contents, inside the directory the program lives

- Open a text file.
  - allows you to open and read the contents of a txt file in the directory the program lives

- Start a time
  - allows you to set a time and a customer time and alerts you when timer is finished

- Optimize
  - this commands allows you to use an actually AI model, rather than the built in commands seen above. All you need to do is say the commands `optimize`, then follow that with another command of your choice after the voice response from Jarvis
  - optiized commands are cached as to not spam API requests to the AI model. Any command that has a successful cache hit will replay the same response as before.  

- Open a website
  - say `open a website`, then say the site's name (without the domain) and Jarvis opens `https://<name>.com` in your default browser

- Open an app
  - say `open an app`, then say the app's name and Jarvis will launch it (works on macOS, Windows, and Linux)

- Play a song
  - say `play a song` (or `play music`) and Jarvis opens Spotify. Say a song or artist name to play it, or decline and Jarvis will shuffle one of your liked tracks
  - requires an active Spotify Connect device and Spotify API credentials (see Setup below)

- Skip a song
  - say `skip` (or `next song`/`skip track`) to skip to the next track on Spotify

## Setup

- Requires Python 3 and the packages in `requirements.txt` (`pip install -r requirements.txt`)
- Requires a `.env` file with the following variables:
  - `OPENAI_API_KEY` for the `optimize` command
  - `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` for the play/skip song commands
- `pyobjc` is only needed on macOS (used by `pyttsx3` for text-to-speech)



