import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

df = pd.read_csv("charts.csv")


# Convert year column to datetime format
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')

# Calculate the frequency of each artist
artist_counts = df['Artists'].value_counts()

# Get the top 5 artists from user input
top_5_artists = ['Taylor Swift', 'Elton John', 'Madonna', 'Drake', 'Kenny Chesney']

# Filter the dataset for the top 5 artists
top_5_artists_data = df[df['Artists'].isin(top_5_artists)]

# Group and aggregate data at the yearly level for the top 5 artists
grouped = top_5_artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')

# Create a Streamlit sidebar with two select boxes, one for "Top 5" and one for "Comparison".
with st.sidebar:
    selected_option = st.selectbox("Select an option:", ["Top 5", "Comparison"], index=0)

    if selected_option == "Top 5":
        selected_artist = st.selectbox("Select an artist:", top_5_artists, index=0)

# Display the corresponding graph based on the selected option.
if selected_option == "Top 5":

    # Plot the graph for the selected artist
    plt.figure(figsize=(10, 6))
    artist_data = grouped[grouped['Artists'] == selected_artist]
    plt.plot(artist_data['Year'], artist_data['Count'], label=selected_artist)

    plt.xlabel('Year')
    plt.ylabel('Artist Count')
    plt.title('Artist Count Over the Years - ' + selected_artist + ' (User Provided)')
    plt.legend()
    plt.show()


    # Display the image and about us section for the selected artist
    if selected_artist == 'Taylor Swift':
        image = Image.open('keshavsingh2004/music-artist-trends/taylor_swift.jpg')
        st.image(image, caption='Taylor Swift')
        st.markdown("""
        ## About Taylor Swift

        Taylor Swift is an American singer, songwriter, record producer, and actress. She is one of the most successful and influential artists of all time, with over 200 million records sold worldwide. She has won 11 Grammy Awards, 28 American Music Awards, 23 Billboard Music Awards, and seven Brit Awards.

        You can learn more about Taylor Swift at her [official website] or follow her on [Facebook].
        """)
        # Display the line chart for the selected artist
        st.pyplot(plt.gcf())
    elif selected_artist == 'Elton John':
        image = Image.open('keshavsingh2004/music-artist-trends/elton_john.jpg')
        st.image(image, caption='Elton John')
        st.markdown("""
        ## About Elton John

        Elton John is a British singer, songwriter, pianist, and composer. He is one of the most acclaimed and best-selling music artists of all time, with over 300 million records sold worldwide. He has won five Grammy Awards, an Academy Award, a Golden Globe Award, a Tony Award, and a Disney Legends Award.

        You can learn more about Elton John at his [official website] or follow him on [Instagram].
        """)
        # Display the line chart for the selected artist
        st.pyplot(plt.gcf())
    elif selected_artist == 'Madonna':
        image = Image.open('keshavsingh2004/music-artist-trends/madona.jpg')
        st.image(image, caption='Madonna')
        st.markdown("""
        ## About Madonna

        Madonna is an American singer, songwriter, actress, and businesswoman. She is known as the "Queen of Pop" and one of the most influential figures in popular culture. She has sold over 300 million records worldwide, making her the best-selling female music artist of all time. She has won seven Grammy Awards, two Golden Globe Awards, and a Billboard Woman of the Year Award.

        You can learn more about Madonna at her [official website] or follow her on [Twitter].
        """)
        # Display the line chart for the selected artist
        st.pyplot(plt.gcf())
    elif selected_artist == 'Drake':
        image = Image.open('keshavsingh2004/music-artist-trends/drake.jpg')
        st.image(image, caption='Drake')
        st.markdown("""
        ## About Drake

        Drake is a Canadian rapper, singer, songwriter, actor, and entrepreneur. He is one of the most popular and influential artists of his generation, with over 170 million records sold worldwide. He has won four Grammy Awards, six American Music Awards, 27 Billboard Music Awards, and two Brit Awards.

        You can learn more about Drake at his [official website] or follow him on [Instagram].
        """)
        # Display the line chart for the selected artist
        st.pyplot(plt.gcf())
    elif selected_artist == 'Kenny Chesney':
        image = Image.open('keshavsingh2004/music-artist-trends/kenny_chesney.jpg')
        st.image(image, caption='Kenny Chesney')
        st.markdown("""
        ## About Kenny Chesney

        Kenny Chesney is an American country music singer, songwriter, and record producer. He is one of the most successful and award-winning country music artists of all time, with over 30 million albums sold worldwide. He has won nine Academy of Country Music Awards, six Country Music Association Awards, and four Billboard Music Awards.

        You can learn more about Kenny Chesney at his [official website] or follow him on [Facebook].
        """)
        # Display the line chart for the selected artist
        st.pyplot(plt.gcf())

elif selected_option == "Comparison":

    # Plot the graph for the top 5 artistss
    plt.figure(figsize=(10, 6))
    for artists in top_5_artists:
        artists_data = grouped[grouped['Artists'] == artists]
        plt.plot(artists_data['Year'], artists_data['Count'], label=artists)

    plt.xlabel('Year')
    plt.ylabel('Artist Count')
    plt.title('Artist Count Over the Years - Top 5 Artists (User Provided)')
    plt.legend()
    plt.show()

    # Display the line chart for the top 5 artists
    st.pyplot(plt.gcf())
