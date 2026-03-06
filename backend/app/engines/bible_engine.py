"""
Engine for generating series bibles from story ideas.
"""

import json
from typing import Dict, Any

from app.models.story_models import StoryIdea, SeriesBible
from app.utils.groq_client import call_llm


class SeriesBibleGenerator:
    """
    Engine to convert a StoryIdea into a structured SeriesBible.
    """
    
    def generate_series_bible(self, story: StoryIdea) -> SeriesBible:
        """
        Generates a SeriesBible given a StoryIdea.
        
        Args:
            story: The basic story idea containing title, description, and genre.
            
        Returns:
            A SeriesBible object representing the persistent narrative memory.
        """
        # 1. Build a prompt string describing the story idea
        prompt = (
            f"Please generate a series bible for the following story idea.\n"
            f"Return ONLY valid JSON with no extra text or markdown codeblocks or explanation.\n"
            f"The JSON should contain precisely these string keys: 'archetype', 'protagonist', 'supporting_characters' (a list of strings), and 'central_conflict'.\n"
            f"Title: {story.title}\n"
            f"Genre: {story.genre}\n"
            f"Description: {story.description}\n"
        )
        
        # 2. Send prompt to an LLM helper function
        response_text = call_llm(prompt).strip()
        
        # Parse the structured JSON output
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()
            
        try:
            response_data = json.loads(response_text)
        except json.JSONDecodeError:
            response_data = {}
        
        # 4. Convert it into a SeriesBible object
        series_bible = SeriesBible(
            archetype=response_data.get("archetype", ""),
            protagonist=response_data.get("protagonist", ""),
            supporting_characters=response_data.get("supporting_characters", []),
            central_conflict=response_data.get("central_conflict", "")
        )
        
        return series_bible

    def suggest_episode_count(self, story: StoryIdea) -> int:
        """
        Suggests an optimal number of episodes based on the story idea complexity.
        
        Args:
            story: The basic story idea.
            
        Returns:
            An integer between 5 and 8.
        """
        prompt = (
            f"Based on this story idea, suggest how many episodes it needs.\n"
            f"Title: {story.title}\n"
            f"Genre: {story.genre}\n"
            f"Description: {story.description}\n"
            f"Return ONLY a single integer between 5 and 8. Nothing else. No explanation."
        )
        response = call_llm(prompt).strip()
        try:
            count = int(response)
            if count < 5: return 5
            if count > 8: return 8
            return count
        except ValueError:
            return 5
