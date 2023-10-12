import PIL
from PIL import Image
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("charts.csv")

# Convert the 'Week' column to datetime format
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')

# Calculate the frequency of each artist
artist_counts = df['Artists'].value_counts()

# Get the top 5 artists from user input
top_5_artists = ['Taylor Swift', 'Elton John', 'Madonna', 'Drake', 'Kenny Chesney']

# Filter the dataset for the top 5 artists
top_5_artists_data = df[df['Artists'].isin(top_5_artists)]

# Group and aggregate data at the yearly level for the top 5 artists
grouped = top_5_artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')
st.header("Comparison")
plt.figure(figsize=(10, 6))
for artist in top_5_artists:
    artist_data = grouped[grouped['Artists'] == artist]
    plt.plot(artist_data['Year'], artist_data['Count'], label=artist)

plt.xlabel('Year')
plt.ylabel('Artist Count')
plt.title('Artist Count Over the Years - Top 5 Artists (User Provided)')
plt.legend()
st.pyplot(plt.gcf())
