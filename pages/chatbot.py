import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import ai21
import streamlit as st
import lyricsgenius

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = '6c535639a5994b69be734012a94f0f94'
SPOTIPY_CLIENT_SECRET = '8552e374f87f4d64b3cf46a0d085624c'
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

# Create Spotify API object
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Set up AI21 API credentials
ai21.api_key = '6PEdkt0Qn9tYgwAUTuMp8XFevZOjeXAU'

# Set up Genius API credentials
# Set up Genius API credentials
genius = lyricsgenius.Genius("M2PYRzx-UDESVHVGiLyfP8x84d8vCXmxhQmq2WB65XWer3wqYgqyySmmJEmF07yo")

def get_playlist_data(playlist_id):
    # Get playlist data
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
    audio_features_df = pd.DataFrame(audio_features)
    audio_features_df = audio_features_df[['id', 'danceability', 'energy', 'key', 'loudness', 'mode',
                                           'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence',
                                           'tempo', 'duration_ms', 'time_signature']]

    # Merge track information with audio features
    merged_df = pd.merge(data, audio_features_df, on='id')

    return merged_df

def chatbot(df, selected_song_details):
    # Get user input

    # Generate prompt
    # song = genius.search_song(selected_song_details['name'], selected_song_details['artist'])
    songs = genius.search_songs(selected_song_details['name']+selected_song_details['artist'])["songs"]
    for song in songs:
        if song['title'] == "Rap God":
            song_id = song['id']
    song = genius.song(song_id)
    if song:
        prompt = f"Lyrics: {song.lyrics}\n"

    # Add song features to the prompt
    song_features = df[df['id'] == selected_song_details['id']].iloc[0]
    for feature in ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']:
        prompt += f"{feature.capitalize()}: {song_features[feature]}\n"

    # Allow the user to ask further questions
    follow_up_question = st.text_input("Ask me question about the song:")

    if follow_up_question:
        # Include the follow-up question in the prompt
        prompt += f"{follow_up_question}\n\n"

        # Generate response using AI21
        response = ai21.Completion.execute(
            model="j2-ultra",
            prompt=prompt,
            numResults=1,
            maxTokens=1000,
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

        st.write(response["completions"][0]["data"]["text"])
# Example usage:
# Example usage:
playlist_id = st.text_input("Enter a Spotify playlist ID:")
if playlist_id:
    df = get_playlist_data(playlist_id)

    # Display tracklist
    selected_song = st.selectbox("Select a song:", df['name'].tolist())

    # Get the selected song's details
    selected_song_details = df[df['name'] == selected_song].iloc[0]
    st.write(f"Selected Song: {selected_song_details['name']} by {selected_song_details['artist']} from the album {selected_song_details['album']}")

    # Get lyrics for the selected song
    lyrics = genius.search_song(selected_song_details['name'], selected_song_details['artist'])
    if lyrics:
        chatbot(df, selected_song_details)  # Call the chatbot function after displaying lyrics
    else:
        st.write("Lyrics not found.")