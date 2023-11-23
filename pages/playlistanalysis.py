import streamlit as st
import spotipy
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import plotly.subplots as sub
import plotly.graph_objs as go
import plotly.express as px
import cohere
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import urllib.parse
from streamlit_extras.switch_page_button import switch_page 
st.set_page_config(page_title="Analysis of Playlist", page_icon="🎶",initial_sidebar_state="collapsed")
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = '6c535639a5994b69be734012a94f0f94'
SPOTIPY_CLIENT_SECRET = '8552e374f87f4d64b3cf46a0d085624c'
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
st.title('Spotify Playlist Analysis')
# Playlist ID
url = st.text_input('Enter the Spotify playlist link or playlist ID')
parsed_url = urllib.parse.urlparse(url)
playlist_id = parsed_url.path.split('/')[-1]

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

        fig = sub.make_subplots(rows=4, cols=3, subplot_titles=numeric_columns, horizontal_spacing=0.1, vertical_spacing=0.15)

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
        fig.update_layout(
                    height=800, 
                    width=900, 
                    title_text="Histograms of Audio Features", 
                    showlegend=False,
                    autosize=False,
                    margin=dict(
                        autoexpand=False,
                                l=70,
                                r=40,
                                t=110,
                        )
                    )

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

                fig = sub.make_subplots(rows=2, cols=3, subplot_titles=features, horizontal_spacing=0.15, vertical_spacing=0.15)

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
#                fig.update_layout(height=800, width=900, title_text="Histograms of Audio Features for Cluster " + str(i), showlegend=False)
                fig.update_layout(
                        height=800, width=900,
                        title_text="Histograms of Audio Features for Cluster " + str(i), 
                        showlegend=False,
                        autosize=False,
                        margin=dict(
                            autoexpand=False,
                                    l=70,
                                    r=40,
                                    t=110,
                        )
                    )
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
        def generate_insights_for_cluster(mean_values):
                    prompt = f"Generate insights in one paragraph of 100 words only for cluster based on the following mean values:\n"
                    for feature in mean_values:
                        prompt += f"{feature}: {mean_values[feature]}\n"

                    response = co.generate(
                        model='command',
                        prompt=prompt,
                        max_tokens=300,
                        temperature=0.9,
                        k=0,
                        stop_sequences=[],
                        return_likelihoods='NONE')

                    return response.generations[0].text
        co = cohere.Client('KyJVseeehAjgGERR23k1CgS8afQZwYku0OTX4HR9')
        for cluster_label in mean_df.columns:
        # Generate insights for the cluster
            insights = generate_insights_for_cluster(mean_df[cluster_label].to_dict())
            # Display the insights for the cluster
            st.markdown(f"## Insights for {cluster_label}:")
            st.markdown(f"<p>{insights}</p>", unsafe_allow_html=True)
except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 404:
                st.error("Playlist not found. Please check the playlist link or ID and try again.")
            else:
                st.error(f"An error occurred: {e}. Please try again with a different playlist ID.")
col1, col2, col3= st.columns(3)
st.markdown("""
    <style>
    div.stButton > button:first-child  {
    position: fixed;
    bottom: 10px;
}
</style>
    """, unsafe_allow_html=True)
with col1:
    pass
with col3:
    pass
with col2:
    if st.button('Take me Home 🏠'):
       switch_page("🏠 Home")