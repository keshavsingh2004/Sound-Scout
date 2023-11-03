import requests
import base64

import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import seaborn as sns
import streamlit as st
from PIL import Image

def get_token(clientId,clientSecret):
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}
    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')
    headers['Authorization'] = "Basic " + base64Message
    data['grant_type'] = "client_credentials"
    r = requests.post(url, headers=headers, data=data)
    token = r.json()['access_token']
    return token


def get_track_recommendations(seed_tracks,token):
    limit = 10
    recUrl = f"https://api.spotify.com/v1/recommendations?limit={limit}&seed_tracks={seed_tracks}"

    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=recUrl, headers=headers)
    return res.json()

# def song_recommendation_vis(reco_df):    
#     reco_df['duration_min'] = round(reco_df['duration_ms'] / 1000, 0)
#     reco_df["popularity_range"] = reco_df["popularity"] - (reco_df['popularity'].min() - 1)
    
#     plt.figure(figsize=(15, 6), facecolor=(.9, .9, .9))    

#     x = reco_df['name']
#     y = reco_df['duration_min']
#     s = reco_df['popularity_range']*20
        
#     color_labels = reco_df['explicit'].unique()
#     rgb_values = sns.color_palette("Set1", 8)
#     color_map = dict(zip(color_labels, rgb_values))

#     plt.scatter(x, y, s, alpha=0.7, c=reco_df['explicit'].map(color_map))
#     plt.xticks(rotation=90)
#     plt.legend()
#     # show the graph
#     plt.show()
    
#     st.pyplot(plt)

def song_recommendation_vis(reco_df):
    #reco_df['Duration_min'] = round(reco_df['duration_ms'] / 1000, 0)
    reco_df["Popularity_range"] = reco_df["Popularity"] - (reco_df['Popularity'].min() - 1)
    reco_df["Name"]=reco_df["Name"]
    reco_df["Explicit"]=reco_df["Explicit"]

    fig = px.scatter(reco_df, x='Name', y='Similarity(%)', size='Popularity_range', color='Explicit',
                     color_discrete_map={0: 'blue', 1: 'red'}, title='Song Recommendations')

    fig.update_xaxes(tickangle=90)
    fig.update_layout(width=800, height=500)

    st.plotly_chart(fig)

def save_album_image(img_url, track_id):
    r = requests.get(img_url)
    open('img/' + track_id + '.jpg', "wb").write(r.content)
    
def get_album_mage(track_id):
    return Image.open('img/' + track_id + '.jpg')

def calculate_euclidean_distance(original_features, selected_features):
    # Calculate the squared difference between each feature, weighted by its importance.
    weights=[0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    squared_weighted_differences = []
    for i in range(7):
        squared_weighted_differences.append((original_features[i] - selected_features[i]) ** 2 * weights[i])

    # Sum the squared weighted differences.
    sum_of_squared_weighted_differences = sum(squared_weighted_differences)

    # Take the square root of the sum of the squared weighted differences.
    weighted_euclidean_distance = sum_of_squared_weighted_differences ** 0.5

    return weighted_euclidean_distance
