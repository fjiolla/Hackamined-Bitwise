"""
Configuration settings for the EpisodeIQ application.
Handles reading environment variables.
"""
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    """
    Application settings. 
    Can be expanded in the future to load from environment variables / .env files.
    """
    app_name: str = "EpisodeIQ"
    environment: str = "development"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
