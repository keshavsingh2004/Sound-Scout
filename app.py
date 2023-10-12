import PIL
from PIL import Image
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load and preprocess the dataset
df = pd.read_csv("charts.csv")

# Convert the 'Week' column to datetime format
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')

# Calculate the frequency of each artist
artist_counts = df['Artists'].value_counts()

# Get the top 5 artists from user input
top_5_artists = ['Taylor Swift', 'Elton John', 'Madonna', 'Drake', 'Kenny Chesney']

# Filter the dataset for the top 5 artists
top_5_artists_data = df[df['Artists'].isin(top_5_artists)]

# Group and aggregate data at the yearly level for the top 5 artists
grouped = top_5_artists_data.groupby(['Year', 'Artists']).size().reset_index(name='Count')

# Create a Streamlit sidebar with two select boxes, one for "Home Page" and one for "About Us".
selected_option = st.sidebar.selectbox("Select an option:", ["Home Page", "About Us"], index=0)

if selected_option == "Home Page":
    # Create a new sidebar with options for "Top 5" and "Comparison" when "Home Page" is selected
    with st.sidebar:
        selected_option = st.selectbox("Select an option:", ["Top 5", "Comparison"], index=0)

    if selected_option == "Top 5":
        # Allow the user to search for an artist
        st.header("Top 5 Artists")
        search_artist = st.text_input("Search for an artist:")
        selected_artist = st.selectbox("Select an artist:", [artist for artist in top_5_artists if search_artist.lower() in artist.lower()], index=0)

        # Plot the graph for the selected artist
        plt.figure(figsize=(10, 6))
        artist_data = grouped[grouped['Artists'] == selected_artist]
        plt.plot(artist_data['Year'], artist_data['Count'], label=selected_artist)

        plt.xlabel('Year')
        plt.ylabel('Artist Count')
        plt.title('Artist Count Over the Years - ' + selected_artist + ' (User Provided)')
        plt.legend()

        # Display the image and about us section for the selected artist
        if selected_artist == 'Taylor Swift':
            image = Image.open('image/taylor_swift.jpg')
            st.image(image, caption='Taylor Swift')
            st.markdown("""
            ## About Taylor Swift

            Taylor Swift is an American singer, songwriter, record producer, and actress. She is one of the most successful and influential artists of all time, with over 200 million records sold worldwide. She has won 11 Grammy Awards, 28 American Music Awards, 23 Billboard Music Awards, and seven Brit Awards.

            You can learn more about Taylor Swift at her [official website] or follow her on [Facebook].
            """)
            # Display the line chart for the selected artist
            st.pyplot(plt.gcf())

        elif selected_artist == 'Elton John':
            image = Image.open('image/elton_john.jpg')
            st.image(image, caption='Elton John')
            st.markdown("""
            ## About Elton John

            Elton John is a British singer, songwriter, pianist, and composer. He is one of the most acclaimed and best-selling music artists of all time, with over 300 million records sold worldwide. He has won five Grammy Awards, an Academy Award, a Golden Globe Award, a Tony Award, and a Disney Legends Award.

            You can learn more about Elton John at his [official website] or follow him on [Instagram].
            """)
            st.pyplot(plt.gcf())

        elif selected_artist == 'Madonna':
            image = Image.open('image/madonna.jpg')
            st.image(image, caption='Madonna')
            st.markdown("""
            ## About Madonna

            Madonna is an American singer, songwriter, actress, and businesswoman. She is known as the "Queen of Pop" and one of the most influential figures in popular culture. She has sold over 300 million records worldwide, making her the best-selling female music artist of all time. She has won seven Grammy Awards, two Golden Globe Awards, and a Billboard Woman of the Year Award.

            You can learn more about Madonna at her [official website] or follow her on [Twitter].
            """)
            st.pyplot(plt.gcf())

        elif selected_artist == 'Drake':
            image = Image.open('image/drake.jpg')
            st.image(image, caption='Drake')
            st.markdown("""
            ## About Drake

            Drake is a Canadian rapper, singer, songwriter, actor, and entrepreneur. He is one of the most popular and influential artists of his generation, with over 170 million records sold worldwide. He has won four Grammy Awards, six American Music Awards, 27 Billboard Music Awards, and two Brit Awards.

            You can learn more about Drake at his [official website] or follow him on [Instagram].
            """)
            st.pyplot(plt.gcf())

        elif selected_artist == 'Kenny Chesney':
            image = Image.open('image/kenny_chesney.jpg')
            st.image(image, caption='Kenny Chesney')
            st.markdown("""
            ## About Kenny Chesney

            Kenny Chesney is an American country music singer, songwriter, and record producer. He is one of the most successful and award-winning country music artists of all time, with over 30 million albums sold worldwide. He has won nine Academy of Country Music Awards, six Country Music Association Awards, and four Billboard Music Awards.

            You can learn more about Kenny Chesney at his [official website] or follow him on [Facebook].
            """)
            st.pyplot(plt.gcf())

    elif selected_option == "Comparison":
        # Plot the graph for the top 5 artists
        st.header("Comparison")
        plt.figure(figsize=(10, 6))
        for artist in top_5_artists:
            artist_data = grouped[grouped['Artists'] == artist]
            plt.plot(artist_data['Year'], artist_data['Count'], label=artist)

        plt.xlabel('Year')
        plt.ylabel('Artist Count')
        plt.title('Artist Count Over the Years - Top 5 Artists (User Provided)')
        plt.legend()
        st.pyplot(plt.gcf())
elif selected_option == "About Us":
    st.markdown("""
    ## About Us

    This is the "About Us" page. You can learn more about our team, our mission, and our work here.
    """)
