import streamlit as st
import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import polarplot
import songrecommendations

SPOTIPY_CLIENT_ID = 'd55c490e4f9c4372ac59952d422fe1fd'
SPOTIPY_CLIENT_SECRET = 'ca902e2a8d7b43ad8cb3a0ed682bbff8'

auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def search_spotify(sp, search_type, search_keyword):
    results = sp.search(q=f'{search_type}:' + search_keyword, type=search_type, limit=20)
    return [item['name'] for item in results[search_type+'s']['items']]

def get_id_uri(sp, search_type, selected_search_result):
    results = sp.search(q=f'{search_type}:' + selected_search_result, type=search_type, limit=1)
    if results[search_type+'s']['items']:
        item = results[search_type+'s']['items'][0]
        return item['id'], item['uri']
    return None, None

def display_features(track_id):
    track_features = sp.audio_features(track_id)[0] 
    df_features = pd.DataFrame(track_features, index=[0])
    df_features = df_features.loc[:, ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
    st.dataframe(df_features)
    polarplot.feature_plot(df_features)

def display_similar_songs(track_id):
    token = songrecommendations.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    similar_songs_json = songrecommendations.get_track_recommendations(track_id, token)
    recommendation_list = similar_songs_json['tracks']
    recommendation_list_df = pd.DataFrame(recommendation_list)
    recommendation_df = recommendation_list_df[['name', 'explicit', 'duration_ms', 'popularity']]
    st.dataframe(recommendation_df)
    songrecommendations.song_recommendation_vis(recommendation_df)

st.header('Analysis of Songs')

search_selected = st.selectbox('Search by', ['Artist', 'Song'])
search_keyword = st.text_input(search_selected + " (Keyword Search)")
button_clicked = st.button("Search")

search_results = []

if button_clicked and search_keyword:
    search_type = 'artist' if search_selected == 'Artist' else 'track'
    search_results = search_spotify(sp, search_type, search_keyword)

selected_search_result = st.selectbox("Select your " + search_selected.lower() + ": ", search_results)

selected_id = None

if selected_search_result:
    selected_id, selected_uri = get_id_uri(sp, search_type, selected_search_result)

if selected_id:
    if search_selected == 'Artist':
        top_songs_result = sp.artist_top_tracks(selected_uri)
        for i, track in enumerate(top_songs_result['tracks'], start=1):
            st.write(f"{i}. {track['name']}")
            if st.button('Track Audio Features', key='features_' + track['id']):
                display_features(track['id'])
            if st.button('Similar Songs', key='similar_' + track['id']):
                display_similar_songs(track['id'])
    elif search_selected == 'Song':
        if st.button('Track Audio Features', key='features_' + selected_id):
            display_features(selected_id)
        if st.button('Similar Songs', key='similar_' + selected_id):
            display_similar_songs(selected_id)
