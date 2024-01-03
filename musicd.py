import streamlit as st
import requests
from moviepy.editor import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

# Deezer API endpoint for searching tracks
DEEZER_API_URL = "https://api.deezer.com/search"

def clean_filename(filename):
    return ''.join(c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in filename)

def search_and_download(song_name):
    # Search for the song using Deezer API
    params = {'q': song_name}
    response = requests.get(DEEZER_API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            # Get the first track in the search results
            track = data[0]

            # Download the track in MP4 format (assuming it's available)
            mp4_url = track.get('preview')
            if mp4_url:
                mp4_content = requests.get(mp4_url).content

                # Construct a clean and safe filename
                safe_song_name = clean_filename(song_name)

                # Construct the proper filename
                mp4_filename = f"{safe_song_name}_320kbps.mp4"

                # Save the MP4 file
                with open(mp4_filename, "wb") as mp4_file:
                    mp4_file.write(mp4_content)

                # Convert the MP4 file to WAV format using moviepy
                try:
                    clip = VideoFileClip(mp4_filename)
                    audio_clip = clip.audio
                except KeyError:
                    # If video properties are not available, assume it's an audio file
                    audio_clip = AudioFileClip(mp4_filename)

                wav_filename = f"{safe_song_name}_320kbps.wav"
                audio_clip.write_audiofile(wav_filename)

                st.success(f"Downloaded {song_name} in MP4 and WAV formats.")
            else:
                st.error("Error: No MP4 preview available for the selected track.")
        else:
            st.error("Error: No data found for the given song name.")
    else:
        st.error("Error: Unable to fetch song data from Deezer API.")

# Streamlit UI
st.title("Music Downloader")

# Input for song name
song_name = st.text_input("Enter the song name:")
if st.button("Download"):
    if song_name:
        search_and_download(song_name)
    else:
        st.warning("Please enter a song name.")
