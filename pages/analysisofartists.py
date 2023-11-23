import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import PIL
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import wikipedia
import cohere
from st_pages import add_page_title
st.set_page_config(page_title="Analysis of Artists", page_icon="🎤",initial_sidebar_state="collapsed")

with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)

st.title("Analysis of Artists")

# Spotify API credentials
CLIENT_ID = 'f1668ad4ac8e49ba8bd3d55bbf3bbce0'
CLIENT_SECRET = '72ce9471b197447d9798dbe19a4325e3'

# Authenticate with the Spotify API
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Wikipedia API endpoint
WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'

# Load data
df = pd.read_csv("charts.csv")

def get_artist_image(artist_name):
  """Retrieves the artist's image from Spotify."""

  # Search for the artist
  results = sp.search(q=artist_name, type='artist', limit=1)

  if results['artists']['items']:
    artist = results['artists']['items'][0]

    # Get the artist's images
    images = artist['images']
    if images:
      image_url = images[0]['url']
      st.image(image_url, caption=selected_artist)
  else:
    st.write(f"No artist found with the name {artist_name}.")

def get_artist_info(artist_name):
    co = cohere.Client('cFYu6fx7vYGvlUNwcwRCs7LPTLRuyWM2eKqUQfnE') # This is your trial API key

    try:
        result = wikipedia.summary(artist_name + " artist", sentences=6)
        return st.markdown(result)
    except wikipedia.DisambiguationError as e:
        result = wikipedia.summary(e.options[0], sentences=6)
        return st.markdown(result)
    except wikipedia.exceptions.PageError:
        response = co.generate(
            model='command',
            prompt=f'Generate a single 130-word biographical description of the music artist {artist_name}, focusing on their early career and influences',
            max_tokens=300,
            temperature=0.9,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        return st.markdown('{}'.format(response.generations[0].text))


# Convert the 'Week' column to datetime format
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')

tab1, tab2 = st.tabs(["Artist's Discography over Time", "Artists' Comparison"])

with tab1:
  st.subheader("Artist's Discography over Time")
  # Calculate the frequency of each artist
  
  artist_counts = df['Artists'].value_counts()

  # Get the top 5 artists
  top_5_artists = [artist for artist in df['Artists'].unique().tolist()]

  #top_5_artists = sorted(top_5, key=lambda x: df['Artists'].value_counts()[x], reverse=True)

  # Filter the dataset for the top 5 artists
  top_5_artists_data = df[df['Artists'].isin(top_5_artists)]

  # Group and aggregate data at the yearly level for the top 5 artists
  grouped = top_5_artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')

  selected_artist = st.selectbox("Select an artist:", [artist for artist in artist_counts.index if artist_counts[artist] > 10])


  # Plot the graph for the selected artist
  chart_data = grouped[grouped['Artists'] == selected_artist]
  fig = px.line(chart_data, x='Year', y='Count', title=f'Artist Count Over the Years - {selected_artist}')
  fig.update_traces(line=dict(color='green'))

  # Display the image and about section for the selected artist
  if selected_artist in top_5_artists:
    # Display the image
    col1, col2 = st.columns(2,gap="medium")

    with col1:
        st.markdown(f"<h1 style='text-align: center;'>{selected_artist}</h1>", unsafe_allow_html=True)
        get_artist_image(selected_artist)

    with col2:
        get_artist_info(selected_artist)

  # Display the graph
  st.plotly_chart(fig)

with tab2:
  st.subheader("Artists' Comparison")
  artist_counts = df['Artists'].value_counts()

  # Get the unique list of artists
  unique_artists = df['Artists'].unique().tolist()

  # Ask the user to select artists using multiselect dropdown
  selected_artists = st.multiselect("Select artists:", [artist for artist in artist_counts.index if artist_counts[artist] > 10])

  if len(selected_artists) > 0:
      # Filter the dataset for the selected artists
      artists_data = df[df['Artists'].isin(selected_artists)]

      # Group and aggregate data at the yearly level for the selected artists
      grouped = artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')

      st.header("Comparison")

      # Create the Plotly line chart for the selected artists
      fig = px.line(grouped, x='Year', y='Count', color='Artists', title='Artist Comparison Over the Years')
      st.plotly_chart(fig)
col1, col2=st.columns([7,3])
with col2:
   if st.button("Take me Home "):
      switch_page("🏠 Home")
   