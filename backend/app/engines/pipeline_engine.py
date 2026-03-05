"""
Pipeline Engine for orchestrating the end-to- natural narrative generation workflow.
"""

from typing import Dict, Any

from app.models.story_models import StoryIdea
from app.engines.bible_engine import SeriesBibleGenerator
from app.engines.episode_generator import EpisodeGenerator
from app.engines.continuity_ledger import ContinuityLedger
from app.analysis.emotional_arc import EmotionalArcAnalyzer
from app.analysis.cliffhanger_score import CliffhangerScorer
from app.analysis.retention_predictor import RetentionRiskPredictor
from app.optimisation.stress_test import NarrativeStressTest
from app.optimisation.suggestion_engine import SuggestionEngine


class PipelineEngine:
    """
    Orchestrates the entire end-to-end story generation and analysis workflow.
    """

    def __init__(self):
        """
        Initializes the various components of the pipeline.
        """
        self.bible_generator = SeriesBibleGenerator()
        self.episode_generator = EpisodeGenerator()
        self.continuity_ledger = ContinuityLedger()
        self.emotional_analyzer = EmotionalArcAnalyzer()
        self.cliffhanger_scorer = CliffhangerScorer()
        self.retention_predictor = RetentionRiskPredictor()
        self.stress_tester = NarrativeStressTest()
        self.suggestion_engine = SuggestionEngine()

    def run_pipeline(self, story: StoryIdea) -> Dict[str, Any]:
        """
        Runs the full story generation and analysis pipeline.
        
        Args:
            story: The initial short story idea and genre.
            
        Returns:
            A cohesive dictionary combining all generated narrative data, 
            analysis tools, and optimizations.
        """
        # 1. Generate Series Bible
        series_bible = self.bible_generator.generate_series_bible(story)

        # 2. Generate Episode Series
        episodes = self.episode_generator.generate_series(series_bible)

        # 3. Initialise Continuity Ledger (created in __init__, but we process here)
        processed_episodes = []

        # 4. For each episode:
        for episode in episodes:
            # update ledger
            self.continuity_ledger.update_from_episode(episode)
            
            # run emotional analysis
            emotional_analysis = self.emotional_analyzer.analyse_episode(episode)
            
            # score cliffhanger
            cliffhanger_score = self.cliffhanger_scorer.score_cliffhanger(episode)
            
            # predict retention risk
            retention_risk = self.retention_predictor.predict_retention_risk(episode)
            
            # run stress tests
            stress_test_results = self.stress_tester.run_tests(
                episode=episode,
                emotional_analysis=emotional_analysis,
                cliffhanger_score=cliffhanger_score,
                retention_results=retention_risk
            )
            
            # generate suggestions
            suggestions_result = self.suggestion_engine.generate_suggestions(
                episode=episode,
                issues=stress_test_results
            )
            
            # Use Pydantic dict formatting to return clean structured JSON
            processed_episodes.append({
                "episode_number": episode.episode_number,
                "beats": [beat.model_dump() for beat in episode.beats],
                "emotional_analysis": emotional_analysis,
                "cliffhanger_score": cliffhanger_score,
                "retention_risk": retention_risk,
                "issues": stress_test_results.get("issues", []),
                "suggestions": suggestions_result.get("suggestions", [])
            })

        # 5. Collect all outputs
        return {
            "series_bible": series_bible.model_dump(),
            "episodes": processed_episodes
        }
