import PIL
from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px

st.header("Artist Comparison")
df = pd.read_csv("charts.csv")
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')
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
    st.plotly_chart(chart, use_container_width=True)
else:
    st.write("Select Artists you want to compare")
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)