import streamlit as st
import pandas as pd
import altair as alt

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

# Create the Altair line chart for the top 5 artists
chart = alt.Chart(grouped).mark_line().encode(
    x='Year:T',
    y='Count:Q',
    color='Artists:N',
    tooltip=['Year:T', 'Artists:N', 'Count:Q']
).properties(
    width=600,
    height=400,
    title='Artist Count Over the Years - Top 5 Artists (User Provided)'
)

# Display the chart using Streamlit
st.altair_chart(chart)