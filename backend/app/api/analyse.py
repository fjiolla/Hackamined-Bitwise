from fastapi import APIRouter
from typing import List, Dict, Any
from app.models.story_models import EpisodeStructure
from app.analysis.emotional_arc import EmotionalArcAnalyzer
from app.analysis.cliffhanger_score import CliffhangerScorer
from app.analysis.retention_predictor import RetentionRiskPredictor
from app.optimisation.stress_test import NarrativeStressTest
from app.optimisation.suggestion_engine import SuggestionEngine

router = APIRouter()
emotional_analyzer = EmotionalArcAnalyzer()
cliffhanger_scorer = CliffhangerScorer()
retention_predictor = RetentionRiskPredictor()
stress_tester = NarrativeStressTest()
suggestion_engine = SuggestionEngine()

@router.post("/emotional-arc")
async def analyse_emotional_arc(episode: EpisodeStructure) -> List[Dict[str, Any]]:
    return emotional_analyzer.analyse_episode(episode)

@router.post("/cliffhanger")
async def analyse_cliffhanger(episode: EpisodeStructure) -> Dict[str, Any]:
    return cliffhanger_scorer.score_cliffhanger(episode)

@router.post("/retention")
async def analyse_retention(episode: EpisodeStructure) -> List[Dict[str, Any]]:
    emotional = emotional_analyzer.analyse_episode(episode)
    return retention_predictor.predict_retention_risk(episode, emotional_analysis=emotional)

@router.post("/full")
async def analyse_full(episode: EpisodeStructure) -> Dict[str, Any]:
    emotional = emotional_analyzer.analyse_episode(episode)
    cliffhanger = cliffhanger_scorer.score_cliffhanger(episode)
    retention = retention_predictor.predict_retention_risk(episode, emotional_analysis=emotional)
    stress = stress_tester.run_tests(
        episode=episode,
        emotional_analysis=emotional,
        cliffhanger_score=cliffhanger,
        retention_results=retention
    )
    suggestions = suggestion_engine.generate_suggestions(
        episode=episode,
        issues=stress,
        emotional_analysis=emotional,
        retention_results=retention,
        cliffhanger_score=cliffhanger
    )
    return {
        "emotional_analysis": emotional,
        "cliffhanger_score": cliffhanger,
        "retention_risk": retention,
        "issues": stress.get("issues", []),
        "suggestions": suggestions.get("suggestions", [])
    }
