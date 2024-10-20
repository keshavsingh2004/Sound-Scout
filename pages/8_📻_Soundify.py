import streamlit as st
import PyPDF2
import os
import openai
import nltk
from nltk.tokenize import word_tokenize
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
import boto3

st.set_page_config(page_title="Soundify", page_icon="📻",initial_sidebar_state="collapsed")
with open("designing.css") as source_des:
    st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)

# Download NLTK tokenizer data if not already present
nltk.download('punkt_tab')

# Function to extract text from uploaded PDF file
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""  # Ensure empty pages don't cause issues
    return text

# Function to interact with SambaNova AI for generating conversation
def get_conversation_from_sambanova(text):
    client = openai.OpenAI(
        api_key=st.secrets["SAMBANOVA_API_KEY_2"],
        base_url="https://api.sambanova.ai/v1",
    )

    response = client.chat.completions.create(
        model='Meta-Llama-3.1-70B-Instruct',
        messages=[
            {
                "role": "system",
                "content": """Create a natural dialogue between Person A and Person B that conveys the following text as a conversation. Follow these guidelines:
    
    - Each speaker should have a distinct personality and speaking style
    - Responses should be 2-3 sentences long (30-50 words)
    - Use natural transitions and reactions between speakers
    - Include appropriate emotional responses and conversational markers (e.g., "hmm", "I see", "that's interesting")
    - Maintain the key information and logical flow of the original text
    - Add relevant follow-up questions and clarifications where appropriate
    - Use everyday language unless technical terms are essential
    
    The conversation should feel like two friends or colleagues having an engaging discussion, not a formal exchange."""
            },
            {"role": "user", "content": text},
            {
                "role": "system",
                "content": "Ensure the dialogue maintains factual accuracy while being engaging and conversational."
            }
        ],
        temperature=0.7,  # Lowered for more consistent output
        top_p=0.9,        # Slightly reduced for better focus
        max_tokens=1500,  # Increased to allow for longer conversations
        presence_penalty=0.6,  # Added to encourage diverse responses
        frequency_penalty=0.3  # Added to reduce repetitive language
    )

    return response.choices[0].message.content

# Function to tokenize each turn of the conversation
def tokenize_conversation(conversation):
    conversation_turns = conversation.split("\n")
    tokenized_conversation = []
    
    for turn in conversation_turns:
        if turn.strip():  # Avoid empty lines
            tokens = word_tokenize(turn)
            tokenized_conversation.append(tokens)
    
    return tokenized_conversation

# Amazon Polly text-to-speech function
def polly_text_to_speech(text, voice_id='Joanna'):
    session = boto3.Session(
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        region_name='us-east-1'  # Change as necessary
    )
    polly = session.client('polly')
    
    try:
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine='neural'  # Explicitly specify the neural engine
        )
        
        if 'AudioStream' in response:
            audio_stream = response['AudioStream'].read()
            audio_segment = AudioSegment.from_mp3(BytesIO(audio_stream))
            return audio_segment
        else:
            st.error("Could not synthesize speech using Amazon Polly.")
            return None
    except Exception as e:
        st.error(f"Error in text-to-speech conversion: {str(e)}")
        return None

# Streamlit app setup
st.title("Soundify")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # Extract text from the uploaded PDF
    pdf_text = extract_text_from_pdf(uploaded_file)

    # Generate the conversation using SambaNova model
    conversation = get_conversation_from_sambanova(pdf_text)

    # Tokenize the conversation
    tokenized_conversation = tokenize_conversation(conversation)

    # Display the original conversation
    st.subheader("Original Podcast-style Conversation")
    st.text(conversation)

    # Generate audio for each conversation turn and merge them
    audio_segments = []

    for idx, turn in enumerate(tokenized_conversation):
        turn_text = " ".join(turn)

        # Clean turn text, skip the first 9 characters
        clean_turn_text = turn_text.replace('*', '').strip()[10:]  # Skip first 9 characters
        if not clean_turn_text:  # Skip empty turns
            continue

        # Skip the first line
        if idx == 0:
            continue

        # Generate audio based on speaker's text without speaker name
        if idx % 2 == 0:  # For "Man"
            audio_segment = polly_text_to_speech(clean_turn_text, voice_id='Matthew')
        else:  # For "Lady"
            audio_segment = polly_text_to_speech(clean_turn_text, voice_id='Ruth')

        if audio_segment:
            audio_segments.append(audio_segment)

    # Merge all audio segments into a single audio file
    if audio_segments:  # Check if there are any audio segments to merge
        combined_audio = AudioSegment.silent(duration=0)  # Start with silence to combine audio
        for segment in audio_segments:
            combined_audio += segment  # Append each audio segment
        combined_audio_file = BytesIO()
        combined_audio.export(combined_audio_file, format='mp3')
        combined_audio_file.seek(0)

        # Show the combined audio
        st.subheader("Combined Audio Conversation")
        st.audio(combined_audio_file)
