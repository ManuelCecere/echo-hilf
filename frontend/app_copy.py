from st_audiorec import st_audiorec
from pathlib import Path
import streamlit as st
import logging
import io
import requests
import json
import time
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.ERROR)
load_dotenv("config/credentials.env")  # This loads the environment variables from .env

# Assuming a hypothetical OpenAI class based on your setup for simplified API calls
class OpenAI:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    @st.cache_resource(allow_output_mutation=True, show_spinner=False)  # Caching response to improve speed
    def audio_transcriptions_create(self, audio_bytes):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        response = requests.post("https://api.openai.com/v1/audio-transcriptions", headers=headers, files=files)
        return response.json()

    @st.cache_resource(allow_output_mutation=True, show_spinner=False)  # Caching response to improve speed
    def audio_speech_create(self, text):
        data = {"text": text}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post("https://api.openai.com/v1/audio-speech", headers=headers, json=data)
        return response.content

client = OpenAI()

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

def display_message(user_message, is_user=True):
    if is_user:
        st.text_area("You:", value=user_message, height=100, disabled=True)
    else:
        st.text_area("Chatbot:", value=user_message, height=100, disabled=True)


def gather_feedback():
    # Feedback Section
    st.write("---")  # Draw a divider line
    st.subheader("Was This Conversation Useful? 🤔")

    # Define the feedback options
    feedback_options = ["Yes, it was helpful!", "Somewhat helpful", "No, not really"]
    # Use st.radio for feedback selection
    user_feedback = st.radio("Please let us know:", feedback_options)

    # Submit button for feedback
    if st.button("Submit Feedback"):
        if user_feedback == "Yes, it was helpful!":
            st.success("Great to hear that! Thank you for your feedback! 😊")
        elif user_feedback == "Somewhat helpful":
            st.info("Thanks for your feedback! We'll work on making it more helpful. 🛠")
        else:  # 'No, not really'
            st.error("Sorry to hear that. We appreciate your feedback and will improve. 🙏")

        # Additional instructions or actions based on feedback can be added here
        # For example, asking for detailed feedback, redirecting to a help page, etc.

st.title("Canton St. Gallen Chatbot")
st.subheader("Talk to me, and I'll assist you with your questions!")

audio_recorded = st_audiorec()

if audio_recorded is not None:
    audio_bytes = io.BytesIO(audio_recorded)
    with st.spinner('Transcribing your message...'):
        transcription_result = client.audio_transcriptions_create(audio_bytes.getvalue())
    transcription = transcription_result.get('transcription', 'Sorry, I could not understand that.')
    display_message(transcription, is_user=True)
    st.session_state['conversation_history'].append({"role": "user", "content": transcription})
    
    # Simulate processing transcription with your backend here
    # Example: processed_response = process_transcription(transcription)
    processed_response = "This is an example response."
    
    with st.spinner('Generating response...'):
        audio_response = client.audio_speech_create(processed_response)
    if audio_response:
        display_message(processed_response, is_user=False)
        st.session_state['conversation_history'].append({"role": "bot", "content": processed_response})
        st.audio(audio_response, format="audio/mp3")

# Example of improving user feedback and interaction
st.write("---")
gather_feedback()  # Assuming this function is defined as in your original code
st.write("Record another message to continue the conversation.")
