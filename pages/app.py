from pathlib import Path
import streamlit as st
with st.echo("below"):
    from st_pages import Page, Section, add_page_title, show_pages

    ## Declaring the pages in your app:

    show_pages(
        [
                Page("pages/home.py", "Home"),
            Section(name="Analysis of Artists"),
            Page("pages/top_5.py", "Top 5"),
            Page("pages/comparison.py", "Comparison"),
            Page("pages/analysisofgenre.py","Analysis of Genre",in_section=False),
            Page("pages/linear","LinearRegression")
        ]
    )
    add_page_title()
