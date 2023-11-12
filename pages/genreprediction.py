import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
st.set_page_config(page_title="Genre Prediction", page_icon="🔍")

with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)
# Load and preprocess the dataset
st.markdown("""
  ## Prediction of Genre
  
  Below is the prediction of the Genres of Music featured in BillBoard during in the future:
  
  """)
df = pd.read_csv("billboard.csv")
df['Week'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')
df['Genres'] = df['Genre'].str.split(',')
df = df.explode('Genre')

# Flatten the list of genres
genres_list = [genre for genres in df['Genres'] for genre in genres]

# Calculate the frequency of each genre
genre_counts = pd.Series(genres_list).value_counts()

# Get the genre with the highest frequency
selected_genre = st.selectbox("Select a genre:", genre_counts.index)

# Filter the dataset for the top genre
top_genre_data = df[df['Genres'].apply(lambda x: selected_genre in x)]

# Group and aggregate data at the weekly level for the top genre
grouped = top_genre_data.groupby('Week').size().reset_index(name='Count')

# Convert the Week column to a numeric column
ref_date = grouped['Week'].min()
grouped['Week_Num'] = (grouped['Week'] - ref_date).dt.days

# Split the data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(grouped['Week_Num'], grouped['Count'], test_size=0.2, random_state=0)
x_train = x_train.values.reshape(-1, 1)
x_test = x_test.values.reshape(-1, 1)
y_train = y_train.values.reshape(-1, 1)
y_test = y_test.values.reshape(-1, 1)

# Create a dictionary of models
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=0),
    "Random Forest": RandomForestRegressor(random_state=0)
}

# Create a dropdown menu to select the model
model_selection = st.selectbox("Select Model:", models.keys())

# Train the selected model
selected_model = models[model_selection]
selected_model.fit(x_train, y_train)

# Make predictions on the test set
test_pred = selected_model.predict(x_test)

# Calculate the R-squared score
test_score = r2_score(y_test, test_pred)

# Make predictions for all data points
predicted_values = selected_model.predict(grouped['Week_Num'].values.reshape(-1, 1)).reshape(-1)

# Create a DataFrame for plotting
plot_data = pd.DataFrame({'Year': grouped['Week'], 'Actual': grouped['Count'], 'Predicted': predicted_values})

# Create the plotly figure
fig = px.line(plot_data, x='Year', y=['Actual', 'Predicted'], labels={'value': 'Count'})

# Display the plotly figure
st.plotly_chart(fig)

# Display the R-squared score
st.write("R-squared score:", test_score)
