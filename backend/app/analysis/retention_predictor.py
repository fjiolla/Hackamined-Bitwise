"""
Module for predicting retention risk across episode beats.
"""

from typing import Dict, Any, List

from app.models.story_models import EpisodeStructure
from app.analysis.semantic_scorer import score_engagement


class RetentionRiskPredictor:
    def predict_retention_risk(self, episode: EpisodeStructure, emotional_analysis: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        results = []
        
        if not episode.beats:
            return results

        beats_count = len(episode.beats)

        for index, beat in enumerate(episode.beats):
            engagement = score_engagement(beat.content)
            # engagement is -1 to +1
            # high engagement = low risk, low engagement = high risk
            if engagement > 0.3:
                risk_score = 20   # LOW
            elif engagement > 0:
                risk_score = 45   # MEDIUM
            else:
                risk_score = 70   # HIGH
                
            # Get emotion score for this beat if available
            emotion_score = 0.0
            if emotional_analysis and index < len(emotional_analysis):
                emotion_score = emotional_analysis[index]['emotion_score']

            # High emotional intensity = lower retention risk
            if abs(emotion_score) >= 0.7:
                risk_score -= 15
            elif abs(emotion_score) >= 0.4:
                risk_score -= 8
            elif abs(emotion_score) < 0.1:
                risk_score += 15
                
            # Determine Risk Level Mapping
            if risk_score <= 35:
                risk_level = "LOW"
            elif 36 <= risk_score <= 60:
                risk_level = "MEDIUM"
            else:
                risk_level = "HIGH"
                
            if risk_level == "HIGH":
                explanation = f"High drop-off risk at {beat.time_range} — semantic engagement score {round(engagement, 2)} indicates insufficient tension to retain viewers"
            elif risk_level == "MEDIUM":
                explanation = f"Moderate retention risk at {beat.time_range} — engagement score {round(engagement, 2)} suggests room for improvement"
            else:
                explanation = f"Low retention risk at {beat.time_range} — strong engagement score {round(engagement, 2)} should keep viewers watching"

            results.append({
                "beat_index": index + 1,
                "time_range": beat.time_range,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "explanation": explanation
            })
            
        return results
