import streamlit as st
from gtts import gTTS
import tempfile

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts.save(tmpfile.name)
        return tmpfile.name

st.title("Text to Speech")
text = st.text_input("Enter Text")
lang = st.selectbox("Select Language", ['en', 'hi', 'ta', 'te', 'kn', 'ml', 'mr', 'bn', 'gu', 'pa'])

if st.button("Speak"):
    if text.strip():
        audio_file = text_to_speech(text, lang)
        st.audio(audio_file, format="audio/mp3")
    else:
        st.warning("Please enter some text to convert to speech.")
