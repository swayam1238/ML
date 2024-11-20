import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import requests

# Function to get video ID from YouTube URL
def get_video_id(url):
    if "youtube.com" in url:
        video_id = url.split("v=")[1].split("&")[0]
        return video_id
    return None

# Function to get transcript from YouTube video
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

# Function to translate transcript
def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Streamlit UI
st.title("AutoDubs - Automatic Video Dubbing")

# Get YouTube link and language input
video_url = st.text_input("Enter YouTube Video URL")
language = st.selectbox("Translate to", ["French", "Spanish", "German", "Italian", "Portuguese"])

if video_url:
    video_id = get_video_id(video_url)
    if video_id:
        transcript = get_transcript(video_id)
        if transcript:
            # Extract and combine all the text from the transcript
            transcript_text = " ".join([item['text'] for item in transcript])

            # Translate the transcript text
            translated_text = translate_text(transcript_text, language)

            st.write("### Translated Text")
            st.write(translated_text)

            # Optional: You can add audio dubbing functionality here (e.g., using text-to-speech libraries)
        else:
            st.error("No transcript available for this video.")
    else:
        st.error("Invalid YouTube URL.")