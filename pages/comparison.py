import PIL
from PIL import Image
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.header("Comparison")
plt.figure(figsize=(10, 6))
for artist in top_5_artists:
    artist_data = grouped[grouped['Artists'] == artist]
    plt.plot(artist_data['Year'], artist_data['Count'], label=artist)

plt.xlabel('Year')
plt.ylabel('Artist Count')
plt.title('Artist Count Over the Years - Top 5 Artists (User Provided)')
plt.legend()
st.pyplot(plt.gcf())
