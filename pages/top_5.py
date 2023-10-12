import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

# Create tabs for each artist
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Taylor Swift", "Elton John", "Madonna", "Drake", "Kenny Chesney"])

# Load the artist data
df = pd.read_csv("charts.csv")

# Convert the 'Week' column to datetime format
df['Year'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')

# Calculate the frequency of each artist
artist_counts = df['Artists'].value_counts()

# Create a list of artists
artists = ["Taylor Swift", "Elton John", "Madonna", "Drake", "Kenny Chesney"]

# Display content in each tab
with tab1:
    if st.button("Taylor Swift"):
        selected_artist = 'Taylor Swift'
    # Create a placeholder for the chart
    chart_placeholder = st.empty()

    # Display Taylor Swift's image and about us section
    image = Image.open('image/taylor_swift.jpg')
    st.image(image, caption='Taylor Swift')
    st.markdown("""
        ## About Taylor Swift

        Taylor Swift is an American singer, songwriter, record producer, and actress. She is one of the most successful and influential artists of all time, with over 200 million records sold worldwide. She has won 11 Grammy Awards, 28 American Music Awards, 23 Billboard Music Awards, and seven Brit Awards.

        You can learn more about Taylor Swift at her [official website](https://taylorswift.com/) or follow her on [Facebook](https://www.facebook.com/taylorswift).
    """)

    # Plot the line chart for the selected artist
    plt.figure(figsize=(10, 6))
    artist_data = df[df['Artists'] == selected_artist]
    plt.plot(artist_data['Year'], artist_data['Count'], label=selected_artist)

    plt.xlabel('Year')
    plt.ylabel('Artist Count')
    plt.title('Artist Count Over the Years - ' + selected_artist + ' (User Provided)')
    plt.legend()

    # Display the line chart
    chart_placeholder.pyplot(plt.gcf())

with tab2:
    if st.button("Elton John"):
        selected_artist = 'Elton John'
    # Create a placeholder for the chart
    chart_placeholder = st.empty()

    # Display Elton John's image and about us section
    image = Image.open('image/elton_john.jpg')
    st.image(image, caption='Elton John')
    st.markdown("""
        ## About Elton John

        Elton John is a British singer, songwriter, pianist, and composer. He is one of the most acclaimed and best-selling music artists of all time, with over 300 million records sold worldwide. He has won five Grammy Awards, an Academy Award, a Golden Globe Award, a Tony Award, and a Disney Legends Award.

        You can learn more about Elton John at his [official website](https://www.eltonjohn.com/) or follow him on [Instagram](https://www.instagram.com/eltonjohn/).
    """)

    # Plot the line chart for the selected artist
    plt.figure(figsize=(10, 6))
    artist_data = df[df['Artists'] == selected_artist]
    plt.plot(artist_data['Year'], artist_data['Count'], label=selected_artist)

    plt.xlabel('Year')
    plt.ylabel('Artist Count')
    plt.title('Artist Count Over the Years - ' + selected_artist + ' (User Provided)')
    plt.legend()

    # Display the line chart
    chart_placeholder.pyplot(plt.gcf())

# Continue with similar "with" blocks for Madonna, Drake, and Kenny Chesney

with tab3:
    if st.button("Madonna"):
        selected_artist = 'Madonna'
    # Create a placeholder for the chart
    chart_placeholder = st.empty()

    # Display Madonna's image and about us section
    image = Image.open('image/madonna.jpg')
    st.image(image, caption='Madonna')
    st.markdown("""
        ## About Madonna

        Madonna is an American singer, songwriter, actress, and businesswoman. She is known as the "Queen of Pop" and one of the most influential figures in popular culture. She has sold over 300 million records worldwide, making her the best-selling female music artist of all time. She has won seven Grammy Awards, two Golden Globe Awards, and a Billboard Woman of the Year Award.

        You can learn more about Madonna at her [official website](https://www.madonna.com/) or follow her on [Twitter](https://twitter.com/Madonna/).
    """)

    # Plot the line chart for the selected artist
    plt.figure(figsize=(10, 6))
    artist_data = df[df['Artists'] == selected_artist]
    plt.plot(artist_data['Year'], artist_data['Count'], label=selected_artist)

    plt.xlabel('Year')
    plt.ylabel('Artist Count')
    plt.title('Artist Count Over the Years - ' + selected_artist + ' (User Provided)')
    plt.legend()

    # Display the line chart
    chart_placeholder.pyplot(plt.gcf())

with tab4:
    if st.button("Drake"):
        selected_artist = 'Drake'
    # Create a placeholder for the chart
    chart_placeholder = st.empty()

    # Display Drake's image and about us section
    image = Image.open('image/drake.jpg')
    st.image(image, caption='Drake')
    st.markdown("""
        ## About Drake

        Drake is a Canadian rapper, singer, songwriter, actor, and entrepreneur. He is one of the most popular and influential artists of his generation, with over 170 million records sold worldwide. He has won four Grammy Awards, six American Music Awards, 27 Billboard Music Awards, and two Brit Awards.

        You can learn more about Drake at his [official website](https://www.drakeofficial.com/) or follow him on [Instagram](https://www.instagram.com/champagnepapi/).
    """)

    # Plot the line chart for the selected artist
    plt.figure(figsize=(10, 6))
    artist_data = df[df['Artists'] == selected_artist]
    plt.plot(artist_data['Year'], artist_data['Count'], label=selected_artist)

    plt.xlabel('Year')
    plt.ylabel('Artist Count')
    plt.title('Artist Count Over the Years - ' + selected_artist + ' (User Provided)')
    plt.legend()

    # Display the line chart
    chart_placeholder.pyplot(plt.gcf())

with tab5:
    if st.button("Kenny Chesney"):
        selected_artist = 'Kenny Chesney'
    # Create a placeholder for the chart
    chart_placeholder = st.empty()

    # Display Kenny Chesney's image and about us section
    image = Image.open('image/kenny_chesney.jpg')
    st.image(image, caption='Kenny Chesney')
    st.markdown("""
        ## About Kenny Chesney

        Kenny Chesney is an American country music singer, songwriter, and record producer. He is one of the most successful and award-winning country music artists of all time, with over 30 million albums sold worldwide. He has won nine Academy of Country Music Awards, six Country Music Association Awards, and four Billboard Music Awards.

        You can learn more about Kenny Chesney at his [official website](https://www.kennychesney.com/) or follow him on [Facebook](https://www.facebook.com/kennychesney/).
    """)

    # Plot the line chart for the selected artist
    plt.figure(figsize=(10, 6))
    artist_data = df[df['Artists'] == selected_artist]
    plt.plot(artist_data['Year'], artist_data['Count'], label=selected_artist)

    plt.xlabel('Year')
    plt.ylabel('Artist Count')
    plt.title('Artist Count Over the Years - ' + selected_artist + ' (User Provided)')
    plt.legend()

    # Display the line chart
    chart_placeholder.pyplot(plt.gcf())

