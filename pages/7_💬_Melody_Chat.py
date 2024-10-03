import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import ai21
import streamlit as st
import requests
import json
import urllib.parse
from streamlit_extras.switch_page_button import switch_page 
from ai21 import AI21Client
import google.generativeai as genai
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch API key and model name from environment variables
gemini_api_key = os.getenv('google_API_KEY')
gemini_model_name = os.getenv('GEMINI_MODEL_NAME')

genai.configure(api_key=gemini_api_key)

st.set_page_config(page_title="Melody Chat", page_icon="💬",initial_sidebar_state="collapsed")
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)
col1,col2=st.columns([8,1])
with col1:
    st.title("Melody Chat")
with col2:
    for _ in range(2):
        st.write(" ")
    if st.button("🏠"):
        switch_page("🏠 Home")

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = '6c535639a5994b69be734012a94f0f94'
SPOTIPY_CLIENT_SECRET = '8552e374f87f4d64b3cf46a0d085624c'
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

# Create Spotify API object
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Set up Genius API credentials
def get_lyrics(music_name):
    url = f"https://lyrics.astrid.sh/api/search?q={music_name}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def get_playlist_data(playlist_id):
    # Get playlist dat
    try:
        results = sp.playlist(playlist_id, fields="tracks,next")
        tracks = results['tracks']
        spotify_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
        st.markdown(f"""
            <iframe style="border-radius:12px" src="{spotify_url}" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            <br><br>
            """, unsafe_allow_html=True)

        # Collect all tracks
        tracklist = tracks['items']
        while tracks['next']:
            tracks = sp.next(tracks)
            tracklist += tracks['items']

        # Extract track information and audio features
        playlist_info = []
        for track in tracklist:
            info = track['track']
            playlist_info.append((info['id'], info['name'], info['artists'][0]['name'], info['album']['name'], info['album']['id']))

        # Create DataFrame with track information
        data = pd.DataFrame(playlist_info, columns=['id', 'name', 'artist', 'album', 'album_id'])

        # Extract audio features for each song
        audio_features_ids = [track['track']['id'] for track in tracklist]
        audio_features = []

        for i in range(0, len(audio_features_ids), 50):
            audio_features_batch = sp.audio_features(audio_features_ids[i:i+50])
            audio_features += audio_features_batch

        # Create DataFrame with audio features
        try:
            audio_features_df = pd.DataFrame(audio_features)
            audio_features_df = audio_features_df[['id', 'danceability', 'energy', 'key', 'loudness', 'mode',
                                            'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence',
                                            'tempo', 'duration_ms', 'time_signature']]
            merged_df = pd.merge(data, audio_features_df, on='id')
        except:
            audio_features_df = None
            merged_df=data
        # Merge track information with audio features
        

        return merged_df
    except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 404:
                st.info("Playlist not found. Please check the playlist link or ID and try again.")
            else:
                st.info(f"An error occurred: {e}. Please try again with a different playlist ID.")

def get_track_data(track_id):
    try:
        track = sp.track(track_id)
        spotify_url = f"https://open.spotify.com/embed/track/{track_id}"
        st.markdown(f"""
            <iframe style="border-radius:12px" src="{spotify_url}" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            <br><br>
            """, unsafe_allow_html=True)

        # Extract track information
        track_info = (track['id'], track['name'], track['artists'][0]['name'], track['album']['name'], track['album']['id'])

        # Create DataFrame with track information
        data = pd.DataFrame([track_info], columns=['id', 'name', 'artist', 'album', 'album_id'])

        # Extract audio features for the song
        audio_features = sp.audio_features([track_id])

        # Create DataFrame with audio features
        try:
            audio_features_df = pd.DataFrame(audio_features)
            audio_features_df = audio_features_df[['id', 'danceability', 'energy', 'key', 'loudness', 'mode',
                                            'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence',
                                            'tempo', 'duration_ms', 'time_signature']]
            merged_df = pd.merge(data, audio_features_df, on='id')
        except:
            audio_features_df = None
            merged_df=data
        # Merge track information with audio features
        

        return merged_df
    except spotipy.exceptions.SpotifyException as e:
            st.info("Song not found. Please check the song link and try again.")

# Chatbot function to process song details and user input
def chatbot(df, selected_song_details):
    # Retrieve song name and features
    song_name = selected_song_details['name']
    song_id = selected_song_details['id']

    # Fetch song lyrics
    song_lyrics = get_lyrics(song_name)
    
    # Construct context using song lyrics and features
    CONTEXT = f"""
Song: {song_name}

Lyrics:
{song_lyrics}

Song Features:
"""
    
    # Try to add song features from the dataframe
    try:
        song_features = df[df['id'] == song_id].iloc[0]
        for feature in ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']:
            CONTEXT += f"- {feature.capitalize()}: {song_features[feature]}\n"
    except Exception as e:
        CONTEXT += "Song features could not be loaded.\n"

    follow_up_question = st.text_input("Ask me a question about the song:")

    if follow_up_question:
        # Construct a more detailed prompt
        prompt = f"""
Based on the following context about the song "{song_name}", please provide a detailed and insightful response to the question below. Your response should be between 150-200 words and incorporate relevant information from the song's lyrics and features when applicable.

Context:
{CONTEXT}

Question: {follow_up_question}

Instructions:
1. Analyze the question and the provided context.
2. Provide a coherent and informative response that directly addresses the question.
3. Incorporate specific details from the lyrics or song features if relevant to the question.
4. If the question cannot be answered solely based on the given information, provide the best possible interpretation or general insight related to the topic.
5. Maintain a friendly and engaging tone in your response.

Response:
"""

        # Initialize the Gemini model
        model = genai.GenerativeModel(gemini_model_name)
        
        response = model.generate_content(prompt)
        st.info(response.text)
# Example usage:
selector = st.selectbox("Choose an option:", ['Playlist', 'Song'])
st.write(" ")
if selector == 'Playlist':
    url = st.text_input('Enter the Spotify playlist link or playlist ID')
    parsed_url = urllib.parse.urlparse(url)
    playlist_id = parsed_url.path.split('/')[-1]
    if playlist_id:
        df = get_playlist_data(playlist_id)
        if df is not None:
            # Display tracklist
            selected_song = st.selectbox("Select a song:", df['name'].tolist())

            # Get the selected song's details
            selected_song_details = df[df['name'] == selected_song].iloc[0]
            st.write(f"Selected Song: {selected_song_details['name']} by {selected_song_details['artist']} from the album {selected_song_details['album']}")

            # Get lyrics for the selected song

            if selected_song:
                chatbot(df, selected_song_details)  # Pass the lyrics to the chatbot function
            else:
                st.write("Lyrics not found.")
else:

    url = st.text_input("Enter a Spotify track link or track ID:")
    parsed_url = urllib.parse.urlparse(url)
    track_id = parsed_url.path.split('/')[-1]
    if track_id:
        df = get_track_data(track_id)
        if df is not None:
            selected_song_details = df.iloc[0]
            chatbot(df, selected_song_details)