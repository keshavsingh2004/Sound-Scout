import streamlit as st
from st_pages import add_page_title
import pandas as pd
from streamlit_extras.switch_page_button import switch_page 
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Home", page_icon="🏠",initial_sidebar_state="collapsed")
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)
# icon("Sound_Scout.png")
st.markdown("<h1 style='text-align: center; color: white;'>Sound Scout</h1>", unsafe_allow_html=True)
st.write("Welcome to SoundScout, where the power of music comes alive through analysis, exploration, and prediction.")
# st.subheader("What We Offer")
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("Analysis of Songs 🎵"):
        switch_page("🎵 Analysis of Songs")
with col2:
    if st.button("Analysis of Artists 🎤"):
        switch_page("🎤 Analysis of Artists")
with col3:
    if st.button("Analysis of Genre 🎧"):
        switch_page("🎧 Analysis of Genre")
with col4:
    if st.button("Genre Prediction 🔍"):
        switch_page("🔍 Genre Prediction")
with col5:
    if st.button("Analysis of Playlists 🎶"):
        switch_page("🎶 Analysis of Playlists")
with col6:
    if st.button("Melody Bot 💬"):
        switch_page("💬 Melody Bot")
st.write(" ")
st.info("Artist Insights: Uncover the artist's musical journey, compare artists side-by-side, and trace the trajectory of your favorites.\nGenre Exploration: Delve into the history of music genres, identify driving forces behind transformations, and predict future trends.\nPlaylist Analysis: Peek into the musical DNA of your playlists, identify patterns, and understand personal preferences.\nComprehensive Guide: Explore the music industry from artists to genres, gain insights, and become a music connoisseur.\nNuanced Understanding: Discover the sonic landscapes that resonate with your preferences, gain a deeper appreciation for music.")