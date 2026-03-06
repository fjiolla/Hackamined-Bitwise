"""
Module for generating structured improvement suggestions for weak story elements.
"""

from typing import Dict, Any, List

from app.models.story_models import EpisodeStructure


class SuggestionEngine:
    """
    Engine to read detected narrative issues and suggest improvements.
    """

    def generate_suggestions(
        self,
        episode: EpisodeStructure,
        issues: Dict[str, Any],
        emotional_analysis: List[Dict[str, Any]],
        retention_results: List[Dict[str, Any]],
        cliffhanger_score: Dict[str, Any] = None
    ) -> Dict[str, List[Dict[str, str]]]:
        """
        Generates improvement recommendations based on detected issues.

        Args:
            episode: The original episode structure.
            issues: The issues detected by NarrativeStressTest.

        Returns:
            A dictionary containing a list of structured suggestions.
        """
        suggestions = []
        detected_issues = issues.get("issues", [])

        # If no issues detected, return empty with positive message
        if not detected_issues:
            return {
                "suggestions": [],
                "overall": "No major issues detected. This episode has strong narrative structure."
            }

        # 1. Loop through detected issues.
        for issue in detected_issues:
            issue_type = issue.get("type")
            suggestion_text = ""

            # 2. Map each issue type to a suggestion rule.
            if issue_type == "weak_hook":
                hook_score = emotional_analysis[0]['emotion_score']
                suggestion_text = f"Hook at 0-15s has emotional score of {hook_score} — consider opening with immediate danger or mystery to grab attention instantly"

            elif issue_type == "flat_emotion":
                flat_beats = [a['beat_type'] for a in emotional_analysis if a['risk_flag']]
                suggestion_text = f"Emotional flatness detected at {', '.join(flat_beats)} — introduce a new conflict or unexpected revelation here"

            elif issue_type == "weak_cliffhanger":
                score = (cliffhanger_score or {}).get('score', 0)
                suggestion_text = f"Cliffhanger scored {score}/10 — end with an unanswered question, physical danger, or shocking revelation"

            elif issue_type == "high_retention_risk":
                high_risk = [r['time_range'] for r in retention_results if r['risk_level'] == 'HIGH']
                suggestion_text = f"High viewer drop-off risk at {', '.join(high_risk)} — add a twist or unexpected reveal at this moment"
            else:
                # Fallback for unknown issues
                suggestion_text = f"Review the beat related to: {issue.get('message')}"

            if suggestion_text:
                suggestions.append({
                    "issue_type": issue_type,
                    "suggestion": suggestion_text
                })

        # 3. Return structured suggestions.
        return {"suggestions": suggestions}
