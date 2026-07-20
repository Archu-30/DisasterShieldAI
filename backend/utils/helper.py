import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
# Load environment variables
load_dotenv()
def get_llm():
    """
    Returns the Groq LLM instance.
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )
    return llm