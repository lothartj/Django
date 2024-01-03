import streamlit as st
import requests
import os

# Jamendo API endpoint for searching tracks
JAMENDO_API_URL = "https://api.jamendo.com/v3.0/tracks/"

def search_and_download(song_name):
    # Search for the song using Jamendo API
    params = {'client_id': 'YOUR_JAMENDO_CLIENT_ID', 'format': 'json', 'name': song_name}
    response = requests.get(JAMENDO_API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json().get('results', [])
        if data:
            # Get the first track in the search results
            track = data[0]

            # Get the direct link to the audio file
            audio_url = track.get('audio', '')
            if audio_url:
                # Construct a clean and safe filename
                safe_song_name = ''.join(c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in song_name)

                # Construct the proper filename
                audio_filename = f"{safe_song_name}_jamendo.mp3"

                # Save the audio file
                with open(audio_filename, "wb") as audio_file:
                    audio_file.write(requests.get(audio_url).content)

                st.success(f"Downloaded {song_name} from Jamendo in MP3 format.")
            else:
                st.error("Error: No audio available for the selected track.")
        else:
            st.error(f"Error: No data found for the given song name: {song_name}")
    else:
        st.error("Error: Unable to fetch song data from Jamendo API.")

# Streamlit UI
st.title("Music Downloader")

# Input for song name
song_name = st.text_input("Enter the song name:")
if st.button("Download"):
    if song_name:
        search_and_download(song_name)
    else:
        st.warning("Please enter a song name.")
