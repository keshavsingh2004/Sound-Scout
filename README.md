# Sound Scout

[![Open in Streamlit][share_badge]][share_link]

[share_badge]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[share_link]: https://sound-scout.streamlit.app

Welcome to Sound Scout on GitHub! This repository is dedicated to the exploration, analysis, and prediction of music. We provide a platform for in-depth analysis of songs, artists, genres, and even predictions of genre trends over the years. This readme file serves as a guide to help you navigate through our project.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

### Analysis of Songs

Sound Scout offers a comprehensive analysis of songs, delving into various aspects such as danceability, acousticness, and more. This feature provides a deeper understanding of the music you love and helps you discover similar songs.

### Analysis of Artists

Explore artists' discographies and compare them. This feature provides insights into artists' performances over time, using data from Spotify and Wikipedia.

### Analysis of Genre

Analyze the distribution and trends of music genres over time. This feature includes visualizations like pie charts and bar graphs to help you understand genre trends.

### Playlist Analysis

Analyze Spotify playlists to gain insights into song features and clustering. This feature includes audio feature correlations and song clustering visualizations.

### Melody Chat

Interact with music data through a chat interface. This feature allows you to input Spotify playlist or track links and fetches data for interaction.

### Generate Songs

Generate music based on text prompts. This feature displays generated music and associated lyrics.

### Soundify

Convert text from PDFs into audio conversations. This feature extracts text from PDFs, generates dialogues using AI models, and converts them into audio.

## Configuration

### Secrets Configuration

To configure your secrets, you need to rename the `secrets-example.toml` file to `secrets.toml` and fill in the necessary API keys and credentials. This file is used to securely store sensitive information such as API keys and access tokens.

1. Rename the file:

   ```bash
   mv .streamlit/secrets-example.toml .streamlit/secrets.toml
   ```

2. Open `secrets.toml` and fill in your credentials:
   ```toml
   google_API_KEY="your_google_api_key"
   GEMINI_MODEL_NAME="gemini-1.5-flash"
   SPOTIPY_CLIENT_ID="your_spotify_client_id"
   SPOTIPY_CLIENT_SECRET="your_spotify_client_secret"
   SAMBA_NOVA_API_KEY="your_samba_nova_api_key"
   SAMBANOVA_API_KEY_2="your_sambanova_api_key_2"
   AWS_ACCESS_KEY_ID="your_aws_access_key_id"
   AWS_SECRET_ACCESS_KEY="your_aws_secret_access_key"
   ```

### Docker Compose Setup

To run the application using Docker Compose, follow these steps:

1. Ensure you have Docker installed on your machine.

2. Build and run the application using Docker Compose:

   ```bash
   docker-compose up --build
   ```

This will start the Sound Scout application in a Docker container, making it accessible at `http://localhost:8501`.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/keshavsingh2004/Sound-Scout.git
   cd sound-scout
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run 0_🏠_Home_Page.py
   ```

## Usage

- Navigate through the different pages using the buttons on the home page.
- Use the analysis features to explore songs, artists, genres, and playlists.
- Generate music or convert text to audio using the respective features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
