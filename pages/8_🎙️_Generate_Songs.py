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
            'https://suno-apiiss.vercel.app'
            # 'https://suno-api-whwo.vercel.app/',
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
            link = f"{base_url}image_{id}.png"
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
            col1, col2 = st.columns(2, gap="medium")
            with col1:
                st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
                co1,co2,co3=st.columns([2,6,2])
                with co2:
                    st.image(image_link)
            with col2:
                st.write("Lyrics:", lyric)
            st.audio(audio_link, format='audio/mp3')

        except Exception as e:
            st.write("Something went wrong:", e)
