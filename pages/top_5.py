import PIL
from PIL import Image
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import wikipedia

# Load data
df = pd.read_csv("charts.csv")

st.title("Artist Analysis")

def get_artist_info(artist_name):
    try:
        # Search for the artist's page on Wikipedia
        page = wikipedia.page(artist_name)

        # Get the artist's summary and image
        summary = page.summary
        image_url = page.images[0]

        # Display the artist's image
        image = Image.open(requests.get(image_url, stream=True).raw)
        st.image(image, caption=artist_name)

        # Display the artist's summary
        st.markdown(f'## About {artist_name}')
        st.markdown(summary)

    except wikipedia.exceptions.PageError:
        st.write(f"No Wikipedia page found for {artist_name}.")
    except wikipedia.exceptions.DisambiguationError:
        st.write(f"Multiple Wikipedia pages found for {artist_name}. Please specify the artist more precisely.")

# Convert the 'Week' column to datetime format
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')

analysis_option = st.radio("Choose an analysis option:", ("Artist Discography over Time", "Artist Comparison"))

if analysis_option == "Artist Discography over Time":
    st.subheader("Artist Discography over Time")
    # Calculate the frequency of each artist
    artist_counts = df['Artists'].value_counts()

    # Get the top 5 artists
    top_5_artists = artist_counts.head(5).index.tolist()

    # Filter the dataset for the top 5 artists
    top_5_artists_data = df[df['Artists'].isin(top_5_artists)]

    # Group and aggregate data at the yearly level for the top 5 artists
    grouped = top_5_artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')

    selected_artist = st.selectbox("Select an artist:", top_5_artists)

    # Plot the graph for the selected artist
    chart_data = grouped[grouped['Artists'] == selected_artist]
    fig = px.line(chart_data, x='Year', y='Count', title=f'Artist Count Over the Years - {selected_artist}')
    fig.update_traces(line=dict(color='green'))

    # Display the image and about section for the selected artist
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