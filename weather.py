import streamlit as st
import requests
from pydub import AudioSegment
import os

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

                # Get the absolute path to the current working directory
                current_directory = os.getcwd()

                # Construct the full paths
                mp4_full_path = os.path.abspath(os.path.join(current_directory, mp4_filename))
                wav_full_path = os.path.abspath(os.path.join(current_directory, f"{safe_song_name}_320kbps.wav"))

                # Create the directory if it doesn't exist
                os.makedirs(os.path.dirname(mp4_full_path), exist_ok=True)

                # Save the MP4 file
                with open(mp4_full_path, "wb") as mp4_file:
                    mp4_file.write(mp4_content)

                # Debugging information
                print(f"mp4_full_path: {mp4_full_path}")
                print(f"wav_full_path: {wav_full_path}")

                # Check if the file exists
                if os.path.exists(mp4_full_path):
                    print(f"MP4 file exists at {mp4_full_path}")
                else:
                    print(f"MP4 file does not exist at {mp4_full_path}")

                # Convert the MP4 file to WAV format
                audio = AudioSegment.from_file(mp4_full_path, format="mp4")
                audio.export(wav_full_path, format="wav")

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
