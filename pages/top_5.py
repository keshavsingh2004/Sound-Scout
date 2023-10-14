import PIL
from PIL import Image
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import pandas as pd
import plotly.express as px

# Spotify API credentials
CLIENT_ID = 'd55c490e4f9c4372ac59952d422fe1fd'
CLIENT_SECRET = 'ca902e2a8d7b43ad8cb3a0ed682bbff8'

# Authenticate with the Spotify API
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Load data
df = pd.read_csv("charts.csv")

st.title("Artist Analysis")

def get_artist_info(artist_name):
    # Search for the artist
    results = sp.search(q=artist_name, type='artist', limit=1)

    if results['artists']['items']:
        artist = results['artists']['items'][0]

        # Get the artist's images
        images = artist['images']
        if images:
            image_url = images[0]['url']
            st.image(image_url, caption=artist_name, width=400)

        # Get the artist's description
        artist_id = artist['id']
        headers = {
            'Authorization': f'Bearer {sp.auth_manager.get_access_token()}'
        }
        url = f'https://api.spotify.com/v1/artists/{artist_id}'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            artist_info = response.json()
            description = artist_info.get('bio', {}).get('summary')
            if description:
                st.markdown(f'## About {artist_name}')
                st.markdown(description)
            else:
                st.write(f"No description available for {artist_name}.")
        else:
            st.write(f"Error retrieving artist information for {artist_name}.")
    else:
        st.write(f"No artist found with the name {artist_name}.")

# Convert the 'Week' column to datetime format
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')

analysis_option = st.radio("Choose an analysis option:", ("Artist Discography over Time", "Artist Comparison"))

if analysis_option == "Artist Discography over Time":
    st.subheader("Artist Discography over Time")
    # Calculate the frequency of each artist
    artist_counts = df['Artists'].value_counts()

    # Get the top 5 artists from user input
    top_5_artists = ['Taylor Swift', 'Elton John', 'Madonna', 'Drake', 'Kenny Chesney','Travis Scott','Ed Sheeran','Doja Cat','Kendrick Lamar','Justin Bieber', 'One Direction', 'Zayn','Harry Styles','Niall Horan', 'The Weeknd']

    # Filter the dataset for the top 5 artists
    top_5_artists_data = df[df['Artists'].isin(top_5_artists)]

    # Group and aggregate data at the yearly level for the top 5 artists
    grouped = top_5_artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')
    selected_artist = st.selectbox("Select an artist:", [artist for artist in top_5_artists], index=0)

    # Plot the graph for the selected artist
    chart_data = grouped[grouped['Artists'] == selected_artist]
    fig = px.line(chart_data, x='Year', y='Count', title=f'Artist Count Over the Years - {selected_artist}')
    fig.update_traces(line=dict(color='green'))

    # Display the image and about us section for the selected artist
    if selected_artist in top_5_artists:
        get_artist_info(selected_artist)
        st.plotly_chart(fig)

elif analysis_option == "Artist Comparison":
    st.subheader("Artist Comparison")
    # Get the unique list of artists
    unique_artists = df['Artists'].unique().tolist()

    # Ask the user to select artists using multiselect dropdown
    selected_artists = st.multiselect("Select artists:", unique_artists)

    if len(selected_artists) > 0:
    # Filter the dataset for the selected artists
        artists_data = df[df['Artists'].isin(selected_artists)]

    # Group and aggregate data at the yearly level for the selected artists
        grouped = artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')

        st.header("Comparison")

    # Create the Plotly line chart for the selected artists
        chart = px.line(grouped, x='Year', y='Count', color='Artists',
                        title="Artist Count Over the Years - Comparison")

    # Display the chart using Streamlit
        st.plotly_chart(chart)