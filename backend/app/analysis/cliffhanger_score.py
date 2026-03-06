"""
Engine for evaluating the quality of an episode's cliffhanger.
"""

from typing import Dict, Any

from app.models.story_models import EpisodeStructure
from app.analysis.semantic_scorer import score_cliffhanger_semantic


class CliffhangerScorer:
    def score_cliffhanger(self, episode: EpisodeStructure) -> Dict[str, Any]:
        if not episode.beats:
            return {"score": 0, "breakdown": {}}
        cliffhanger_beat = episode.beats[-1]
        result = score_cliffhanger_semantic(cliffhanger_beat.content)
        return result
