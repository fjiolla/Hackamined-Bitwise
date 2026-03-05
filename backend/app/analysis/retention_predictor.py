"""
Module for predicting retention risk across episode beats.
"""

from typing import Dict, Any, List

from app.models.story_models import EpisodeStructure


class RetentionRiskPredictor:
    """
    Predicts viewer retention risk for a given episode structure
    using heuristics based on narrative engagement factors.
    """

    def predict_retention_risk(self, episode: EpisodeStructure) -> List[Dict[str, Any]]:
        """
        Calculates retention risk per beat.
        
        Args:
            episode: structured episode containing beats.
            
        Returns:
            A list of dictionaries representing the risk per beat.
        """
        results = []
        
        if not episode.beats:
            return results

        beats_count = len(episode.beats)

        for index, beat in enumerate(episode.beats):
            # Base Risk
            risk_score = 30
            
            content_lower = beat.content.lower()
            beat_type_lower = beat.beat_type.lower()
            
            # Dialogue Density
            if '"' in beat.content or "'" in beat.content:
                risk_score += 10
                
            # Hook Strength (only applies to the first beat)
            if index == 0:
                hook_keywords = ["suddenly", "secret", "reveals", "danger"]
                if not any(word in content_lower for word in hook_keywords):
                    risk_score += 20
                    
            # Flatness
            if beat_type_lower in ["conflict", "escalation"]:
                flatness_keywords = ["talks", "walks", "sits", "explains"]
                if any(word in content_lower for word in flatness_keywords):
                    risk_score += 30
                    
            # Cliffhanger Strength (only applies to the last beat)
            if index == beats_count - 1:
                cliffhanger_keywords = ["deadline", "danger", "?"]
                if any(word in content_lower for word in cliffhanger_keywords):
                    risk_score -= 20
                    
            # Clamp risk score to be at least 0
            if risk_score < 0:
                risk_score = 0
                
            # Determine Risk Level Mapping
            if risk_score <= 35:
                risk_level = "LOW"
            elif 36 <= risk_score <= 60:
                risk_level = "MEDIUM"
            else:
                risk_level = "HIGH"
                
            results.append({
                "beat_index": index + 1,
                "time_range": beat.time_range,
                "risk_score": risk_score,
                "risk_level": risk_level
            })
            
        return results
