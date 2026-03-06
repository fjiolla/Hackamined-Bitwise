"""
Client utility to interface with the Groq API.
"""

from groq import AsyncGroq
from app.config import settings

# Initialize the Groq async client
async_client = AsyncGroq(api_key=settings.groq_api_key)

# Initialize the model as specified
MODEL_NAME = 'llama-3.3-70b-versatile'

async def call_llm(prompt: str) -> str:
    """
    Calls the Groq API asynchronously with the given prompt.
    
    Args:
        prompt: The text prompt describing the generation task.
        
    Returns:
        The text response from the model.
    """
    chat_completion = await async_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL_NAME,
    )
    
    return chat_completion.choices[0].message.content
