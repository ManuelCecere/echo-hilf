from pathlib import Path
import streamlit as st
import logging
import io
from audiorecorder import audiorecorder
from openai import OpenAI
import os


logging.basicConfig(level=logging.ERROR)
from dotenv import load_dotenv


load_dotenv("config/credentials.env")  # This loads the environment variables from .env
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_KEY"]

client = OpenAI()


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
            model="whisper-1", file=("placeholder.wav", audio_bytes)
        )
        return transcription.text
    except Exception as e:
        st.error(f"Failed to transcribe audio: {e}")
        return None


st.title("🎙️ Audio Recorder")

audio = audiorecorder("Click to record 🎤", "Click to stop recording ⏹️")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")
    with st.expander("Show Audio Properties 📊"):
        display_audio_properties(audio)

    with st.spinner("Transcribing audio..."):
        transcription = transcribe_audio(audio)
        if transcription:
            st.subheader("Transcription 📝")
            st.write(transcription)
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

    # Example Text-to-Speech section
    st.subheader("Text-to-Speech Sample 🔊")
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="Today is a wonderful day to build something people love!",
    )
    audio_content = response.content
    st.audio(audio_content, format="audio/mp3")

    st.info("Try recording something and see it transcribed!")

    # Other parts of your Streamlit app...

# Feedback Section
st.write("---")  # Draw a divider line
st.header("Was This Conversation Useful? 🤔")

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
