import streamlit as st
from st_pages import add_page_title
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

st.set_page_config(page_title="HOME", page_icon="🏠")

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
goto_page("🎶 Analysis of Songs", "analysis.py")


st.header("Analysis of Artists")
st.write("We offer a comprehensive artist discography and a platform for meaningful artist comparisons. Whether you're a music enthusiast or a professional, our platform provides valuable insights into your favorite artists' performance over the years. Our interactive graphs will take you through the years of their music careers. Additionally, our comparison tool lets you visualize their journey side by side, helping you identify trends and differences.")
st.write("Here are the top 5 artists in BillBoard Hot 100")
st.write(top_5_artists)
goto_page("🎤 Top Artists", "top_5.py")

st.header("Analysis of Genre")
st.write("We go beyond just exploring genres—we analyze their evolution and provide insights into the most popular genres over time. Our in-depth analysis tracks the growth and trends of each genre, allowing you to understand how musical landscapes have shifted and transformed throughout history.")
st.write("Here are the most popular genres")
st.write(top_5_genres)
goto_page("🎧 Genre Analysis", "analysisofgenre.py")

st.header("Prediction of Genre")
st.write("Prediction of genre uses, machine learning algorithms to predict what will be the trend of the genre over years. It gives you the option to visualize the prediction of Genre over Years by different Machine Learning Models and compare them with the actual data.")
st.write("Here are the R-squared scores of Pop Genre trained on different models")
st.write("Linear Regression:",linear_score)
st.write("Decision Tree:",dt_score)
st.write("Random Forest:",rf_score)
goto_page("🔍 Genre Prediction", "linear.py")