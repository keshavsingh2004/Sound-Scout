import streamlit as st
from st_pages import add_page_title
import pandas as pd

def icon(image_path: str):
    """Shows an image as a Notion-style page icon."""
    st.image(image_path, width=175)

st.set_page_config(page_title="Home", page_icon="🏠")
def redirect_button(url: str, text: str= None, color="#FD504D"):
    st.markdown(
    f"""
    <a href="{url}" target="_self">
        <div style="
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
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
# with col2:
#     st.title("SOUND SCOUT")
st.caption("A In-Depth Analysis of Everything you like about Music")
st.header("What We Offer")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    redirect_button("https://sound-scout.streamlit.app/%F0%9F%8E%B5%20Analysis%20of%20Songs","Analysis of Songs")
# with col2:

# with col3:
    
# with col4:
    
# with col5:
    