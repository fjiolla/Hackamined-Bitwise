"""
Client utility to interface with the Google Gemini API.
"""

import google.generativeai as genai
from app.config import settings

# Configure the API key
genai.configure(api_key=settings.gemini_api_key)

# Initialize the model as specified (using the newest version supported by the api)
model = genai.GenerativeModel('gemini-2.5-flash')


def call_llm(prompt: str) -> str:
    """
    Calls the Gemini API with the given prompt.
    
    Args:
        prompt: The text prompt describing the generation task.
        
    Returns:
        The text response from the model.
    """
    response = model.generate_content(prompt)
    return response.text
