import pandas as pd
import streamlit as st
import plotly.express as px

st.markdown("""
    ## Analysis of Genre
    
    Below is the Pie-Chart of the Genres of Music featured in BillBoard during 1999-2019
    
    """)

# Load and preprocess the dataset
df = pd.read_csv("billboard.csv")
df['Week'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')
df['Genres'] = df['Genre'].str.split(',')
df = df.explode('Genre')

# Flatten the list of genres
genres_list = [genre for genres in df['Genres'] for genre in genres]

# Calculate the frequency of each genre
genre_counts = pd.Series(genres_list).value_counts()

# Select top 10 genres and group the rest as "Others"
top_genres = genre_counts.head(6)
other_count = genre_counts[6:].sum()
top_genres['Others'] = other_count

# Create a Pie chart using Plotly Express
fig = px.pie(top_genres, values=top_genres.values, names=top_genres.index, title='Genre Distribution')

# Display the chart using Streamlit
st.plotly_chart(fig)