import streamlit as st
from st_pages import add_page_title

add_page_title(layout="narrow")


st.title("Get the Most Out of Your Music Data with Music Insights")
st.write("At Music Insights, we've made understanding music data easier than ever. Whether you're a music enthusiast or a professional, our platform provides valuable insights into your favorite artists' performance over the years. Explore and analyze data for the top 5 artists, and gain a deeper appreciation for their music journey.")
st.header("What We Offer")
st.subheader("Top 5 Artists")
st.write("Discover the statistical journey of your favorite artist. Select from Taylor Swift, Elton John, Madonna, Drake, and Kenny Chesney. Our interactive graphs will take you through the years of their music careers.")
st.subheader("Comparison")
st.write("Ever wondered how your top 5 artists stack up against each other? Our comparison tool lets you visualize their journey side by side, helping you identify trends and differences.")
