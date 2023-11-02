import streamlit as st
import pandas as pd
import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import polarplot
import songrecommendations

st.set_page_config(page_title="Analysis of Songs", page_icon="🎶")

SPOTIPY_CLIENT_ID = '6c535639a5994b69be734012a94f0f94'
SPOTIPY_CLIENT_SECRET = '8552e374f87f4d64b3cf46a0d085624c'

auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.header('Analysis of Songs')

search_selected = st.selectbox('Search by', ['Artist', 'Song'])

search_keyword = st.text_input(search_selected + " (Keyword Search)")
button_clicked = st.button("Search")

search_results = []

if search_keyword is not None and len(str(search_keyword)) > 0:
    if search_selected == 'Artist':
        st.write("Start artist search")
        artists = sp.search(q='artist:' + search_keyword, type='artist', limit=20)
        artists_list = artists['artists']['items']
        
        if len(artists_list) > 0:
            for artist in artists_list:
                search_results.append(artist['name'])
    elif search_selected == 'Song':
        st.write("Start song search")
        songs = sp.search(q='track:' + search_keyword, type='track', limit=20)
        songs_list = songs['tracks']['items']
        
        if len(songs_list) > 0:
            for song in songs_list:
                search_results.append(song['name'])

selected_search_result = st.selectbox("Select your " + search_selected.lower() + ": ", search_results)

if selected_search_result is not None:
    if search_selected == 'Artist':
        artist_id = None
        artist_uri = None
        
        for artist in artists_list:
            if selected_search_result == artist['name']:
                artist_id = artist['id']
                artist_uri = artist['uri']
        
        if artist_id is not None:
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
                                original_track_features = sp.audio_features(track_id)
                                original_features = np.array([
                                    original_track_features[0]['acousticness'],
                                    original_track_features[0]['danceability'],
                                    original_track_features[0]['energy'],
                                    original_track_features[0]['instrumentalness'],
                                    original_track_features[0]['liveness'],
                                    original_track_features[0]['speechiness'],
                                    original_track_features[0]['valence']
                                ])
                                token = songrecommendations.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
                                similar_songs_json = songrecommendations.get_track_recommendations(track_id, token)
                                recommendation_list = similar_songs_json['tracks']
                                recommendation_list_df = pd.DataFrame(recommendation_list)
                                recommendation_df = recommendation_list_df[['name','duration_ms', 'popularity','explicit']]
                                name_list = recommendation_df['name'].tolist()
                                simi=[]

                                for recommendations in name_list:
                                    s_song = sp.search(q='track:' + recommendations, type='track', limit=20)
                                    selected_track_id = s_song['tracks']['items'][0]['id'] 
                                    selected_track_features = sp.audio_features(selected_track_id)
                                    selected_features = np.array([
                                        selected_track_features[0]['acousticness'],
                                        selected_track_features[0]['danceability'],
                                        selected_track_features[0]['energy'],
                                        selected_track_features[0]['instrumentalness'],
                                        selected_track_features[0]['liveness'],
                                        selected_track_features[0]['speechiness'],
                                        selected_track_features[0]['valence']
                                    ])

                                    distance = songrecommendations.calculate_euclidean_distance(original_features, selected_features)
                                    distance=1-distance
                                    distance=distance*100
                                    simi.append(distance)
                                recommendation_df["similarity(in %)"]=simi


                                
                                with col21:
                                    st.dataframe(recommendation_df)
                                with col31:
                                    songrecommendations.song_recommendation_vis(recommendation_df)
                            
                            similar_button_state = col4.button('Similar Songs', key='similar_' + track['id'])
                            if similar_button_state:
                                similar_songs_requested(track['id'])
                        track_id=track['id']
                        spotify_url = f"https://open.spotify.com/embed/track/{track_id}"
                        st.markdown(f"""
                            <iframe style="border-radius:12px" src="{spotify_url}" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                            <br><br>
                        """, unsafe_allow_html=True)
                        st.divider()
     
    elif search_selected == 'Song':
        track_id = None
        song_name = None
    
        for song in songs_list:
            if selected_search_result == song['name']:
                track_id = song['id']
                song_name = song['name']
    
        if track_id is not None:
            col1, col2, col3, col4 = st.columns((4, 4, 2, 2))
            col11, col12 = st.columns((10, 2))
            col21, col22 = st.columns((11, 1))
            col31, col32 = st.columns((11, 1))
            col1.write(song_name)
        
            with col3:
                def feature_requested(track_id):
                    track_features = sp.audio_features(track_id)
                    df = pd.DataFrame(track_features, index=[0])
                    df_features = df.loc[:, ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                    with col21:
                                st.dataframe(df_features)
                    with col31:
                                polarplot.feature_plot(df_features)
                
            
                feature_button_state = st.button('Track Audio Features', key='features_' + track_id)
                if feature_button_state:
                    feature_requested(track_id)
        
            with col4:
                def similar_songs_requested(track_id):
                    token = songrecommendations.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
                    similar_songs_json = songrecommendations.get_track_recommendations(track_id, token)
                    recommendation_list = similar_songs_json['tracks']
                    recommendation_list_df = pd.DataFrame(recommendation_list)
                    recommendation_df = recommendation_list_df[['name', 'duration_ms', 'popularity','explicit']]
                    with col21:
                                st.dataframe(recommendation_df)
                    with col31:
                                songrecommendations.song_recommendation_vis(recommendation_df)
                
            
                similar_button_state = st.button('Similar Songs', key='similar_' + track_id)
                if similar_button_state:
                    similar_songs_requested(track_id)
            spotify_url = f"https://open.spotify.com/embed/track/{track_id}"
            st.markdown(f"""
            ___
            ### Listen to this song on Spotify!
            <iframe style="border-radius:12px" src="{spotify_url}" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            <br><br>
            """, unsafe_allow_html=True)
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)