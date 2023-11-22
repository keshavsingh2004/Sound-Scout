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
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown('Please <a href="https://happylife.streamlit.app" target="_self">click</a>', unsafe_allow_html=True)
with col2:
    st.subheader("Analysis of Artist")
with col3:
    st.subheader("Analysis of Genre")
with col4:
    st.subheader("Genre Prediction")
with col5:
    st.subheader("Analysis of Playlists")