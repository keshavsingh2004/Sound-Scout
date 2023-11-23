import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

st.set_page_config(page_title="Analysis of Genre", page_icon="🎧",initial_sidebar_state="collapsed")
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)
st.title("Analysis of Genre")
st.write("PieChart")

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

st.write("BarGraph")

# Plot a histogram of the top 20 genre counts
fig_hist = px.bar(top_20_counts, x=top_20_genres, y=top_20_counts.values,
                  labels={'x': 'Genre', 'y': 'Count'}, title='Top 20 Genres')
fig_hist.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig_hist)

# st.write("Clusters")

# def load_data():
#     genre_data = pd.read_csv('data_by_genres.csv')
#     return genre_data

# genre_data = load_data()

# cluster_pipeline = Pipeline([('scaler', StandardScaler()), ('kmeans', KMeans(n_clusters=10))])
# X = genre_data.select_dtypes(np.number)
# cluster_pipeline.fit(X)
# genre_data['cluster'] = cluster_pipeline.predict(X)

# # Visualizing the Clusters with t-SNE

# tsne_pipeline = Pipeline([('scaler', StandardScaler()), ('tsne', TSNE(n_components=2, verbose=1))])
# genre_embedding = tsne_pipeline.fit_transform(X)
# projection = pd.DataFrame(columns=['x', 'y'], data=genre_embedding)
# projection['genres'] = genre_data['genres']
# projection['cluster'] = genre_data['cluster']

# fig = px.scatter(
#     projection,
#     x='x',
#     y='y',
#     color='cluster',
#     hover_data=['x', 'y', 'genres'],
#     width=700,
#     height=500,
#     title="SNE Plot of Music Genres",
# )

# st.plotly_chart(fig)

st.write("Analysis of a selected Genre")



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


col1, col2, col3 , col4, col5 = st.columns(5)
with col1:
    pass
with col2:
    pass
with col4:
    pass
with col5:
    pass
with col3 :
    if st.button('Take me Home 🏠'):
       switch_page("🏠 Home")