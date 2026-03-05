"""
Analyzer for detecting emotional shifts across episode beats.
"""

import random
from typing import Dict, Any, List

from app.models.story_models import EpisodeStructure


def score_emotion(text: str) -> float:
    """
    Mock function to compute a sentiment score for a given text.
    
    Args:
        text: The content of the story beat.
        
    Returns:
        A float representing the sentiment score, between -1.0 and 1.0.
    """
    # Hackathon prototype: returning a random score for now
    # In a real implementation, this would use an NLP library or LLM
    return round(random.uniform(-1.0, 1.0), 2)


class EmotionalArcAnalyzer:
    """
    Analyzes emotional progression within an episode to identify flat engagement zones.
    """
    
    def analyse_episode(self, episode: EpisodeStructure) -> List[Dict[str, Any]]:
        """
        Detect emotional shifts across episode beats.
        
        Args:
            episode: The episode structure containing story beats.
            
        Returns:
            A list of dictionary results containing analysis per beat.
        """
        results = []
        previous_score = None
        
        for index, beat in enumerate(episode.beats):
            # 1. Compute a sentiment score for each beat.
            current_score = score_emotion(beat.content)
            
            risk_flag = False
            
            # 2. Compare consecutive beats.
            if previous_score is not None:
                difference = abs(current_score - previous_score)
                # 3. If difference < 0.15 -> mark as flat engagement zone.
                if difference < 0.15:
                    risk_flag = True
                    
            # 4. Return structured analysis results.
            results.append({
                "beat_index": index + 1,
                "beat_type": beat.beat_type.lower(),
                "emotion_score": current_score,
                "risk_flag": risk_flag
            })
            
            previous_score = current_score
            
        return results
