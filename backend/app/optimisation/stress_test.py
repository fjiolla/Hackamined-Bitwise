"""
Module for testing an episode's narrative and detecting structural weaknesses.
"""

from typing import Dict, Any, List

from app.models.story_models import EpisodeStructure
from app.analysis.semantic_scorer import score_engagement, score_narrative_flow, score_cliffhanger_semantic


class NarrativeStressTest:
    """
    Evaluates an episode structure and existing analysis data
    to detect critical structural weaknesses.
    """

    def run_tests(
        self,
        episode: EpisodeStructure,
        emotional_analysis: List[Dict[str, Any]],
        cliffhanger_score: Dict[str, Any],
        retention_results: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Run all narrative stress tests.

        Args:
            episode: The full episode structure.
            emotional_analysis: The results from the EmotionalArcAnalyzer.
            cliffhanger_score: The result from the CliffhangerScorer.
            retention_results: The results from the RetentionRiskPredictor.

        Returns:
            A dictionary containing a list of detected issues.
        """
        issues = []

        if not episode.beats:
            return {"issues": issues}

        # 1. Hook Strength Test
        hook_engagement = score_engagement(episode.beats[0].content)
        if hook_engagement < 0:
            issues.append({"type": "weak_hook", "message": "Hook lacks immediate tension."})

        # 2. Emotional Flatness Test
        has_flat_emotion = any(
            analysis_beat.get("risk_flag") is True
            for analysis_beat in emotional_analysis
        )
        if has_flat_emotion:
            issues.append({
                "type": "flat_emotion",
                "message": "Emotional variance too low between beats."
            })

        # 3. Cliffhanger Impact Test
        if not episode.is_last_episode:
            cliff_result = score_cliffhanger_semantic(episode.beats[-1].content)
            if cliff_result["score"] < 4:
                issues.append({
                    "type": "weak_cliffhanger",
                    "message": f"Cliffhanger score is low ({cliff_result['score']}/10)."
                })

        # 4. Retention Risk Test
        has_high_risk = any(
            beat_risk.get("risk_level") == "HIGH"
            for beat_risk in retention_results
        )
        if has_high_risk:
            issues.append({
                "type": "high_retention_risk",
                "message": "One or more beats have a HIGH risk of viewer drop-off."
            })

        flow_issues = score_narrative_flow(episode.beats)
        issues.extend(flow_issues)

        return {"issues": issues}
