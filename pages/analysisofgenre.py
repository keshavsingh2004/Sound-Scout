import pandas as pd
import matplotlib.pyplot as plt
import PIL
from PIL import Image
import streamlit as st
from st_pages import add_page_title
add_page_title(layout="narrow")

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


# Plot the genre distribution in a pie chart
plt.figure(figsize=(12, 6))
plt.pie(top_genres, labels=top_genres.index, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Genre Distribution')
total_genres = len(genre_counts)
plt.text(0, -1.3, f"Total Genres: {total_genres}", horizontalalignment='center', verticalalignment='center')
st.pyplot(plt.gcf())