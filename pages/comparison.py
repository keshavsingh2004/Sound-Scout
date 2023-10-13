# import streamlit as st
# import pandas as pd
# import plotly.express as px

# df = pd.read_csv("charts.csv")

# # Convert the 'Week' column to datetime format
# df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')

# # Calculate the frequency of each artist
# artist_counts = df['Artists'].value_counts()

# # Get the top 5 artists from user input
# top_5_artists = ['Taylor Swift', 'Elton John', 'Madonna', 'Drake', 'Kenny Chesney']

# # Filter the dataset for the top 5 artists
# top_5_artists_data = df[df['Artists'].isin(top_5_artists)]

# # Group and aggregate data at the yearly level for the top 5 artists
# grouped = top_5_artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')

# st.header("Comparison")

# # Create the Plotly line chart for the top 5 artists
# chart = px.line(grouped, x='Year', y='Count', color='Artists', title='Artist Count Over the Years - Top 5 Artists (User Provided)')

# # Display the chart using Streamlit
# st.plotly_chart(chart, theme=None, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("charts.csv")

# Convert the 'Week' column to datetime format
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')

# Ask the user for two artists
artist1 = st.text_input("Enter the first artist:")
artist2 = st.text_input("Enter the second artist:")

artist1 = artist1.title()
artist2 = artist2.title()


# Filter the dataset for the user-provided artists
artists_data = df[df['Artists'].isin([artist1, artist2])]

# Group and aggregate data at the yearly level for the user-provided artists
grouped = artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')

st.header("Comparison")

# Create the Plotly line chart for the user-provided artists
chart = px.line(grouped, x='Year', y='Count', color='Artists',
                title=f"Artist Count Over the Years - {artist1} vs {artist2}")

# Display the chart using Streamlit
st.plotly_chart(chart, use_container_width=True)