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
        issues: Dict[str, List[Dict[str, Any]]]
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

        # 1. Loop through detected issues.
        for issue in detected_issues:
            issue_type = issue.get("type")
            suggestion_text = ""

            # 2. Map each issue type to a suggestion rule.
            if issue_type == "weak_hook":
                suggestion_text = "Suggest adding a shocking event, mystery, or danger in the first 5 seconds."
            elif issue_type == "flat_emotion":
                suggestion_text = "Suggest introducing a new conflict or emotional shift."
            elif issue_type == "weak_cliffhanger":
                suggestion_text = "Suggest ending the episode with an unanswered question or urgent situation."
            elif issue_type == "high_retention_risk":
                suggestion_text = "Suggest adding a twist or unexpected reveal earlier in the episode."
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
