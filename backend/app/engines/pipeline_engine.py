"""
Pipeline Engine for orchestrating the end-to- natural narrative generation workflow.
"""

import asyncio
from typing import Dict, Any, List

from app.models.story_models import StoryIdea, SeriesBible
from app.engines.bible_engine import SeriesBibleGenerator
from app.engines.episode_generator import EpisodeGenerator
from app.engines.continuity_ledger import ContinuityLedger
from app.analysis.emotional_arc import EmotionalArcAnalyzer
from app.analysis.cliffhanger_score import CliffhangerScorer
from app.analysis.retention_predictor import RetentionRiskPredictor
from app.optimisation.stress_test import NarrativeStressTest
from app.optimisation.suggestion_engine import SuggestionEngine
from app.engines.script_generator import ScriptGenerator


class PipelineEngine:
    """
    Orchestrates the entire end-to-end story generation and analysis workflow.
    """

    def __init__(self):
        self.bible_generator = SeriesBibleGenerator()
        self.episode_generator = EpisodeGenerator()
        self.emotional_analyzer = EmotionalArcAnalyzer()
        self.cliffhanger_scorer = CliffhangerScorer()
        self.retention_predictor = RetentionRiskPredictor()
        self.stress_tester = NarrativeStressTest()
        self.suggestion_engine = SuggestionEngine()
        self.script_generator = ScriptGenerator()

    def calculate_series_arc_score(self, processed_episodes: list) -> dict:
        
        cliffhanger_scores = [
            ep['cliffhanger_score']['score']
            for ep in processed_episodes
            if ep.get('cliffhanger_score') and ep['cliffhanger_score'].get('score') is not None
        ]
        avg_cliffhanger = sum(cliffhanger_scores) / len(cliffhanger_scores) if cliffhanger_scores else 0
        
        all_emotions = [
            beat['emotion_score']
            for ep in processed_episodes
            for beat in ep.get('emotional_analysis', [])
            if beat.get('emotion_score') is not None
        ]
        emotional_variance = (max(all_emotions) - min(all_emotions)) if len(all_emotions) > 1 else 0
        
        high_risk_count = sum(
            1 for ep in processed_episodes
            for beat in ep.get('retention_risk', [])
            if beat.get('risk_level') == 'HIGH'
        )
        total_beats = sum(len(ep.get('retention_risk', [])) for ep in processed_episodes)
        
        cliffhanger_component = round((avg_cliffhanger / 10) * 40)
        emotion_component = round(min(emotional_variance, 1.0) * 35)
        retention_component = round(
            max(0, (1 - high_risk_count / total_beats)) * 25
        ) if total_beats > 0 else 0
        
        total = cliffhanger_component + emotion_component + retention_component
        
        if total >= 80:
            grade = "A"
            verdict = "Strong narrative arc with excellent tension and emotional range."
        elif total >= 60:
            grade = "B"
            verdict = "Moderate arc with good structure but room for improvement."
        else:
            grade = "C"
            verdict = "Weak arc — cliffhangers or emotional variance need improvement."
        
        return {
            "series_arc_score": total,
            "grade": grade,
            "verdict": verdict,
            "breakdown": {
                "cliffhanger_strength": cliffhanger_component,
                "emotional_variance": emotion_component,
                "retention_health": retention_component
            },
            "explanation": (
                f"Series scored {total}/100 (Grade {grade}). "
                f"Cliffhanger strength contributed {cliffhanger_component}/40, "
                f"emotional variance {emotion_component}/35, "
                f"retention health {retention_component}/25. "
                f"{verdict}"
            )
        }

    async def run_pipeline(self, story) -> Dict[str, Any]:
        continuity_ledger = ContinuityLedger()  # local, not self
        series_bible = story.series_bible
        episode_count = story.episode_count
        episodes = []
        all_scores = []
        previous_ending = ""

        for ep_number in range(1, episode_count + 1):
            ledger_summary = continuity_ledger.get_summary()

            # ---- Step 1: Generate base episode once ----
            episode = await self.episode_generator.generate_episode(
                series_bible=series_bible,
                episode_number=ep_number,
                previous_ending=previous_ending,
                continuity_context=ledger_summary
            )
            original_episode = episode  # anchor for regeneration

            script = None
            analysis = None

            # ---- Step 2: Repair loop (regeneration only, no fresh generation) ----
            for attempt in range(3):  # 0 = first analysis, 1 and 2 = repairs
                script = await self.script_generator.generate_script(
                    episode_outline=episode,
                    previous_ending=previous_ending
                )
                analysis = self.stress_tester.analyse_episode(script)
                issues = analysis.get("issues", [])
                score = analysis.get("score", 0)

                if not issues:
                    break  # episode is good, accept it

                if attempt < 2:  # only repair on attempts 0 and 1
                    suggestions = self.suggestion_engine.generate_suggestions(issues)
                    episode = await self.episode_generator.regenerate_episode(
                        original_outline=original_episode,  # continuity anchor
                        current_outline=episode,            # what to improve
                        suggestions=suggestions,
                        continuity_context=ledger_summary,
                        previous_ending=previous_ending     # how last ep ended
                    )
                else:
                    analysis["quality_flag"] = "failed_repair"

            # ---- Step 3: Update ledger AFTER episode is finalised ----
            continuity_ledger.update_from_episode(episode)

            # ---- Step 4: Extract ending from script for next episode ----
            previous_ending = "\n".join(script.strip().split("\n")[-20:])

            episodes.append({
                "episode_number": ep_number,
                "outline": episode,
                "script": script,
                "analysis": analysis
            })
            all_scores.append(score)

        # ---- Weighted series score ----
        weighted = sum(s * (i + 1) for i, s in enumerate(all_scores))
        total_weight = sum(range(1, len(all_scores) + 1))
        avg_score = round(weighted / total_weight, 2) if all_scores else 0

        return {
            "series_bible": series_bible,
            "episodes": episodes,
            "series_score": avg_score
        }
    async def regenerate_episode(
        self,
        episode_number: int,
        series_bible: SeriesBible,
        suggestions: List[str],
        is_last_episode: bool = False,
        prior_context: str = "",
        previous_ending: str = "",
        next_episode_hook: str = ""
    ) -> Dict[str, Any]:

        episode = await self.episode_generator.regenerate_episode(
            episode_number=episode_number,
            series_bible=series_bible,
            suggestions=suggestions,
            is_last_episode=is_last_episode,
            prior_context=prior_context,
            next_episode_hook=next_episode_hook
        )
        episode.is_last_episode = is_last_episode

        emotional_analysis = self.emotional_analyzer.analyse_episode(episode)
        cliffhanger_score = self.cliffhanger_scorer.score_cliffhanger(episode)
        retention_risk = self.retention_predictor.predict_retention_risk(
            episode,
            emotional_analysis=emotional_analysis
        )
        stress_test_results = self.stress_tester.run_tests(
            episode=episode,
            emotional_analysis=emotional_analysis,
            cliffhanger_score=cliffhanger_score,
            retention_results=retention_risk
        )
        suggestions_result = self.suggestion_engine.generate_suggestions(
            episode=episode,
            issues=stress_test_results,
            emotional_analysis=emotional_analysis,
            retention_results=retention_risk,
            cliffhanger_score=cliffhanger_score
        )
        script = await self.script_generator.generate_script(
            episode,
            series_bible,
            is_last_episode=is_last_episode,
            previous_ending=previous_ending
        )

        return {
            "episode_number": episode.episode_number,
            "beats": [beat.model_dump() for beat in episode.beats],
            "script": script,
            "emotional_analysis": emotional_analysis,
            "cliffhanger_score": cliffhanger_score,
            "retention_risk": retention_risk,
            "issues": stress_test_results.get("issues", []),
            "suggestions": suggestions_result.get("suggestions", [])
        }