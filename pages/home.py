import streamlit as st
from st_pages import add_page_title
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('charts.csv')

# Group the data by the "artist" column and count the occurrences
artist_counts = df['artist'].value_counts()

# Retrieve the top 5 artists with the highest value count
top_5_artists = artist_counts.head(5)

# Create a Streamlit app
st.title("Home")
st.write("Welcome to [Your Website Name], where the power of music comes alive through analysis, exploration, and prediction.")
st.header("Analysis of Artists")
st.write("In this section, we offer a comprehensive artist discography and a platform for meaningful artist comparisons")
st.write("Here is the top 5 artist in BillBoard Hot 100")
st.write(top_5_artists)
st.subheader("Artists' Discography over Years")
st.write("Whether you're a music enthusiast or a professional, our platform provides valuable insights into your favorite artists' performance over the years. Our interactive graphs will take you through the years of their music careers.")
st.subheader("Comparison")
st.write("Ever wondered how your favourite artists stack up against each other? Our comparison tool lets you visualize their journey side by side, helping you identify trends and differences.")
