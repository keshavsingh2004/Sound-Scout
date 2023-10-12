import PIL
from PIL import Image
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit_elements as se

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

# Wrap the existing `plt.plot()` code in a `with elements("nivo_charts"):` block.
with se.elements("nivo_charts"):
    # Replace the `plt.plot()` function with the corresponding Nivo chart function, such as `nivo.Line()`.
    nivo.Line(
        data=grouped,
        x="Year",
        y="Count",
        keys=top_5_artists,
        colors=["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF"],
        curve="basis",
        strokeWidth={ "value": 2 },
        lineWidth={ "value": 2 },
        enableGridY={ "axis": "y" },
        enableGridX={ "axis": "x" },
        enableDots={ "value": True },
        dotSize={ "value": 6 },
        dotColor={ "from": "color" },
        dotBorderWidth={ "value": 2 },
        dotBorderColor={ "from": "color" },
        enableLegend={ "value": True },
        margin={ "top": 20, "right": 80, "bottom": 50, "left": 80 },
        xTickValues={ "value": grouped['Year'].unique() },
        yTickValues={ "value": range(0, grouped['Count'].max() + 10, 10) },
        theme={
            "background": "#FFFFFF",
            "textColor": "#31333F",
            "tooltip": {
                "container": {
                    "background": "#FFFFFF",
                    "color": "#31333F",
                }
            }
        }
    )