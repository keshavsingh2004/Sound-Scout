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
st.subheader("What We Offer")
col1, col2, col3, col4, col5 = st.columns(5)