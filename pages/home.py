import streamlit as st
from st_pages import add_page_title
import pandas as pd

def icon(image_path: str):
    """Shows an image as a Notion-style page icon."""
    st.image(image_path, width=158)

st.set_page_config(page_title="Home", page_icon="🏠")

with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)
col1, col2 = st.columns(2,1)
with col1:
    icon("Sound_Scout.png")
with col2:
    st.title("SOUND SCOUT")
