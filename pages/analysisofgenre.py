import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(page_title="Genre Analysis", page_icon="🎧")
st.markdown("""
    ## Analysis of Genre
    
    Below is the Pie-Chart of the Genres of Music featured in BillBoard during 1999-2019
    
    """)

# Load and preprocess the dataset
df = pd.read_csv("billboard.csv")
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')
df['Genres'] = df['Genre'].str.split(',')
df = df.explode('Genre')

# Flatten the list of genres
genres_list = [genre for genres in df['Genres'] for genre in genres]

# Calculate the frequency of each genre
genre_counts = pd.Series(genres_list).value_counts()

top_20_genres = genre_counts.index[:20]
top_20_counts = genre_counts[:20]

# Select top 10 genres and group the rest as "Others"
top_genres = genre_counts.head(6)
other_count = genre_counts[6:].sum()
top_genres['Others'] = other_count

# Create a Pie chart using Plotly Express
fig = px.pie(top_genres, values=top_genres.values, names=top_genres.index, title='Genre Distribution')

# Display the chart using Streamlit
st.plotly_chart(fig)

# Plot a histogram of the top 20 genre counts
fig_hist = px.bar(top_20_counts, x=top_20_genres, y=top_20_counts.values,
                  labels={'x': 'Genre', 'y': 'Count'}, title='Top 20 Genre Counts')
fig_hist.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig_hist)



# Create a dropdown menu to select the genre
selected_genre = st.selectbox("Select a genre:", genre_counts.index)

# Filter the dataset for the selected genre
genre_data = df[df['Genre'].str.contains(selected_genre)]

# Group and aggregate data at the yearly level
grouped = genre_data.groupby('Year').size().reset_index(name='Count')

# Plot the graph of genre frequency over the years
fig = px.line(grouped, x='Year', y='Count', title='Genre Count Over the Years - Selected Genre: ' + selected_genre)
st.plotly_chart(fig)


genre_count = genre_counts[selected_genre]
st.write("Count of", selected_genre, ":", genre_count)
total_count = sum(genre_counts)
st.write("Total Count of All Genres:", total_count)
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)