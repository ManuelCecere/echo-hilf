# EchoHilf

## Voice Bot Project

## Introduction

This repository hosts the code for a voice-activated customer service bot developed during the 36-hour StartHack hackathon in St.Gallen. It is designed to assist users in navigating the canton of St.Gallen's website through voice commands. The bot utilizes Streamlit for user interaction, FastAPI for backend processes, and leverages OpenAI's API for converting speech to text and vice versa. To answer user queries, it combines Retrieval-Augmented Generation (RAG) with GPT-4 for generating relevant and accurate responses. The RAG process involves creating embeddings using the Cohere API from HTML website content and employing Chroma for vector database management.
For more info on the challenge [here the presentation link.](https://www.canva.com/design/DAGAK87nvNg/QTXV33sKVcL7yYzjJrZ7yw/view?utm_content=DAGAK87nvNg&utm_campaign=designshare&utm_medium=link&utm_source=editor)

## Features

- **Speech Recognition**: Convert user speech to text using OpenAI's robust API.
- **Natural Language Understanding**: Leverage RAG and GPT-4 models to understand the context and generate accurate responses.
- **Text-to-Speech**: Convert the bot's text responses back into speech, providing a seamless conversational experience.
- **Streamlit Frontend**: An intuitive and user-friendly interface for interacting with the voice bot.
- **FastAPI Backend**: Efficient and scalable backend architecture to handle requests and processing.

## Installation

Before installing, ensure you have Python 3.8+ installed on your system. Follow these steps to set up the project environment:

1. Clone the repository:

```
git clone https://github.com/yourusername/voice-bot-project.git
cd voice-bot-project
```

2. Install the required Python packages:
```
pip install -r requirements.txt
```
3. Set up environment variables for OpenAI API credentials:
```
export OPENAI_API_KEY='your_openai_api_key_here
```
To run the voice bot, you need to start both the Streamlit frontend and FastAPI backend servers.

4. Starting the Backend Server:
navigate to the project directory and run:
```
uvicorn app:app --reload
```
This command starts the FastAPI server. Ensure it is running before launching the Streamlit app.

5. Launching the Streamlit App
In a new terminal window, start the Streamlit frontend by running:
```
streamlit run frontend/app.py
```
The Streamlit app should now be accessible in your web browser at http://localhost:8501.
