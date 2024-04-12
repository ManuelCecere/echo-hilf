# EchoHilf

## Voice Bot Project

## Introduction

This repository contains the code for a voice-activated bot designed to answer questions in natural language. The project uses Streamlit for an interactive frontend, FastAPI for managing backend operations, and integrates OpenAI's API for both speech-to-text and text-to-speech functionalities. Questions asked by the user are answered using a combination of RAG (Retrieval-Augmented Generation) for retrieving relevant information, and GPT-4 for generating coherent and contextually appropriate responses.

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

4. Starting the Backend Server
Navigate to the project directory and run:
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
