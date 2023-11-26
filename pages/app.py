from pathlib import Path
import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages


show_pages(
        [
            Page("pages/home.py", "🏠 Home"),
            Page("pages/analysisofsongs.py","🎵 Analysis of Songs"),
            Page("pages/analysisofartists.py", "🎤 Analysis of Artists"),
            Page("pages/analysisofgenre.py","🎧 Analysis of Genre"),
            Page("pages/genreprediction.py","🔍 Genre Prediction"),
            Page("pages/playlistanalysis.py","🎶 Analysis of Playlists"),
            Page("pages/chatbot.py","📝 Song Insights")  
        ]
    )
add_page_title()
