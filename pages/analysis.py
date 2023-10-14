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

st.header('Analysis of songs')

search_selected = 'Artist'

search_keyword = st.text_input(search_selected + " (Keyword Search)")
button_clicked = st.button("Search")

search_results = []

if search_keyword is not None and len(str(search_keyword)) > 0:
    st.write("Start artist search")
    artists = sp.search(q='artist:' + search_keyword, type='artist', limit=20)
    artists_list = artists['artists']['items']
    
    if len(artists_list) > 0:
        for artist in artists_list:
            search_results.append(artist['name'])

selected_artist = None
selected_track = None

if search_selected == 'Artist':
    selected_artist = st.selectbox("Select your artist: ", search_results)

if selected_artist is not None:
    artist_id = None
    artist_uri = None
    
    for artist in artists_list:
        if selected_artist == artist['name']:
            artist_id = artist['id']
            artist_uri = artist['uri']
    
    if artist_id is not None:
        artist_choice = ['Top Songs']
        selected_artist_choice = st.selectbox('Select artist choice', artist_choice)
                
        if selected_artist_choice == 'Top Songs':
            artist_uri = 'spotify:artist:' + artist_id
            top_songs_result = sp.artist_top_tracks(artist_uri)
            i=1
            for track in top_songs_result['tracks']:
                with st.container():
                    col1, col2, col3, col4 = st.columns((4, 4, 2, 2))
                    col11, col12 = st.columns((10, 2))
                    col21, col22 = st.columns((11, 1))
                    col31, col32 = st.columns((11, 1))
                    col1.write(i)
                    i=i+1
                    col2.write(track['name'])
                    
                    if track['preview_url'] is not None:
                        col11.write(track['preview_url'])  
                        
                        with col12:   
                            st.audio(track['preview_url'], format="audio/mp3")  
                    
                    with col3:
                        def feature_requested(track_id):
                            track_features = sp.audio_features(track_id) 
                            df = pd.DataFrame(track_features, index=[0])
                            df_features = df.loc[:, ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                            
                            with col21:
                                st.dataframe(df_features)
                            with col31:
                                polarplot.feature_plot(df_features)
                            
                        feature_button_state = col3.button('Track Audio Features', key='features_' + track['id'])
                        if feature_button_state:
                            feature_requested(track['id'])
                    
                    with col4:
                        def similar_songs_requested(track_id):
                            token = songrecommendations.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
                            similar_songs_json = songrecommendations.get_track_recommendations(track_id, token)
                            recommendation_list = similar_songs_json['tracks']
                            recommendation_list_df = pd.DataFrame(recommendation_list)
                            recommendation_df = recommendation_list_df[['name', 'explicit', 'duration_ms', 'popularity']]
                            
                            with col21:
                                st.dataframe(recommendation_df)
                            with col31:
                                songrecommendations.song_recommendation_vis(recommendation_df)

                        similar_songs_state = col4.button('Similar Songs', key='similar_songs_' + track['id'])
                        if similar_songs_state:
                            similar_songs_requested(track['id'])
                    
                    st.write('----')