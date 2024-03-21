from pathlib import Path
import streamlit as st
import logging
import io
from audiorecorder import audiorecorder
from openai import OpenAI
import os
import requests
import json
import time


logging.basicConfig(level=logging.ERROR)
from dotenv import load_dotenv


load_dotenv("config/credentials.env")  # This loads the environment variables from .env

client = OpenAI()


# Initialize session state variables if they don't exist
if 'transcription_done' not in st.session_state:
    st.session_state.transcription_done = False
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False


def display_audio_properties(audio):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Frame Rate", f"{audio.frame_rate} Hz")
    with col2:
        st.metric("Frame Width", f"{audio.frame_width} bytes")
    with col3:
        st.metric("Duration", f"{audio.duration_seconds} seconds")


def transcribe_audio(audio):
    audio_bytes = io.BytesIO()
    audio.export(audio_bytes, format="wav")
    audio_bytes.seek(0)
    try:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=("placeholder.wav", audio_bytes), prompt= "Hoi und schön dich z'treffe, ich ha e Frag für dich, bitte antwort mir in miner Sproch.",
        )
        return transcription.text
    except Exception as e:
        st.error(f"Failed to transcribe audio: {e}")
        return None
    
def process_transcription(transcription):
    start_time = time.time()
    url = 'http://127.0.0.1:8000/api/generate'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "user_id": "testing",
        "conversation_id": "testing",
        "question": transcription
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    st.session_state.processing_done = True

    if response.status_code == 200:
        end_time = time.time()
        print("time for process_transcription: ", start_time-end_time)
        return response.json()
    else:
        st.error("Failed to process transcription through the API.")
    
def display_message(user_message, is_user=True):
    # Define the user and bot message styles with escaped curly braces
    user_message_style = """
    <style>
        div.stTextInput>div>div>div>input {{
            border-width: 1px;
            border-radius: 20px;
            border-color: gray;
        }}
        .message {{
            position: relative;
            margin: 10px;
            padding: 10px;
            background-color: #007bff; /* Blue background for user */
            color: white;
            border-radius: 25px;
            width: fit-content;
            max-width: 60%;
            float: left; /* Align user messages to the left */
        }}
        .bot {{
            position: relative;
            margin: 10px;
            padding: 10px;
            background-color: #ff9999; /* Light red background for bot, change as needed */
            color: white;
            border-radius: 25px;
            width: fit-content;
            max-width: 60%;
            float: right; /* Align bot messages to the right */
        }}
        /* Clear floats after the messages */
        .clearfix {{
            content: "";
            clear: both;
            display: table;
        }}
    </style>
    <div class="message {style}" >{message}</div>
    <div class="clearfix"></div> <!-- Use clearfix to deal with the float property -->
    """
    
    # Choose the style based on the message sender
    if is_user:
        style = ""
    else:
        style = "bot"
    
    # Display the message
    st.markdown(user_message_style.format(message=user_message, style=style), unsafe_allow_html=True)

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



st.title("🎙️ Audio Recorder")
st.subheader("Try recording something and see it transcribed!")


audio = audiorecorder("Click to record 🎤", "Click to stop recording ⏹️")

if len(audio) > 0 and not st.session_state.transcription_done:
    
    st.audio(audio.export().read(), format="audio/wav")
    
    # with st.expander("Show Audio Properties 📊"):
    #     display_audio_properties(audio)

    with st.spinner("Transcribing and answering..."):
        transcription = transcribe_audio(audio)
        if transcription:
            st.session_state.transcription_done = True
            
            #st.subheader("Transcription 📝")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant designed to output JSON, with key 'output' and values "
                                   "only 'yes' or 'no'",
                    },
                    {
                        "role": "user",
                        "content": f"Does this sentence transmit anger? {transcription}",
                    },
                ],
            )
            if "yes" in response.choices[0].message.content.lower():
                st.markdown(
                    """
                    <div style="color: white; background-color: red; border-radius: 8px; padding: 10px; text-align: center;">
                        <strong>Anger Detected!</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            display_message(transcription)
            answer = process_transcription(transcription)
            display_message(answer, is_user=False)
            

    # Example Text-to-Speech section
    #st.subheader("Text-to-Speech Sample 🔊")
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=f"{answer}",
    )
    audio_content = response.content
    st.audio(audio_content, format="audio/mp3")

    gather_feedback()


