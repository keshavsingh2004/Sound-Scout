import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import polarplot
import songrecommendations

SPOTIPY_CLIENT_ID = 'd55c490e4f9c4372ac59952d422fe1fd'
SPOTIPY_CLIENT_SECRET = 'ca902e2a8d7b43ad8cb3a0ed682bbff8'

def main():
    auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    st.header('Analysis of Songs')
    search_selected = st.selectbox('Search by', ['Artist', 'Song'])
    search_keyword = st.text_input(search_selected + " (Keyword Search)")
    button_clicked = st.button("Search")

    search_results = perform_search(sp, search_selected, search_keyword)

    selected_search_result = st.selectbox("Select your " + search_selected.lower() + ": ", search_results)

    if selected_search_result:
        if search_selected == 'Artist':
            artist_id, artist_uri = get_artist_info(sp, selected_search_result)

            if artist_id:
                artist_choice = ['Top Songs']
                selected_artist_choice = 'Top Songs'
                if selected_artist_choice == 'Top Songs':
                    top_songs_result = sp.artist_top_tracks(artist_uri)
                    display_top_songs(top_songs_result, sp)
        elif search_selected == 'Song':
            track_id = get_track_id(sp, selected_search_result)
            if track_id:
                display_track_info(sp, track_id)

def perform_search(sp, search_selected, search_keyword):
    search_results = []

    if search_keyword and len(str(search_keyword)) > 0:
        if search_selected == 'Artist':
            artists = sp.search(q='artist:' + search_keyword, type='artist', limit=20)
            artists_list = artists['artists']['items']

            for artist in artists_list:
                search_results.append(artist['name'])
        elif search_selected == 'Song':
            songs = sp.search(q='track:' + search_keyword, type='track', limit=20)
            songs_list = songs['tracks']['items']

            for song in songs_list:
                search_results.append(song['name'])

    return search_results

def get_artist_info(sp, selected_search_result):
    artists = sp.search(q='artist:' + selected_search_result, type='artist', limit=1)
    if artists['artists']['items']:
        artist = artists['artists']['items'][0]
        return artist['id'], artist['uri']
    return None, None

def display_top_songs(top_songs_result, sp):
    i = 1
    for track in top_songs_result['tracks']:
        st.write(i)
        st.write(track['name'])
        
        track_features = sp.audio_features(track['id'])[0]
        display_audio_features(track_features)
        display_similar_songs(track['id'])
        i += 1

def display_track_info(sp, track_id):
    st.write('Track Details:')
    track_features = sp.audio_features(track_id)[0]
    display_audio_features(track_features)
    display_similar_songs(track_id)

def display_audio_features(track_features):
    df_features = pd.DataFrame({k: [v] for k, v in track_features.items()}, columns=['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence'])
    st.dataframe(df_features)
    polarplot.feature_plot(df_features)

def display_similar_songs(track_id):
    token = songrecommendations.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    similar_songs_json = songrecommendations.get_track_recommendations(track_id, token)
    recommendation_list = similar_songs_json['tracks']
    recommendation_df = pd.DataFrame(recommendation_list)[['name', 'explicit', 'duration_ms', 'popularity']]
    st.dataframe(recommendation_df)
    songrecommendations.song_recommendation_vis(recommendation_df)

if __name__ == '__main__':
    main()
