import streamlit as st
from st_pages import add_page_title
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

st.set_page_config(page_title="HOME", page_icon="🏠")

import streamlit as st

import streamlit as st

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    body {{
        margin: 0;
        height: 100%;
    }}
    #retrobg {{
        position: relative;
        overflow: hidden;
        height: 100%;
        color: #a3c;
        background-color: #000;
    }}
    #retrobg-sky {{
        position: absolute;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        top: 0;
        width: 100%;
        height: 55%;
        background: linear-gradient( #214 75%, #249 );
    }}
    #retrobg-sunWrap {{
        position: relative;
        width: 40%;
        margin-bottom: -15%;
    }}
    #retrobg-sun {{
        --glow-color: #d44;
        padding-top: 100%;
        border-radius: 50%;
        background-image: linear-gradient( #fcdf11, #ff623f, #fe2085 50% );
        box-shadow: 0 0 160px 80px var( --glow-color );
        animation: 2s ease infinite alternate retrobg-sun-glow-anim;
    }}
    .retrobg-shutdown #retrobg-sun {{
        background-image: linear-gradient( #000, #000 40% );
        --glow-color: #000;
    }}
    @keyframes retrobg-sun-glow-anim {{
        from {{ box-shadow: 0 0 160px 80px var( --glow-color ); }}
        to   {{ box-shadow: 0 0 200px 95px var( --glow-color ); }}
    }}
    #retrobg-stars {{
        position: absolute;
        width: 100%;
        height: 100%;
    }}
    .retrobg-star {{
        position: absolute;
        border-radius: 50%;
        width: 2px;
        height: 2px;
        background-color: #fff;
    }}

    /* ............................................................... */
    #retrobg-mountains {{
        position: absolute;
        width: 100%;
        height: 30%;
    }}
    .retrobg-mountain {{
        position: absolute;
        width: 30%;
        height: 100%;
        background-image: linear-gradient( #000 70%, #111 85%, #fff1 );
    }}
    #retrobg-mountains-left {{ left: 0; clip-path: polygon( 0% 100%,0% 55%,5% 60%,10% 55%,20% 50%,25% 42%,30% 38%,33% 35%,40% 45%,50% 50%,60% 70%,70% 85%,75% 82%,80% 91%,85% 90%,90% 95%,95% 98%,100% 100% ); }}
    #retrobg-mountains-right {{ right: 0; clip-path: polygon( 0% 100%,5% 95%,10% 85%,15% 87%,20% 80%,25% 78%,30% 65%,40% 70%,50% 57%,60% 53%,67% 68%,70% 70%,75% 66%,80% 55%,90% 50%,95% 60%,100% 57%,100% 100% ); }}

    /* ............................................................... */
    #retrobg-cityWrap {{
        position: absolute;
        width: 50%;
        margin-left: -1%;
    }}
    #retrobg-city {{
        padding-top: 20%;
    }}
    .retrobg-building {{
        position: absolute;
        width: 5%;
        height: 100%;
        bottom: 0;
        border-radius: 4px 4px 0 0;
        background-image: linear-gradient( 0deg, rgba( 17, 17, 34, 0 ), #112 30px, #000 );
    }}
    .retrobg-building:nth-child( odd ) {{
        background-image: linear-gradient( 0deg, rgba( 24, 24, 42, 0 ), #223 30px, #000 );
    }}
    .retrobg-antenna::after {{
        content: "";
        position: absolute;
        left: 50%;
        margin-left: calc( -1px - 5% );
        bottom: 100%;
        width: 10%;
        min-width: 2px;
        height: 33%;
        background-color: #000;
    }}

    /* ............................................................... */
    #retrobg-ground {{
        position: absolute;
        overflow: hidden;
        width: 100%;
        height: 45%;
        bottom: 0;
        border-top: 2px solid #bf578c;
        background-color: #000;
    }}
    .retrobg-shutdown #retrobg-ground {{
        border-color: #000;
    }}
    #retrobg-groundShadow {{
        position: absolute;
        top: 0;
        width: 100%;
        height: 100%;
        background-image: linear-gradient( #000 0%, transparent );
    }}

    /* ............................................................... */
    #retrobg-linesWrap {{
        height: 100%;
        perspective: 1000px;
        perspective-origin: center top;
    }}
    #retrobg-lines {{
        position: absolute;
        width: 100%;
        height: 100%;
        transform-origin: top center;
        animation: .35s linear infinite retrobg-lines-anim;
    }}
    .retrobg-shutdown #retrobg-lines {{
        animation-duration: 5s;
    }}
    @keyframes retrobg-lines-anim {{
        from {{ transform: rotateX( 84deg ) translateY( 0 ); }}
        to {{ transform: rotateX( 84deg ) translateY( 100px ); }}
    }}
    #retrobg-hlines,
    #retrobg-vlines {{
        position: absolute;
        left: calc( ( 900% - 100% ) / -2 );
        width: 900%;
        height: 500%;
    }}
    #retrobg-vlines {{
        display: flex;
        justify-content: center;
    }}
    .retrobg-hline,
    .retrobg-vline {{
        width: 100%;
        height: 100%;
        background-color: currentColor;
    }}
    .retrobg-hline {{ height: 3px; }}
    .retrobg-vline {{ width: 3px; }}
    .retrobg-hline + .retrobg-hline {{ margin-top: 98px; }}
    .retrobg-vline + .retrobg-vline {{ margin-left: 98px; }}
</style>
<div id="retrobg">
    <div id="retrobg-sky">
        <div id="retrobg-sunWrap">
            <div id="retrobg-sun"></div>
        </div>
        <div id="retrobg-stars"></div>
    </div>
    <div id="retrobg-mountains">
        <div id="retrobg-mountains-left" class="retrobg-mountain"></div>
        <div id="retrobg-mountains-right" class="retrobg-mountain"></div>
    </div>
    <div id="retrobg-cityWrap">
        <div id="retrobg-city">
            <div class="retrobg-building retrobg-antenna"></div>
            <div class="retrobg-building retrobg-antenna"></div>
            <div class="retrobg-building retrobg-antenna"></div>
            <div class="retrobg-building retrobg-antenna"></div>
            <div class="retrobg-building retrobg-antenna"></div>
            <div class="retrobg-building retrobg-antenna"></div>
            <div class="retrobg-building"></div>
            <div class="retrobg-building"></div>
            <div class="retrobg-building"></div>
            <div class="retrobg-building"></div>
            <div class="retrobg-building"></div>
            <div class="retrobg-building"></div>
            <div class="retrobg-building"></div>
            <div class="retrobg-building"></div>
            <div class="retrobg-building"></div>
            <div class="retrobg-building"></div>
            <div class="retrobg-building"></div>
        </div>
    </div>
    <div id="retrobg-ground">
        <div id="retrobg-groundShadow"></div>
    </div>
    <div id="retrobg-linesWrap">
        <div id="retrobg-lines">
            <div id="retrobg-hlines">
                <div class="retrobg-hline"></div>
                <div class="retrobg-hline"></div>
                <div class="retrobg-hline"></div>
            </div>
            <div id="retrobg-vlines">
                <div class="retrobg-vline"></div>
                <div class="retrobg-vline"></div>
                <div class="retrobg-vline"></div>
            </div>
        </div>
    </div>
</div>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def goto_page(display_text, destination_page):
    if st.button(display_text):
        switch_page(destination_page)

# Load and preprocess the dataset
df = pd.read_csv("billboard.csv")
df['Week'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')
df['Genres'] = df['Genre'].str.split(',')

# Flatten the list of genres
genres_list = [genre for genres in df['Genres'] for genre in genres]

# Calculate the frequency of each genre
genre_counts = pd.Series(genres_list).value_counts()

# Get the genre with the highest frequency
top_genre = genre_counts.index[0]

# Filter the dataset for the top genre
top_genre_data = df[df['Genres'].apply(lambda x: top_genre in x)]

# Group and aggregate data at the weekly level for the top genre
grouped = top_genre_data.groupby('Week').size().reset_index(name='Count')

# Convert dates to numerical representation
ref_date = grouped['Week'].min()
grouped['Week_Num'] = (grouped['Week'] - ref_date).dt.days

# Split the data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(grouped['Week_Num'], grouped['Count'], test_size=0.2, random_state=0)

# Reshape the training and test data
x_train = x_train.values.reshape(-1, 1)
x_test = x_test.values.reshape(-1, 1)
y_train = y_train.values.reshape(-1, 1)
y_test = y_test.values.reshape(-1, 1)


# Linear Regression
linear_reg = LinearRegression()
linear_reg.fit(x_train, y_train)
linear_pred = linear_reg.predict(x_test)
linear_score = r2_score(y_test, linear_pred)




# Decision Tree Regression
dt_reg = DecisionTreeRegressor(random_state=0)
dt_reg.fit(x_train, y_train)
dt_pred = dt_reg.predict(x_test)
dt_score = r2_score(y_test, dt_pred)

# Random Forest Regression
rf_reg = RandomForestRegressor(random_state=0)
rf_reg.fit(x_train, y_train)
rf_pred = rf_reg.predict(x_test)
rf_score = r2_score(y_test, rf_pred)



# # Print the accuracy scores
# print("Linear Regression Accuracy: {:.2f}%".format(linear_score * 100))
# print("Decision Tree Regression Accuracy: {:.2f}%".format(dt_score * 100))
# print("Random Forest Regression Accuracy: {:.2f}%".format(rf_score * 100))

# Read the CSV file into a DataFrame
df1 = pd.read_csv('charts.csv')

# Group the data by the "artist" column and count the occurrences
artist_counts = df1['Artists'].value_counts()

# Retrieve the top 5 artists with the highest value count
top_5_artists = artist_counts.head(5)

df['Genres'] = df['Genre'].str.split(',')
df = df.explode('Genre')

# Flatten the list of genres
genres_list = [genre for genres in df['Genres'] for genre in genres]

# Calculate the frequency of each genre
genre_counts = pd.Series(genres_list).value_counts()

top_5_genres = genre_counts.head(5)

# Create a Streamlit app
st.title("Home")
st.write("Welcome to [Your Website Name], where the power of music comes alive through analysis, exploration, and prediction.")
st.header("Analysis of Songs")
st.write("We offer a comprehensive analysis of songs, going beyond just the surface level. Our detailed analysis dives into various aspects of songs, including danceability, acousticness, and more, providing you with a deeper understanding of the music you love. Discover the essence of each track and find similar songs to expand your musical horizons.")



st.header("Analysis of Artists")
st.write("We offer a comprehensive artist discography and a platform for meaningful artist comparisons. Whether you're a music enthusiast or a professional, our platform provides valuable insights into your favorite artists' performance over the years. Our interactive graphs will take you through the years of their music careers. Additionally, our comparison tool lets you visualize their journey side by side, helping you identify trends and differences.")
st.write("Here are the top 5 artists in BillBoard Hot 100")
st.write(top_5_artists)


st.header("Analysis of Genre")
st.write("We go beyond just exploring genres—we analyze their evolution and provide insights into the most popular genres over time. Our in-depth analysis tracks the growth and trends of each genre, allowing you to understand how musical landscapes have shifted and transformed throughout history.")
st.write("Here are the most popular genres")
st.write(top_5_genres)


st.header("Prediction of Genre")
st.write("Prediction of genre uses, machine learning algorithms to predict what will be the trend of the genre over years. It gives you the option to visualize the prediction of Genre over Years by different Machine Learning Models and compare them with the actual data.")
st.write("Here are the R-squared scores of Pop Genre trained on different models")
st.write("Linear Regression:",linear_score)
st.write("Decision Tree:",dt_score)
st.write("Random Forest:",rf_score)
