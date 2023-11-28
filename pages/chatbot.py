import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import ai21
import streamlit as st
import requests
import json
import urllib.parse
from streamlit_extras.switch_page_button import switch_page 

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

# Set up AI21 API credentials
ai21.api_key = '6PEdkt0Qn9tYgwAUTuMp8XFevZOjeXAU'

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


def chatbot(df, selected_song_details):

    follow_up_question = st.text_input("Ask me question about the song:")
    song = get_lyrics(selected_song_details['name'])
    if song:
        prompt = f"Lyrics of the song are: {song}\nBelow are the features of the song:"

    # Add song features to the prompt
    try:
        song_features = df[df['id'] == selected_song_details['id']].iloc[0]
        for feature in ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']:
            prompt += f"{feature.capitalize()}: {song_features[feature]}\n"
    except:
        prompt+=""

    if follow_up_question:
        # Include the follow-up question in the prompt
        prompt += f"You are a music expert hired to analyze lyrics and other elements in songs. Your goal is to provide insightful commentary on the themes, poetic devices, and musical techniques used in a given song. Craft a detailed analysis that goes beyond surface-level observations, showcasing your expertise and enhancing the audience's understanding of the song's artistic nuances. Consider the impact of the lyrics on the overall message, the cultural context, and any intertextual references. Your analysis should be engaging and cater to both music enthusiasts and those seeking a deeper appreciation of the song. Your first analysis topic would be {follow_up_question}.The target language is English."
        # Generate response using AI21
        response = ai21.Completion.execute(
            model="j2-ultra",
            prompt=prompt,
            numResults=1,
            minTokens=50,
            maxTokens=2000,
            temperature=0.9,
            topKReturn=1,
            topP=1,
            presencePenalty={
                "scale": 1,
                "applyToNumbers": True,
                "applyToPunctuations": True,
                "applyToStopwords": True,
                "applyToWhitespaces": True,
                "applyToEmojis": True
            },
            countPenalty={
                "scale": 1,
                "applyToNumbers": True,
                "applyToPunctuations": True,
                "applyToStopwords": True,
                "applyToWhitespaces": True,
                "applyToEmojis": True
            },
            frequencyPenalty={
                "scale": 1,
                "applyToNumbers": True,
                "applyToPunctuations": True,
                "applyToStopwords": True,
                "applyToWhitespaces": True,
                "applyToEmojis": True
            },
            stopSequences=[]
        )

        st.info(response["completions"][0]["data"]["text"])
# Example usage:
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