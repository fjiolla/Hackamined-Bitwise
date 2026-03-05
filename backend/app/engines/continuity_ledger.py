"""
Engine for tracking narrative continuity across episodes.
"""

from typing import Dict, Any, List

from app.models.story_models import EpisodeStructure


class ContinuityLedger:
    """
    Ledger to track story state across episodes for narrative consistency.
    Maintains characters, revealed information, and unresolved plot threads.
    """

    def __init__(self):
        """
        Initialise an empty ledger.
        """
        self.characters_introduced: List[str] = []
        self.revealed_secrets: List[str] = []
        self.unresolved_threads: List[str] = []
        self.timeline_events: List[str] = []

    def update_from_episode(self, episode: EpisodeStructure):
        """
        Extract important events from episode beats and update ledger.
        
        Args:
            episode: The episode structure containing story beats.
        """
        # Hackathon mock logic: In a real app we would use an LLM
        # to analyse the episode beats and extract these details.
        # For prototype purposes, we are doing a simplified mock extraction.
        
        self.timeline_events.append(f"Episode {episode.episode_number} occurred.")
        
        for beat in episode.beats:
            content_lower = beat.content.lower()
            
            # Very basic string matching mock for hackathon prototype
            if "aisha" in content_lower and "Aisha" not in self.characters_introduced:
                self.characters_introduced.append("Aisha")
            if "zara" in content_lower and "Zara" not in self.characters_introduced:
                self.characters_introduced.append("Zara")
                
            if "secret" in content_lower or "lies" in content_lower:
                secret_mock = "Aisha can hear lies"
                if secret_mock not in self.revealed_secrets:
                    self.revealed_secrets.append(secret_mock)
            
            if "uncover" in content_lower or "truth" in content_lower:
                thread_mock = "What is Zara hiding?"
                if thread_mock not in self.unresolved_threads:
                    self.unresolved_threads.append(thread_mock)
            
            if "follows" in content_lower:
                event_mock = "Aisha followed Zara after class"
                if event_mock not in self.timeline_events:
                    self.timeline_events.append(event_mock)

    def get_summary(self) -> Dict[str, List[str]]:
        """
        Return compact JSON summary of current story state.
        
        Returns:
            Dictionary containing the state of the continuity ledger.
        """
        return {
            "characters_introduced": self.characters_introduced,
            "revealed_secrets": self.revealed_secrets,
            "unresolved_threads": self.unresolved_threads,
            "timeline_events": self.timeline_events
        }
