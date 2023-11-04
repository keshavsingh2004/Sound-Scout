import streamlit as st
import spotipy
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import plotly.subplots as sub
import plotly.graph_objs as go
import plotly.express as px

from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
st.set_page_config(page_title="Analysis of Playlist", page_icon="🎶")
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = '6c535639a5994b69be734012a94f0f94'
SPOTIPY_CLIENT_SECRET = '8552e374f87f4d64b3cf46a0d085624c'
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
st.title('Spotify Playlist Analysis')
# Playlist ID
playlist_link = st.text_input('Enter the Spotify playlist link or playlist ID')
playlist_id = playlist_link.split('/')[-1]
#playlist_id = '561Z6T9i38xWLoPQIMIbBs'
try:
    if playlist_id:
        playlist_info = []
        tracklist = []
        tracks = sp.playlist_tracks(playlist_id)
        tracklist += tracks['items']
        spotify_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
        st.markdown(f"""
            <iframe style="border-radius:12px" src="{spotify_url}" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            <br><br>
            """, unsafe_allow_html=True)
        # Fetch playlist tracks from Spotify API


        while tracks['next']:
            tracks = sp.next(tracks)
            tracklist += tracks['items']

        # Extract track information
        for track in tracklist:
            info = track['track']
            playlist_info.append((info['id'], info['name'], info['artists'][0]['name'], info['album']['name'], info['album']['id']))

        # Create DataFrame with track information
        data = pd.DataFrame(playlist_info, columns=['id', 'name', 'artist', 'album', 'album_id'])

        # Extract audio features for each song
        audio_features_ids = [track['track']['id'] for track in tracklist]
        audio_features = []

        for i in range(0, len(audio_features_ids), 50):
            audio_features_batch = sp.audio_features(audio_features_ids[i:i+50])
            audio_features += audio_features_batch

        # Create DataFrame with audio features
        audio_features_df = pd.DataFrame(audio_features)
        audio_features_df = audio_features_df[['id', 'danceability', 'energy', 'key', 'loudness', 'mode',
                                            'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence',
                                            'tempo', 'duration_ms', 'time_signature']]

        # Merge track information with audio features
        merged_df = pd.merge(data, audio_features_df, on='id')

        # Feature analysis
        numeric_columns = ['danceability', 'energy', 'key', 'loudness', 'mode',
                        'speechiness', 'acousticness', 'instrumentalness',
                        'liveness', 'valence', 'tempo',
                        'duration_ms', 'time_signature']
        correlation_matrix = merged_df[numeric_columns].corr()

        # Streamlit app
        st.subheader('Correlation Heatmap between Audio Features')
        st.text('Playlist ID: ' + playlist_id)

        # Create the correlation heatmap with seaborn and matplotlib
        fig, ax = plt.subplots(figsize=(14, 10))
        heatmap = sns.heatmap(correlation_matrix, annot=True, fmt='.2f', linewidths=1, linecolor='black', ax=ax)
        heatmap.set_title('Correlation Heatmap between Audio Features')
        heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=45, horizontalalignment='right')

        # Display the heatmap with streamlit
        st.pyplot(fig)

        # Select numeric columns for histograms
        numeric_columns = ['danceability', 'energy', 'key', 'loudness', 'mode',
                        'speechiness', 'acousticness', 'instrumentalness',
                        'liveness', 'valence', 'tempo',
                        'duration_ms']

        data_numeric = merged_df[numeric_columns]

        # Create a subplot with 4 rows and 3 columns using plotly.subplots
        fig = sub.make_subplots(rows=4, cols=3, subplot_titles=numeric_columns)

        # Add histograms to the subplot using plotly.graph_objs.Histogram
        for i, col in enumerate(data_numeric.columns):
            fig.add_trace(
                go.Histogram(x=data_numeric[col], nbinsx=50, name=col),
                row=i//3 + 1,
                col=i%3 + 1
            )
            # Add x and y labels using fig.update_xaxes and fig.update_yaxes
            fig.update_xaxes(title_text="Value", row=i//3 + 1, col=i%3 + 1)
            fig.update_yaxes(title_text="Frequency", row=i//3 + 1, col=i%3 + 1)

        # Update layout for a nice fit using fig.update_layout
        fig.update_layout(height=800, width=900, title_text="Histograms of Audio Features", showlegend=False)

        # Display the figure using streamlit.plotly_chart
        st.plotly_chart(fig)

        # Clustering songs
        X = audio_features_df[numeric_columns]
        distorsions = []
        for k in range(2,10):
            model = KMeans(n_clusters=k)
            model.fit(X)
            distorsions.append(model.inertia_)

        # Plotting Elbow Curve with Plotly
        fig = px.line(x=range(2,10), y=distorsions, labels={'x':'k', 'y':'Distortion'}, title='Elbow Curve')
        st.plotly_chart(fig)

        # Training data with optimal clusters (change this to your optimal number of clusters)
        model = KMeans(n_clusters=4)
        model.fit(X)

        y = model.predict(X) #Each song goes to the cluster which has the most similarities in their features

        # PCA for dimensionality reduction
        pca = PCA(n_components=2) #2 dimensions
        pc = pca.fit_transform(X) #Fit the model with X and apply the dimensionality reduction on X

        #Creating a data frame with the results from the dimensionality reduction (in order to display the data in 2d)
        pca_df = pd.DataFrame(pc, columns=['Principal Component 1', 'Principal Component 2']) 
        pca_df['label'] = y

        # Plotting PCA results with Plotly
        fig = px.scatter(pca_df, x='Principal Component 1', y='Principal Component 2', color='label', title="Songs' Clustering Visualization with PCA")
        st.plotly_chart(fig)

        cluster_counts = pd.Series(y).value_counts().reset_index().rename(columns={'index': 'Cluster', 0: 'count'})

        # Create a bar chart with Plotly
        fig = px.bar(cluster_counts, x='Cluster', y='count', 
                    labels={'Cluster':'Clusters', 'count':'Number of songs'}, 
                    title='Number of songs in each cluster')

        # Display the figure with Streamlit
        st.plotly_chart(fig)

        features = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'valence']

        # Create lists for each cluster
        l0 = []
        l1 = []
        l2 = []
        l3 = []
        audio_features_df.loc[:, 'label'] = y
        audio_features_df.head(10)
        # Append songs to their respective cluster list
        for k,v in enumerate(audio_features_df['id']):
            if y[k] == 0:
                l0.append(v)
            elif y[k] == 1:
                l1.append(v)
            elif y[k] == 2:
                l2.append(v)
            else:
                l3.append(v)


        # Plot histograms of each audio feature for each 
        tabs = st.tabs(["Cluster 0", "Cluster 1", "Cluster 2", "Cluster 3"])

        for i in range(len(tabs)):
            with tabs[i]:

                # Create a figure for the corresponding cluster
                fig = sub.make_subplots(rows=2, cols=3, subplot_titles=features)

                for j, feature in enumerate(features):
                    hist = go.Histogram(
                        x=audio_features_df.loc[:, feature][audio_features_df['label'] == i],
                        nbinsx=50,
                        name=feature,
                    )
                    fig.add_trace(hist, row=j // 3 + 1, col=j % 3 + 1)
                    fig.update_xaxes(title_text="Value", row=j // 3 + 1, col=j % 3 + 1)
                    fig.update_yaxes(title_text="Frequency", row=j // 3 + 1, col=j % 3 + 1)

                # Update the layout of the figure and display it
                fig.update_layout(height=800, width=900, title_text="Histograms of Audio Features for Cluster " + str(i), showlegend=False)
                st.plotly_chart(fig)

        # Calculate mean values of each audio feature for each cluster
        mean_cluster0 = audio_features_df.loc[:,features][audio_features_df['label'] == 0].mean()
        mean_cluster1 = audio_features_df.loc[:,features][audio_features_df['label'] == 1].mean()
        mean_cluster2 = audio_features_df.loc[:,features][audio_features_df['label'] == 2].mean()
        mean_cluster3 = audio_features_df.loc[:,features][audio_features_df['label'] == 3].mean()

        # Create DataFrame with mean values
        mean_df = pd.DataFrame(mean_cluster0, columns=['Cluster 0'])
        mean_df['Cluster 1'] = mean_cluster1
        mean_df['Cluster 2'] = mean_cluster2
        mean_df['Cluster 3'] = mean_cluster3

        # Display DataFrame with Streamlit
        st.dataframe(mean_df)
        # Display insights for each cluster
        st.header("Insights:")
        st.write('**Cluster 0**: This cluster is characterized by a moderate danceability score of 0.582, suggesting that the songs in this cluster have a balanced rhythm and beat that could be suitable for dancing. The energy level of these songs is relatively high (0.6636), indicating that they are likely to be fast, loud, and noisy. The acousticness score of 0.1764 suggests that many songs in this cluster have an acoustic quality. However, the valence score of 0.5523 indicates that the songs are not particularly happy or cheerful.')

        st.write('**Cluster 1**: Songs in this cluster are energetic with a high energy score of 0.6988, suggesting that they are likely to be fast and noisy. The danceability score of 0.6005 indicates that these songs are suitable for dancing. However, the valence score of 0.6751 suggests that these songs may not evoke positive feelings such as happiness or cheerfulness.')

        st.write('**Cluster 2**: This cluster has the highest danceability score of 0.6087, making it the most suitable for dancing. The songs in this cluster are also loud and noisy, as indicated by the high energy score of 0.6933. However, the valence score of 0.6163 suggests that these songs may not be particularly cheerful or happy.')

        st.write('**Cluster 3**: Songs in this cluster have a lower danceability score of 0.471 compared to other clusters, suggesting that they may not be as suitable for dancing. However, these songs tend to be cheerful, as indicated by the higher valence score of 0.4582. The energy level of these songs is relatively high (0.6678), indicating that they are likely to be fast and noisy.')
except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 404:
                st.error("Playlist not found. Please check the playlist ID and try again.")
            else:
                st.error(f"An error occurred: {e}. Please try again with a different playlist ID.")