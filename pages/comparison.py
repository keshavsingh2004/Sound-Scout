import streamlit as st
import pandas as pd
import plotly.express as px

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

# Create the Plotly line chart for the top 5 artists
chart = px.line(grouped, x='Year', y='Count', color='Artists', title='Artist Count Over the Years - Top 5 Artists (User Provided)')

# Display the chart using Streamlit
st.plotly_chart(chart, theme=None, use_container_width=True)