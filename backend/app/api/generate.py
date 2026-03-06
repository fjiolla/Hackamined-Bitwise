"""
API router for generation operations.
"""
from fastapi import APIRouter
from typing import Dict, Any

from app.models.story_models import StoryIdea
from app.engines.pipeline_engine import PipelineEngine

router = APIRouter()
pipeline_engine = PipelineEngine()
bible_generator = pipeline_engine.bible_generator

@router.post("/generate-series")
async def generate_series_endpoint(story: StoryIdea) -> Dict[str, Any]:
    """
    Endpoint to trigger the full end-to-end AI story generation pipeline.
    
    Args:
        story: The initial StoryIdea with title, description, and genre.
        
    Returns:
        A dictionary containing the full pipeline results including 
        series bible, episodes, analysis, and optimizations.
    """
    return pipeline_engine.run_pipeline(story)

@router.post("/suggest-episodes")
async def suggest_episodes_endpoint(story: StoryIdea) -> Dict[str, Any]:
    """
    Endpoint to suggest an episode count based on the basic story details.
    
    Args:
        story: The initial StoryIdea with title, description, and genre.
        
    Returns:
        A dictionary containing the suggested_count.
    """
    count = bible_generator.suggest_episode_count(story)
    return {"suggested_count": count}
