import streamlit as st
from st_pages import add_page_title
import pandas as pd
from streamlit_extras.switch_page_button import switch_page 

# def icon(image_path: str):
#     """Shows an image as a Notion-style page icon."""
#     st.image(image_path, width=175)

st.set_page_config(page_title="Home", page_icon="🏠",initial_sidebar_state="collapsed")
def redirect_button(url: str, text: str = None, color="rgba(0, 0, 0, 0.3)"):
    st.markdown(
        f"""
        <style>
        .button-container {{
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 10px;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }}
        
        .button-container:hover {{
            background-color: rgba(0, 0, 0, 1);
        }}
        </style>
        
        <a href="{url}" target="_self">
            <div class="button-container">
                {text}
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)
# icon("Sound_Scout.png")
st.markdown("<h1 style='text-align: center; color: white;'>Sound Scout</h1>", unsafe_allow_html=True)
st.write("Welcome to SoundScout, where the power of music comes alive through analysis, exploration, and prediction.")
# st.subheader("What We Offer")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("Analysis of Songs"):
        switch_page("🎵 Analysis of Songs")
with col2:
    redirect_button("https://sound-scout.streamlit.app/%F0%9F%8E%A4%20Analysis%20of%20Artists","Analysis of Artists")
with col3:
    redirect_button("https://sound-scout.streamlit.app/%F0%9F%8E%A7%20Genre%20Analysis","Analysis of Genre")
with col4:
    redirect_button("https://sound-scout.streamlit.app/%F0%9F%94%8D%20Genre%20Prediction","Genre Prediction")
with col5:
    redirect_button("https://sound-scout.streamlit.app/%F0%9F%8E%B6%20Analysis%20of%20Playlists","Analysis of Playlists")
st.write(" ")
st.info("Our platform offers a multifaceted exploration of the music industry, delving into both artist-specific and genre-wide analyses. For artists, we provide an extensive discography and a tool for insightful comparisons, enabling enthusiasts and professionals alike to trace the trajectory of their favorite musicians. Moving to genres, we don't just scratch the surface but conduct a thorough examination of their evolution, offering a deep dive into the historical shifts and trends that have shaped musical landscapes. For those curious about the future, our genre prediction feature employs machine learning algorithms, allowing users to visualize and compare predictions against actual data. Our playlist analysis goes beyond the surface, dissecting the intricate features of each song to uncover trends in tempo, mood, and instrumentation. Dive deep into the musical DNA of your playlists, gaining valuable insights into the sonic landscapes that resonate with your preferences. Our platform is a comprehensive guide for anyone seeking a nuanced understanding of the dynamic world of music.")
