import streamlit as st
import requests
import time
from io import BytesIO
from streamlit_extras.switch_page_button import switch_page 

st.set_page_config(page_title="Generated Songs", page_icon="🎙️",initial_sidebar_state="collapsed")
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)

col1,col2=st.columns([8,1])
with col1:
    st.title("Generate Songs")
with col2:
    for _ in range(2):
        st.write(" ")
    if st.button("🏠"):
        switch_page("home page")
st.write("Enter a prompt to generate music:")

prompt = st.text_input("Your music prompt", "")

if st.button("Generate"):
    with st.spinner("Generating music..."):
        def get_quota_information(base_url):
            url = f"{base_url}/api/get_limit"
            response = requests.get(url)
            return response.json()

        arr = [
            'https://suno-apiiss.vercel.app',
            'https://suno-api-2-three.vercel.app/'
            #'https://suno-api-3.vercel.app/'
        ]

        base_url = None
        for link in arr:
            quota_info = get_quota_information(link)
            if quota_info["credits_left"] > 0:
                base_url = link
                break

        def custom_generate_audio(payload):
            url = f"{base_url}/api/custom_generate"
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
            return response.json()

        def generate_audio_by_prompt(payload):
            url = f"{base_url}/api/generate"
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
            return response.json()

        def get_audio_information(audio_ids):
            url = f"{base_url}/api/get?ids={audio_ids}"
            response = requests.get(url)
            return response.json()

        def generate_audio_link(id):
            base_url = "https://audiopipe.suno.ai/"
            link = f"{base_url}?item_id={id}"
            return link

        def generate_image_link(id):
            base_url = "https://cdn2.suno.ai/"
            link = f"{base_url}image_{id}.jpeg"
            return link

        def generate_audio_from_prompt(prompt):
            data = generate_audio_by_prompt({
                "prompt": prompt,
                "make_instrumental": False,
                "wait_audio": False
            })
            id = data[0]['id']
            time.sleep(10)
            audio_link = generate_audio_link(id)
            image_link = generate_image_link(id)
            lyrics_src = get_audio_information(id)
            title = lyrics_src[0]['title']
            lyric = lyrics_src[0]['lyric']
            return audio_link, image_link, title, lyric

        try:
            audio_link, image_link, title, lyric = generate_audio_from_prompt(prompt)
            
            # Title styling
            st.markdown("""
                <style>
                .song-title {
                    text-align: center;
                    font-size: 2.5rem;
                    font-weight: bold;
                    margin-bottom: 2rem;
                    color: white;
                }
                .lyrics-section {
                    font-size: 1.2rem;
                    color: white;
                    font-weight: bold;
                    margin-top: 1.5rem;
                    margin-bottom: 0.8rem;
                    text-align: center;  /* Center the section headers */
                }
                .lyrics-text {
                    color: white;
                    margin-bottom: 1.2rem;
                    line-height: 1.6;
                    text-align: center;  /* Center the lyrics */
                }
                .content-container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .image-container {
                    display: flex;
                    justify-content: center;
                    margin-bottom: 2rem;
                }
                .image-container img {
                    max-width: 400px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }
                .audio-container {
                    margin: 2rem 0;
                }
                .lyrics-title {
                    text-align: center;
                    color: white;
                    margin-bottom: 1.5rem;
                }
                </style>
            """, unsafe_allow_html=True)
        
            # Display title
            st.markdown(f'<div class="song-title">{title}</div>', unsafe_allow_html=True)
            
            # Display image
            st.markdown(f'''
                <div class="image-container">
                    <img src="{image_link}" alt="Song Cover">
                </div>
            ''', unsafe_allow_html=True)
            
            # Display audio
            st.markdown('<div class="audio-container">', unsafe_allow_html=True)
            st.audio(audio_link, format='audio/mp3')
            st.markdown('</div>', unsafe_allow_html=True)
            
            def format_lyrics(lyrics_text):
                formatted_lyrics = ""
                sections = lyrics_text.replace("[", "\n[").split("\n")
                for section in sections:
                    if section.strip():
                        if section.startswith("["):
                            section_name = section.strip("[]")
                            formatted_lyrics += f'<div class="lyrics-section">[{section_name}]</div>\n'
                        else:
                            formatted_lyrics += f'<div class="lyrics-text">{section}</div>\n'
                return formatted_lyrics
        
            # Display lyrics
            st.markdown('<div class="content-container">', unsafe_allow_html=True)
            st.markdown('<h2 class="lyrics-title">Lyrics</h2>', unsafe_allow_html=True)
            formatted_lyrics = format_lyrics(lyric)
            st.markdown(formatted_lyrics, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
