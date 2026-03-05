"""
Engine for generating sequence of structured episodes based on a SeriesBible.
"""

import json
from typing import Dict, Any, List

from app.models.story_models import SeriesBible, EpisodeBeat, EpisodeStructure
from app.utils.gemini_client import call_llm


class EpisodeGenerator:
    """
    Engine to generate a sequence of structured episodes for vertical storytelling.
    """

    def generate_episode(self, episode_number: int, series_bible: SeriesBible) -> EpisodeStructure:
        """
        Generates a structured episode based on the SeriesBible.

        Args:
            episode_number: The episode number to generate.
            series_bible: The foundational elements of the series.

        Returns:
            An EpisodeStructure object containing the structured 90-second episode beats.
        """
        # 1 Build prompt using series_bible
        prompt = (
            f"Generate Episode {episode_number} beats based on the series bible.\n"
            f"Return ONLY valid JSON with no extra text.\n"
            f"The JSON should contain precisely these string keys: 'hook', 'conflict', 'escalation', 'twist', 'cliffhanger'.\n"
            f"Each value should be a short string describing the beat.\n"
            f"Archetype: {series_bible.archetype}\n"
            f"Protagonist: {series_bible.protagonist}\n"
            f"Supporting Characters: {', '.join(series_bible.supporting_characters)}\n"
            f"Central Conflict: {series_bible.central_conflict}\n"
        )

        # 2 Call placeholder function
        response_text = call_llm(prompt).strip()
        
        # Parse the structured JSON output
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()
            
        try:
            response_data = json.loads(response_text)
        except json.JSONDecodeError:
            response_data = {
                "hook": "Error generating hook",
                "conflict": "Error generating conflict",
                "escalation": "Error generating escalation",
                "twist": "Error generating twist",
                "cliffhanger": "Error generating cliffhanger"
            }

        # 3 Expect LLM to return beat descriptions
        # 4 Convert beats into EpisodeBeat objects
        beats = [
            EpisodeBeat(
                beat_type="Hook",
                content=response_data.get("hook", ""),
                time_range="0-15s"
            ),
            EpisodeBeat(
                beat_type="Conflict",
                content=response_data.get("conflict", ""),
                time_range="15-35s"
            ),
            EpisodeBeat(
                beat_type="Escalation",
                content=response_data.get("escalation", ""),
                time_range="35-55s"
            ),
            EpisodeBeat(
                beat_type="Twist",
                content=response_data.get("twist", ""),
                time_range="55-75s"
            ),
            EpisodeBeat(
                beat_type="Cliffhanger",
                content=response_data.get("cliffhanger", ""),
                time_range="75-90s"
            )
        ]

        # 5 Return EpisodeStructure
        return EpisodeStructure(
            episode_number=episode_number,
            beats=beats
        )

    def generate_series(self, series_bible: SeriesBible, episode_count: int = 5) -> List[EpisodeStructure]:
        """
        Generates a sequence of structured episodes mapping the whole series.

        Args:
            series_bible: The foundational elements of the series.
            episode_count: The total number of episodes in the series. Default is 5.

        Returns:
            A list of EpisodeStructure objects representing the generated series.
        """
        episodes = []
        for i in range(1, episode_count + 1):
            episode = self.generate_episode(episode_number=i, series_bible=series_bible)
            episodes.append(episode)

        return episodes
