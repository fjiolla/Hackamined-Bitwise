"""
Engine for evaluating the quality of an episode's cliffhanger.
"""

from typing import Dict, Any

from app.models.story_models import EpisodeStructure


class CliffhangerScorer:
    def score_cliffhanger(self, episode: EpisodeStructure) -> Dict[str, Any]:
        if not episode.beats:
            return {
                "score": 0,
                "breakdown": {
                    "unresolved_tension": 0,
                    "stakes_escalation": 0,
                    "character_jeopardy": 0,
                    "revelation_hook": 0,
                    "time_pressure": 0
                }
            }

        # 1. Extract the last beat (cliffhanger).
        cliffhanger_beat = episode.beats[-1]
        content_lower = cliffhanger_beat.content.lower()

        # Initialize scores
        unresolved_tension = 0
        stakes_escalation = 0
        character_jeopardy = 0
        revelation_hook = 0
        time_pressure = 0

        # 2. Analyse the text using simple keyword heuristics.
        # 3. Assign scores for each dimension (0-2).
        
        # Unresolved tension: question marks or specific words
        if "?" in content_lower or any(word in content_lower for word in ["why", "who", "what", "where", "how"]):
            unresolved_tension = 2
        elif any(word in content_lower for word in ["wonder", "mystery", "unknown"]):
            unresolved_tension = 1

        # Stakes escalation: words indicating consequences
        if any(word in content_lower for word in ["loss", "fail", "everything", "never"]):
            stakes_escalation = 2
        elif any(word in content_lower for word in ["worse", "trouble", "complicate"]):
            stakes_escalation = 1

        # Character jeopardy: danger or risk words
        if any(word in content_lower for word in ["die", "kill", "danger", "trap", "catch"]):
            character_jeopardy = 2
        elif any(word in content_lower for word in ["risk", "scare", "fear", "follow"]):
            character_jeopardy = 1

        # Revelation hook: secrets being revealed or teased
        if any(word in content_lower for word in ["secret", "realize", "discover", "reveal"]):
            revelation_hook = 2
        elif any(word in content_lower for word in ["hide", "lie", "truth"]):
            revelation_hook = 1

        # Time pressure: urgency words
        if any(word in content_lower for word in ["deadline", "countdown", "bomb", "seconds"]):
            time_pressure = 2
        elif any(word in content_lower for word in ["now", "tonight", "hurry", "fast", "suddenly"]):
            time_pressure = 1

        # 4. Compute total score.
        total_score = (
            unresolved_tension + 
            stakes_escalation + 
            character_jeopardy + 
            revelation_hook + 
            time_pressure
        )

        # 5. Return structured JSON result.
        return {
            "score": total_score,
            "breakdown": {
                "unresolved_tension": unresolved_tension,
                "stakes_escalation": stakes_escalation,
                "character_jeopardy": character_jeopardy,
                "revelation_hook": revelation_hook,
                "time_pressure": time_pressure
            }
        }
