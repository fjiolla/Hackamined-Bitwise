"""
Analyzer for detecting emotional shifts across episode beats.
"""

from transformers import pipeline
from typing import Dict, Any, List

from app.models.story_models import EpisodeStructure

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

def score_emotion(text: str, beat_type: str = "") -> float:
    result = sentiment_pipeline(text[:512])[0]
    score = result['score']
    label = result['label']

    if label == 'LABEL_0':
        raw = -round(score, 2)
    elif label == 'LABEL_2':
        raw = round(score, 2)
    else:
        raw = 0.0

    if beat_type.lower() == "cliffhanger":
        return abs(raw)

    return raw


class EmotionalArcAnalyzer:
    """
    Analyzes emotional progression within an episode to identify flat engagement zones.
    """
    
    def analyse_episode(self, episode: EpisodeStructure) -> List[Dict[str, Any]]:
        results = []
        previous_score = None
        
        for index, beat in enumerate(episode.beats):
            # 1. Compute a sentiment score for each beat.
            current_score = score_emotion(beat.content, beat.beat_type)
            
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
