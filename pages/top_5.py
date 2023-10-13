import PIL
from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px
#change
st.header("Artist Analysis")
df = pd.read_csv("charts.csv")

# Convert the 'Week' column to datetime format
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')

analysis_option = st.radio("Choose an analysis option:", ("Artist Discography over Time", "Artist Comparison"))

if analysis_option == "Artist Discography over Time":
    st.subheader("Artist Discography over Time")
    # Calculate the frequency of each artist
    artist_counts = df['Artists'].value_counts()

    # Get the top 5 artists from user input
    top_5_artists = ['Taylor Swift', 'Elton John', 'Madonna', 'Drake', 'Kenny Chesney','Travis Scott','Ed Sheeran','Doja Cat','Kendrick Lamar','Justin Bieber', 'One Direction', 'Zayn','Harry Styles','Niall Horan', 'The Weeknd']

    # Filter the dataset for the top 5 artists
    top_5_artists_data = df[df['Artists'].isin(top_5_artists)]

    # Group and aggregate data at the yearly level for the top 5 artists
    grouped = top_5_artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')
    selected_artist = st.selectbox("Select an artist:", [artist for artist in top_5_artists], index=0)

    # Plot the graph for the selected artist
    chart_data = grouped[grouped['Artists'] == selected_artist]
    fig = px.line(chart_data, x='Year', y='Count', title=f'Artist Count Over the Years - {selected_artist}')
    fig.update_traces(line=dict(color='green'))

    # Display the image and about us section for the selected artist
    if selected_artist == 'Taylor Swift':
        image = Image.open('image/taylor_swift.jpg')
        st.image(image, caption='Taylor Swift')
        st.markdown("""
            ## About Taylor Swift
            Taylor Swift is an American singer, songwriter, record producer, and actress. She is one of the most successful and influential artists of all time, with over 200 million records sold worldwide. She has won 11 Grammy Awards, 28 American Music Awards, 23 Billboard Music Awards, and seven Brit Awards.
            You can learn more about Taylor Swift at her [official website](https://www.taylorswift.com/) or follow her on [Facebook](https://www.facebook.com/taylorswift).
        """)
        st.plotly_chart(fig)

    elif selected_artist == 'Elton John':
        image = Image.open('image/elton_john.jpg')
        st.image(image, caption='Elton John')
        st.markdown("""
            ## About Elton John
            Elton John is a British singer, songwriter, pianist, and composer. He is one of the most acclaimed and best-selling music artists of all time, with over 300 million records sold worldwide. He has won five Grammy Awards, an Academy Award, a Golden Globe Award, a Tony Award, and a Disney Legends Award.
            You can learn more about Elton John at his [official website](https://www.eltonjohn.com/) or follow him on [Instagram](https://www.instagram.com/eltonofficial/).
        """)
        st.plotly_chart(fig)

    elif selected_artist == 'Madonna':
        image = Image.open('image/madonna.jpg')
        st.image(image, caption='Madonna')
        st.markdown("""
            ## About Madonna
            Madonna is an American singer, songwriter, actress, and businesswoman. She is known as the "Queen of Pop" and one of the most influential figures in popular culture. She has sold over 300 million records worldwide, making her the best-selling female music artist of all time. She has won seven Grammy Awards, two Golden Globe Awards, and a Billboard Woman of the Year Award.
            You can learn more about Madonna at her [official website](https://www.madonna.com/) or follow her on [Twitter](https://twitter.com/Madonna).
        """)
        st.plotly_chart(fig)

    elif selected_artist == 'Drake':
        image = Image.open('image/drake.jpg')
        st.image(image, caption='Drake')
        st.markdown("""
            ## About Drake
            Drake is a Canadian rapper, singer, songwriter, actor, and entrepreneur. He is one of the most popular and influential artists of his generation, with over 170 million records sold worldwide. He has won four Grammy Awards, six American Music Awards, 27 Billboard Music Awards, and two Brit Awards.
            You can learn more about Drake at his [official website](https://www.drakeofficial.com/) or follow him on [Instagram](https://www.instagram.com/champagnepapi/).
        """)
        st.plotly_chart(fig)

elif analysis_option == "Artist Comparison":
    st.subheader("Artist Comparison")
    # Get the unique list of artists
    unique_artists = df['Artists'].unique().tolist()

    # Ask the user to select artists using multiselect dropdown
    selected_artists = st.multiselect("Select artists:", unique_artists)

    if len(selected_artists) > 0:
        # Filter the dataset for the selected artists
        artists_data = df[df['Artists'].isin(selected_artists)]

        # Group and aggregate data at the yearly level for the selected artists
        grouped = artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')

        st.header("Comparison")

        # Create the Plotly line chart for the selected artists
        chart = px.line(grouped, x='Year', y='Count', color='Artists',
                        title="Artist Count Over the Years - Comparison")

        # Display the chart using Streamlit
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.write("Select Artists you want to compare")