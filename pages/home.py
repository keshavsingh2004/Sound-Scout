import streamlit as st
from st_pages import add_page_title
import pandas as pd

def icon(image_path: str):
    """Shows an image as a Notion-style page icon."""
    st.image(image_path, width=175)

st.set_page_config(page_title="Home", page_icon="🏠",initial_sidebar_state="collapsed")
def redirect_button(url: str, text: str = None, color="rgba(0, 0, 0, 0.5)"):
    st.markdown(
        f"""
        <a href="{url}" target="_self">
            <div style="
                display: inline-block;
                padding: 0.5em 1em;
                color: #FFFFFF;
                background-color: {color};
                border-radius: 10px;
                text-decoration: none;">
                {text}
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )

with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)
icon("Sound_Scout.png")
st.caption("In-Depth Analysis of Everything you like about Music")
st.header("What We Offer")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    redirect_button("https://sound-scout.streamlit.app/%F0%9F%8E%B5%20Analysis%20of%20Songs","Analysis of Songs")
with col2:
    redirect_button("https://sound-scout.streamlit.app/%F0%9F%8E%A4%20Analysis%20of%20Artists","Analysis of Artists")
with col3:
    redirect_button("https://sound-scout.streamlit.app/%F0%9F%8E%A7%20Genre%20Analysis","Genre Analysis")
with col4:
    redirect_button("https://sound-scout.streamlit.app/%F0%9F%94%8D%20Genre%20Prediction","Genre Prediction")
with col5:
    redirect_button("https://sound-scout.streamlit.app/%F0%9F%8E%B6%20Analysis%20of%20Playlists","Analysis of Playlists")