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

# Define a dictionary to map tab names to artist names
artist_mapping = {
    "Taylor Swift": "Taylor Swift",
    "Elton John": "Elton John",
    "Madonna": "Madonna",
    "Drake": "Drake",
    "Kenny Chesney": "Kenny Chesney"
}

# Display content in each tab
for tab in [tab1, tab2, tab3, tab4, tab5]:
    artist_name = artist_mapping[tab.label]
    
    with tab:
        # Create a placeholder for the chart
        chart_placeholder = st.empty()

        # Display artist's image and about us section
        image = Image.open(f'image/{artist_name.lower().replace(" ", "_")}.jpg')
        st.image(image, caption=artist_name)
        
        artist_info = {
            "Taylor Swift": """
                ## About Taylor Swift

                Taylor Swift is an American singer, songwriter, record producer, and actress. She is one of the most successful and influential artists of all time, with over 200 million records sold worldwide. She has won 11 Grammy Awards, 28 American Music Awards, 23 Billboard Music Awards, and seven Brit Awards.

                You can learn more about Taylor Swift at her [official website](https://taylorswift.com/) or follow her on [Facebook](https://www.facebook.com/taylorswift).
            """,
            "Elton John": """
                ## About Elton John

                Elton John is a British singer, songwriter, pianist, and composer. He is one of the most acclaimed and best-selling music artists of all time, with over 300 million records sold worldwide. He has won five Grammy Awards, an Academy Award, a Golden Globe Award, a Tony Award, and a Disney Legends Award.

                You can learn more about Elton John at his [official website](https://www.eltonjohn.com/) or follow him on [Instagram](https://www.instagram.com/eltonjohn/).
            """,
            "Madonna": """
                ## About Madonna

                Madonna is an American singer, songwriter, actress, and businesswoman. She is known as the "Queen of Pop" and one of the most influential figures in popular culture. She has sold over 300 million records worldwide, making her the best-selling female music artist of all time. She has won seven Grammy Awards, two Golden Globe Awards, and a Billboard Woman of the Year Award.

                You can learn more about Madonna at her [official website](https://www.madonna.com/) or follow her on [Twitter](https://twitter.com/Madonna/).
            """,
            "Drake": """
                ## About Drake

                Drake is a Canadian rapper, singer, songwriter, actor, and entrepreneur. He is one of the most popular and influential artists of his generation, with over 170 million records sold worldwide. He has won four Grammy Awards, six American Music Awards, 27 Billboard Music Awards, and two Brit Awards.

                You can learn more about Drake at his [official website](https://www.drakeofficial.com/) or follow him on [Instagram](https://www.instagram.com/champagnepapi/).
            """,
            "Kenny Chesney": """
                ## About Kenny Chesney

                Kenny Chesney is an American country music singer, songwriter, and record producer. He is one of the most successful and award-winning country music artists of all time, with over 30 million albums sold worldwide. He has won nine Academy of Country Music Awards, six Country Music Association Awards, and four Billboard Music Awards.

                You can learn more about Kenny Chesney at his [official website](https://www.kennychesney.com/) or follow him on [Facebook](https://www.facebook.com/kennychesney/).
            """
        }
        st.markdown(artist_info[artist_name])

        # Plot the line chart for the selected artist
        plt.figure(figsize=(10, 6))
        artist_data = df[df['Artists'] == artist_name]
        plt.plot(artist_data['Year'], artist_data['Count'], label=artist_name)

        plt.xlabel('Year')
        plt.ylabel('Artist Count')
        plt.title(f'Artist Count Over the Years - {artist_name} (User Provided)')
        plt.legend()

        # Display the line chart
        chart_placeholder.pyplot(plt.gcf())
