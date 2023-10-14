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

st.header('Analysis of Song')

search_selected = st.selectbox("Search by:", ('Song/Track', 'Artist', 'Album'))
search_keyword = st.text_input("Search keyword")
button_clicked = st.button("Search")

search_results = []
tracks = []
artists = []
albums = []
if search_keyword and button_clicked:
    if search_selected == 'Song/Track':
        tracks = sp.search(q='track:' + search_keyword, type='track', limit=20)
        tracks_list = tracks['tracks']['items']
        if tracks_list:
            for track in tracks_list:
                search_results.append(track['name'] + " - By - " + track['artists'][0]['name'])
        
    elif search_selected == 'Artist':
        artists = sp.search(q='artist:' + search_keyword, type='artist', limit=20)
        artists_list = artists['artists']['items']
        if artists_list:
            for artist in artists_list:
                search_results.append(artist['name'])
        
    elif search_selected == 'Album':
        albums = sp.search(q='album:' + search_keyword, type='album', limit=20)
        albums_list = albums['albums']['items']
        if albums_list:
            for album in albums_list:
                search_results.append(album['name'] + " - By - " + album['artists'][0]['name'])

selected_album = None
selected_artist = None
selected_track = None
if search_selected == 'Song/Track':
    selected_track = st.selectbox("Select your song/track:", search_results)
elif search_selected == 'Artist':
    selected_artist = st.selectbox("Select your artist:", search_results)
elif search_selected == 'Album':
    selected_album = st.selectbox("Select your album:", search_results)


if selected_track and len(tracks) > 0:
    tracks_list = tracks['tracks']['items']
    track_id = None
    if tracks_list:
        for track in tracks_list:
            str_temp = track['name'] + " - By - " + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
                track_album = track['album']['name']
                img_album = track['album']['images'][1]['url']
                songrecommendations.save_album_image(img_album, track_id)
    selected_track_choice = None            
    if track_id:
        image = songrecommendations.get_album_mage(track_id)
        st.image(image)
        track_choices = ['Song Features', 'Similar Songs Recommendation']
        selected_track_choice = st.selectbox('Please select track choice:', track_choices)        
        if selected_track_choice == 'Song Features':
            track_features = sp.audio_features(track_id) 
            df = pd.DataFrame(track_features, index=[0])
            df_features = df[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
            st.dataframe(df_features)
            polarplot.feature_plot(df_features)
        elif selected_track_choice == 'Similar Songs Recommendation':
            token = songrecommendations.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
            similar_songs_json = songrecommendations.get_track_recommendations(track_id, token)
            recommendation_list = similar_songs_json['tracks']
            recommendation_list_df = pd.DataFrame(recommendation_list)
            recommendation_df = recommendation_list_df[['name', 'explicit', 'duration_ms', 'popularity']]
            st.dataframe(recommendation_df)
            songrecommendations.song_recommendation_vis(recommendation_df)
            
    else:
        st.write("Please select a track from the list")       

elif selected_album and len(albums) > 0:
    albums_list = albums['albums']['items']
    album_id = None
    album_uri = None    
    album_name = None
    if albums_list:
        for album in albums_list:
            str_temp = album['name'] + " - By - " + album['artists'][0]['name']
            if selected_album == str_temp:
                album_id = album['id']
                album_uri = album['uri']
                album_name = album['name']