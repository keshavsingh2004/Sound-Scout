from pathlib import Path
import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages

# Declaring the pages in your app 📄:
col1, col2, col3 = st.sidebar.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.image('Sound_Scout.png',  use_column_width=True)
with col3:
    st.write("")

show_pages(
        [
            Page("pages/home.py", "🏠 Home"),
            Page("pages/analysisofsongs.py","🎵 Analysis of Songs"),
            Page("pages/analysisofartists.py", "🎤 Analysis of Artists"),
            Page("pages/analysisofgenre.py","🎧 Genre Analysis"),
            Page("pages/genreprediction.py","🔍 Genre Prediction"),
            Page("pages/playlistanalysis.py","🎶 Analysis of Playlists")  
        ]
    )
add_page_title()
