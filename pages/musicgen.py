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
        switch_page("🏠 Home")
st.write("Enter a prompt to generate music:")

prompt = st.text_input("Your music prompt", "")

if st.button("Generate"):
    with st.spinner("Generating music..."):
        def get_quota_information(base_url):
            url = f"{base_url}/api/get_limit"
            response = requests.get(url)
            data = response.json()
            return data if "credits_left" in data else {"credits_left": 0}
        # Replace your Vercel domain
        arr = [
            'https://suno-api3-three.vercel.app/',
            'https://suno-api2-bice.vercel.app/',
            'https://suno-api-plum.vercel.app/',
            'https://suno-api-gamma-snowy.vercel.app/'
            ]

        base_url = next((link for link in arr if get_quota_information(link)["credits_left"] > 0), None)

        if base_url is None:
            st.write("All APIs are out of quota.")
        #base_url='https://suno-api-gold.vercel.app/'
        

        # API helper functions (unchanged)
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


        def get_quota_information(base_url):
            url = f"{base_url}/api/get_limit"
            response = requests.get(url)
            return response.json()

        def generate_audio_from_prompt(prompt):
            data = generate_audio_by_prompt({
                "prompt": prompt,
                "make_instrumental": False,
                "wait_audio": False
            })

            ids = f"{data[0]['id']},{data[1]['id']}"
            print(f"ids: {ids}")

            for _ in range(60):
                data = get_audio_information(ids)
                if data[0]["status"] == 'streaming':
                    result = []
                    result.append(data[0]['audio_url'])
                    result.append(data[0]['lyric'])
                    result.append(data[0]['title'])
                    result.append(data[0]['image_url'])
                    return result
                time.sleep(5)

            return None
        # Generate audio logic
        result = generate_audio_from_prompt(prompt)
        try:
            col1, col2 = st.columns(2,gap="medium")
            with col1:
                st.markdown(f"<h1 style='text-align: center;'>{result[2]}</h1>", unsafe_allow_html=True)
                co1,co2,co3=st.columns([2,6,2])
                with co2:
                 st.image(result[3], caption=result[2])
            with col2:
                st.write("Lyrics :", result[1])
            link=result[0]
            st.audio(link, format='audio/mp3')
            
        except:
            st.write("Something went wront")