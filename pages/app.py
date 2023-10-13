from pathlib import Path
import streamlit as st
with st.echo("below"):
    from st_pages import Page, Section, add_page_title, show_pages

    ## Declaring the pages in your app:

    show_pages(
        [
            Page("pages/home.py", "Home"),
            Page("pages/top_5.py", "Analysis of Artists"),
            Page("pages/analysisofgenre.py","Analysis of Genre"),
            Page("pages/linear.py","Prediction of Genre"),
        ]
    )
    add_page_title()
