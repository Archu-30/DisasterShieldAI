import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm():
    """
    Returns the Groq LLM instance.
    Supports environment variables, .env, and Streamlit Cloud secrets.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass

    if api_key:
        api_key = str(api_key).strip().strip('"').strip("'")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing! Please configure GROQ_API_KEY in your Streamlit Cloud Secrets or .env file."
        )

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=api_key
    )