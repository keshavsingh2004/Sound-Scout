import streamlit as st
from st_pages import add_page_title
import pandas as pd

def icon(image_path: str):
    """Shows an image as a Notion-style page icon."""
    st.image(image_path, width=175)

st.set_page_config(page_title="Home", page_icon="🏠")

with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)
icon("Sound_Scout.png")
# with col2:
#     st.title("SOUND SCOUT")
st.caption("A In-Depth Analysis of Everything you like about Music")
st.header("What We Offer")
st.markdown('<a href="/?key=value" target="_self">View all</a>',unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown('<a href="https://sound-scout.streamlit.app/%F0%9F%8E%B5%20Analysis%20of%20Songs" target="_self">Analysis of Songs</a>', unsafe_allow_html=True)
with col2:
    st.markdown('<a href="https://sound-scout.streamlit.app/%F0%9F%8E%A4%20Analysis%20of%20Artists" target="_self">Analysis of Artists</a>', unsafe_allow_html=True)
with col3:
    st.markdown('<a href="https://sound-scout.streamlit.app/%F0%9F%8E%A7%20Genre%20Analysis" target="_self">Analysis of Genre</a>', unsafe_allow_html=True)
with col4:
    st.markdown('<a href="https://sound-scout.streamlit.app/%F0%9F%94%8D%20Genre%20Prediction" target="_self">Genre Prediction</a>', unsafe_allow_html=True)
with col5:
    st.markdown('<a href="https://sound-scout.streamlit.app/%F0%9F%8E%B6%20Analysis%20of%20Playlists" target="_self">Analysis of Playlists</a>', unsafe_allow_html=True)