import streamlit as st
from st_pages import add_page_title
import pandas as pd
from streamlit_extras.switch_page_button import switch_page 
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Home", page_icon="🏠", initial_sidebar_state="collapsed")

with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)

# Display the title of the app
st.markdown("<h1 style='text-align: center; color: white;'>Sound Scout</h1>", unsafe_allow_html=True)
st.write("Welcome to SoundScout, where the power of music comes alive through analysis, exploration, and prediction.")

# Create a row of buttons for navigating to different pages
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    if st.button("Analysis of Songs"):
        switch_page("2_🎵_Analysis_of_Songs.py")

with col2:
    if st.button("Analysis of Artists"):
        switch_page("3_🎤_Analysis_of_Artists.py")

with col3:
    if st.button("Analysis of Genre"):
        switch_page("4_🎧_Analysis_of_Genre.py")

with col4:
    if st.button("Genre Prediction"):
        switch_page("5_🔍_Genre_Prediction.py")

with col5:
    if st.button("Analysis of Playlists"):
        switch_page("6_🎶_Analysis_of_Playlists.py")

with col6:
    if st.button("Melody Chat"):
        switch_page("7_💬_Melody_Chat.py")

with col7:
    if st.button("Generate Songs"):
        switch_page("8_🎙️_Generate_Songs.py")

# Provide information about the platform
st.write(" ")
st.info(
    "Our platform offers a multifaceted exploration of the music industry, delving into both artist-specific and genre-wide analyses. For artists, we provide an extensive discography and a tool for insightful comparisons, enabling enthusiasts and professionals alike to trace the trajectory of their favorite musicians. Moving to genres, we don't just scratch the surface but conduct a thorough examination of their evolution, offering a deep dive into the historical shifts and trends that have shaped musical landscapes. For those curious about the future, our genre prediction feature employs machine learning algorithms, allowing users to visualize and compare predictions against actual data. Our playlist analysis goes beyond the surface, dissecting the intricate features of each song to uncover trends in tempo, mood, and instrumentation. Dive deep into the musical DNA of your playlists, gaining valuable insights into the sonic landscapes that resonate with your preferences. Our platform is a comprehensive guide for anyone seeking a nuanced understanding of the dynamic world of music."
)
