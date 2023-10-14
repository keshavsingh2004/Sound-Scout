import PIL
from PIL import Image
import streamlit as st
import requests
import pandas as pd

# Wikipedia API endpoint
WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'

# Load data
df = pd.read_csv("charts.csv")

st.title("Artist Analysis")

def get_artist_image_url(artist_name):
  params = {
    'action': 'query',
    'format': 'json',
    'prop': 'pageimages',
    'piprop': 'original',
    'titles': artist_name
  }
  response = requests.get(WIKIPEDIA_API_URL, params=params).json()
  pages = response.get('query', {}).get('pages', {})
  page = next(iter(pages.values()))  # Get the first page
  image_url = page.get('original', {}).get('source', '')

  return image_url

def get_artist_description(artist_name):
  params = {
    'action': 'query',
    'format': 'json',
    'prop': 'extracts',
    'exintro': True,
    'explaintext': True,
    'titles': artist_name
  }
  response = requests.get(WIKIPEDIA_API_URL, params=params).json()
  pages = response.get('query', {}).get('pages', {})
  page = next(iter(pages.values()))  # Get the first page
  description = page.get('extract', '')

  return description

def get_artist_info(artist_name):
  # Get the artist's image URL from Wikipedia
  image_url = get_artist_image_url(artist_name)
  if image_url:
    st.image(image_url, caption=artist_name)
  else:
    st.write(f"No image available for {artist_name}.")

  # Get the artist's description from Wikipedia
  description = get_artist_description(artist_name)
  if description:
    st.markdown(f'## About {artist_name}')
    st.markdown(description)
  else:
    st.write(f"No description available for {artist_name}.")

analysis_option = st.radio("Choose an analysis option:", ("Artist Discography over Time", "Artist Comparison"))

if analysis_option == "Artist Discography over Time":
  st.subheader("Artist Discography over Time")
  # Calculate the frequency of each artist
  artist_counts = df['Artists'].value_counts()

  # Get the top 5 artists from user input
  top_5_artists = ['Taylor Swift', 'Elton John', 'Madonna', 'Drake', 'Kenny Chesney']

  # Filter the dataset for the top 5 artists
  top_5_artists_data = df[df['Artists'].isin(top_5_artists)]

  # Group and aggregate data at the yearly level for the top 5 artists
  grouped = top_5_artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')
  selected_artist = st.selectbox("Select an artist:", [artist for artist in top_5_artists], index=0)

  # Plot the graph for the selected artist
  chart_data = grouped[grouped['Artists'] == selected_artist]
  st.plotly_chart(chart_data)

  # Display the image and about us section for the selected artist
  if selected_artist in top_5_artists:
    get_artist_info(selected_artist)

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