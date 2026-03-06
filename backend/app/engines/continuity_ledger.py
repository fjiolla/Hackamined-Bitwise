"""
Engine for tracking narrative continuity across episodes.
"""

from typing import Dict, Any, List

from app.models.story_models import EpisodeStructure
import spacy
from app.analysis.semantic_scorer import is_secret_revealed, is_unresolved_thread

nlp = spacy.load("en_core_web_sm")


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
        self.timeline_events.append(f"Episode {episode.episode_number} occurred.")
        
        for beat in episode.beats:
            doc = nlp(beat.content)
            content_lower = beat.content.lower()
            
            # Extract character names automatically
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    if ent.text not in self.characters_introduced:
                        self.characters_introduced.append(ent.text)
            
            # Detect revealed secrets — store actual beat content
            if is_secret_revealed(beat.content):
                secret = f"Ep{episode.episode_number} - {beat.beat_type}: {beat.content[:80]}"
                if secret not in self.revealed_secrets:
                    self.revealed_secrets.append(secret)
            
            # Detect unresolved threads — store actual beat content
            if is_unresolved_thread(beat.content):
                thread = f"Ep{episode.episode_number} - {beat.beat_type}: {beat.content[:80]}"
                if thread not in self.unresolved_threads:
                    self.unresolved_threads.append(thread)
            
            # Track significant timeline events from twist and cliffhanger beats
            if beat.beat_type.lower() in ["twist", "cliffhanger"]:
                event = f"Ep{episode.episode_number} - {beat.content[:80]}"
                if event not in self.timeline_events:
                    self.timeline_events.append(event)
                    

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
