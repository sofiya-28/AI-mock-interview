
import os
import io
import streamlit as st
from audiorecorder import audiorecorder
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def audio_recording(key=None):
    return audiorecorder(
        "Click to record",
        "Recording...",
        key=key
    )


def transcribe_audio(audio):
    if audio is None or len(audio) == 0:
        return None

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        st.error("GROQ_API_KEY missing in .env file.")
        return None

    try:
        buffer = io.BytesIO()
        audio.export(buffer, format="wav")
        audio_bytes = buffer.getvalue()

        st.write(
            f"Audio duration: {len(audio) / 1000:.2f} seconds"
        )
        st.write(f"Audio size: {len(audio_bytes)} bytes")

        client = Groq(api_key=api_key)

        response = client.audio.transcriptions.create(
            file=("recording.wav", audio_bytes),
            model="whisper-large-v3",
            response_format="json",
            temperature=0.0,
        )

        transcript = response.text.strip()

        if not transcript:
            st.warning("No speech detected. Please record again.")
            return None

        return transcript

    except Exception as error:
        st.error(f"Transcription error: {error}")
        return None
